from emma_experience_hub.commands.simbot.cli import (
    OBSERVABILITY_COMPOSE_PATH,
    SERVICE_REGISTRY_PATH,
    SERVICES_COMPOSE_PATH,
    SERVICES_PROD_COMPOSE_PATH,
    SERVICES_STAGING_COMPOSE_PATH,
    run_background_services as run_exp_hub_background_services,
)
from simbot_offline_inference.settings import Settings


def run_background_services() -> None:
    """Run the background services for the Experience Hub."""
    settings = Settings()
    settings.put_settings_in_environment()

    run_exp_hub_background_services(
        service_registry_path=SERVICE_REGISTRY_PATH,
        services_docker_compose_path=settings.experience_hub_dir.joinpath(SERVICES_COMPOSE_PATH),
        staging_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            SERVICES_STAGING_COMPOSE_PATH
        ),
        production_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            SERVICES_PROD_COMPOSE_PATH
        ),
        observability_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            OBSERVABILITY_COMPOSE_PATH
        ),
        model_storage_dir=settings.models_dir,
        download_models=True,
        force_download=False,
        run_in_background=False,
        enable_observability=False,
        is_production=False,
    )
