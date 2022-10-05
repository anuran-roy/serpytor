import pytest
from serpytor.pipelines import Pipeline


def a():
    print("A")


def b():
    print("B")


def c():
    print("C")


def d():
    print("D")
    # raise Exception("Random error")


def e():
    print("E")


def test_pipeline():
    pipeline = Pipeline(
        [
            (a, [], {}),
            (b, [], {}),
            (c, [], {}),
            (d, [], {}),
            (e, [], {})
        ], 
    )

    pipeline.execute_pipeline()


if __name__ == "__main__":
    test_pipeline()
