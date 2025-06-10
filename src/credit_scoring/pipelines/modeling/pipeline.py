from kedro.pipeline import Pipeline, node
from .nodes import train_model, predict_model

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=train_model,
            inputs="clean_train",
            outputs=None, 
            name="train_model_node"
        ),
        node(
            func=predict_model,
            inputs=["clean_test", "clean_train"], 
            outputs="predictions",
            name="predict_model_node"
        ),
    ])
