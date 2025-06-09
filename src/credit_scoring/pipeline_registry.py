from typing import Dict
from kedro.pipeline import Pipeline
from credit_scoring.pipelines import data_engineering as de
from credit_scoring.pipelines import modeling as mo

def register_pipelines() -> Dict[str, Pipeline]:
    return {
        "de": de.create_pipeline(),
        "mo": mo.create_pipeline(),
        "__default__": de.create_pipeline() + mo.create_pipeline()
    }