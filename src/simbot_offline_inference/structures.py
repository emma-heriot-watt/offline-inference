from datetime import datetime
from typing import Any, Optional

import shortuuid
from pydantic import BaseModel


class SimBotTrajectory(BaseModel):
    """Single trajectory for a given mission."""

    high_level_key: str
    utterances: list[str]
    cdf: dict[str, Any]

    # Used by T1/T2 data
    mission_group: Optional[str]

    def create_session_id(self, prefix: str) -> str:
        """Create a session ID for the trajectory."""
        safe_high_level_key = self.high_level_key.replace("=", "--").replace("#", "_").lstrip("_")

        now = datetime.now()
        date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"

        return f"{prefix}{date_chunk}.{shortuuid.uuid()[:5]}/{safe_high_level_key}"


class SimBotChallenge(BaseModel):
    """Single challenge for the Arena.."""

    high_level_key: str
    plans: list[list[str]]
    cdf: dict[str, Any]

    # Used by T1/T2 data
    mission_group: Optional[str]

    def convert_to_single_trajectory(self) -> list[SimBotTrajectory]:
        """Convert the challenge to a list of single trajectories."""
        trajectories: list[SimBotTrajectory] = []

        for plan in self.plans:
            trajectories.append(
                SimBotTrajectory(
                    high_level_key=self.high_level_key,
                    utterances=plan,
                    cdf=self.cdf,
                    mission_group=self.mission_group,
                )
            )

        return trajectories
