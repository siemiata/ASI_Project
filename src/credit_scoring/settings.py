"""Project settings. No Spark here."""

# Brak hooków
HOOKS = ()

# Ustawienie loadera configu (jeśli faktycznie używasz niestandardowych wzorców)
from kedro.config import OmegaConfigLoader

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        # Jeśli nie używasz spark*, możesz to też usunąć
        "spark": ["spark*", "spark*/**"],
    },
}