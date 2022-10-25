import pytest
from serpytor.components.pipelines import Pipeline


def producer(*args, **kwargs):
    return [1, 0, 1, 0, 1]


def consumer1(data, *args, **kwargs):
    print(data)
    mod_data = [i + 1 for i in data]
    raise Exception("Random bs gooooooo")
    return mod_data


def consumer2(data, *args, **kwargs):
    if data is None:
        raise Exception("No data received.")
    print(data)
    mod_data2 = [i**2 for i in data]
    return mod_data2


def test_pipeline():
    pipe = Pipeline(
        pipeline=[(producer, [], {}), (consumer1, [], {}), (consumer2, [], {})]
    )

    finished_data = pipe.execute_pipeline()
    print(finished_data)


if __name__ == "__main__":
    test_pipeline()
