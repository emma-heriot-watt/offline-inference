import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Literal, Optional
from uuid import uuid1

import orjson
from loguru import logger


def calculate_subgoal_completion_rate(subgoal_completion_status: list[Literal[0, 1]]) -> float:
    """Calculate the subgoal completion rate for the given set of subgoals."""
    try:
        return sum(subgoal_completion_status) / len(subgoal_completion_status)
    except ZeroDivisionError:
        return 0


class SimBotEvaluationMetrics:
    """Store and calculate metrics for the evaluation."""

    def __init__(self, evaluation_output_dir: Path, output_metrics_file: Path) -> None:
        self._output_path = evaluation_output_dir
        self._output_metrics_file = output_metrics_file

        self._games_played = 0
        self._games_completed = 0

        self._subgoals_completed = 0
        self._total_subgoals = 0

        self._mission_groups: list[str] = []
        self._games_played_per_mission_group = Counter[str]()
        self._games_completed_per_mission_group = Counter[str]()

    @property
    def games_failed(self) -> int:
        """Get the total number of games where the agent failed outright."""
        return self._games_played - self._games_completed

    @property
    def overall_success_rate(self) -> float:
        """Calculate the overall success rate."""
        try:
            return self._games_completed / self._games_played
        except ZeroDivisionError:
            return 0

    @property
    def overall_subgoal_completion_rate(self) -> float:
        """Calculate the overall subgoal completion rate."""
        try:
            return self._subgoals_completed / self._total_subgoals
        except ZeroDivisionError:
            return 0

    @property
    def success_rate_per_mission_group(self) -> dict[str, float]:
        """Calculate the success rate per mission group."""
        output = {}

        for mission_group in set(self._mission_groups):
            try:
                output[mission_group] = (
                    self._games_completed_per_mission_group[mission_group]
                    / self._games_played_per_mission_group[mission_group]
                )
            except (KeyError, ZeroDivisionError):
                output[mission_group] = 0

        return output

    def has_mission_been_evaluated(self, mission_name: str) -> bool:
        """Check if the mission has already been evaluated."""
        return self._output_path.joinpath(f"{mission_name}.json").exists()

    def add_mission_metrics(
        self,
        mission_name: str,
        mission_group: Optional[str],
        is_mission_completed: bool,
        subgoal_completion_status: list[Literal[0, 1]],
        predicted_actions: list[dict[str, Any]],
        last_game_state: dict[str, Any],
    ) -> None:
        """Add metrics from a recently evaluated mission."""
        self._games_played += 1

        if is_mission_completed:
            self._games_completed += 1

        if mission_group:
            self._mission_groups.append(mission_group)
            self._games_played_per_mission_group.update([mission_group])

            if is_mission_completed:
                self._games_completed_per_mission_group.update([mission_group])

        self._total_subgoals += len(subgoal_completion_status)
        self._subgoals_completed += sum(subgoal_completion_status)

        predicted_actions = [{**action, "id": str(uuid1())} for action in predicted_actions]

        output_file = self._output_path.joinpath(f"{mission_name}.json")
        output_results = {
            "predicted_actions": predicted_actions,
            "last_game_state": last_game_state,
        }
        output_file.write_bytes(orjson.dumps(output_results))

        logger.info(f"Test #{self._games_played} over")
        logger.info(f"Mission completion status: {is_mission_completed}")
        logger.info(f"Subgoal completion status: {subgoal_completion_status}")
        logger.info(
            f"Subgoal completion rate for test: {calculate_subgoal_completion_rate(subgoal_completion_status)}"
        )
        logger.info(
            f"Current success rate per mission group: {self.success_rate_per_mission_group}"
        )

        self.log_overall_metrics()

    def log_overall_metrics(self) -> None:
        """Log the metrics to the CLI."""
        logger.info(f"Games played: {self._games_played}")
        logger.info(f"Overall success rate: {self.overall_success_rate}")
        logger.info(f"Overall subgoal completion rate: {self.overall_subgoal_completion_rate}")
        logger.info(f"Success rate per mission group: {self.success_rate_per_mission_group}")

        output = {
            "games_played": self._games_played,
            "games_completed": self._games_completed,
            "subgoals_completed": self._subgoals_completed,
            "total_subgoals": self._total_subgoals,
            "mission_groups": list(set(self._mission_groups)),
            "games_played_per_mission_group": self._games_played_per_mission_group,
            "games_completed_per_mission_group": self._games_completed_per_mission_group,
            "success_rate": self.overall_success_rate,
            "subgoal_completion_rate": self.overall_subgoal_completion_rate,
            "success_rate_per_mission": self.success_rate_per_mission_group,
        }

        self._output_metrics_file.write_bytes(orjson.dumps(output))

    def send_to_s3(self) -> None:
        """Upload the results to S3."""
        logger.info("Uploading to S3...")
        subprocess.run(
            f"aws s3 cp {str(self._output_path)} s3://emma-simbot/results/simbot-eval-ai/missions/ --recursive",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"aws s3 cp {str(self._output_metrics_file)} s3://emma-simbot/results/simbot-eval-ai/metrics_{str(uuid1())}.json",
            shell=True,
            check=True,
        )
