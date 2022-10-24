import pytest
from serpytor.pipelines import Pipeline


def producer(*args, **kwargs):
    return [1, 0, 1, 0, 1]


def proc1(data, *args, **kwargs):
    print(data)
    mod_data = [i + 1 for i in data]
    return mod_data


def proc2(data, *args, **kwargs):
    print(data)
    mod_data2 = [i**2 for i in data]
    return mod_data2


def test_pipeline():
    pipe = Pipeline(pipeline=[(producer, [], {}), (proc1, [], {}), (proc2, [], {})])

    finished_data = pipe.execute_pipeline()
    print(finished_data)


if __name__ == "__main__":
    test_pipeline()
