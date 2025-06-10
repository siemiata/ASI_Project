"""Project settings. No Spark here."""


HOOKS = ()


from kedro.config import OmegaConfigLoader

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        
        "spark": ["spark*", "spark*/**"],
    },
}
