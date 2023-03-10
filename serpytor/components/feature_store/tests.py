import pandas as pd
from feature_stores import SimpleFeatureStore


def test_simplefeaturestore() -> None:
    df = pd.read_csv(
        "https://raw.githubusercontent.com/kylegallatin/components-of-an-ml-system/main/data/user_data.csv"
    )
    df.set_index("user_id", inplace=True)

    feature_store = SimpleFeatureStore(df, backend="pandas")

    assert feature_store.get_all_data() == df.T.to_dict()
