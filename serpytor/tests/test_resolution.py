from serpytor.resolver.resolve import resolve_base
import pytest


def test_base_resolution() -> None:
    assert resolve_base().absolute() != __file__
