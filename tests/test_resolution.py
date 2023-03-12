from pathlib import Path


from serpytor.components.resolver.resolve import resolve_base


def test_base_resolution() -> None:
    print(resolve_base().absolute())
    assert resolve_base().absolute() == Path(__file__).parent


if __name__ == "__main__":
    test_base_resolution()
