from kedro.pipeline import Pipeline, node
from .nodes import clean_data, clean_test, print_columns

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=clean_data,
            inputs="raw_train",
            outputs="clean_train",
            name="clean_train_node"
        ),
        node(
            func=clean_test,
            inputs="raw_test",
            outputs="clean_test",
            name="clean_test_node"
        ),
        node(
            func=print_columns,
            inputs="clean_train",
            outputs=None,
            name="print_columns_node"
        )
    ])