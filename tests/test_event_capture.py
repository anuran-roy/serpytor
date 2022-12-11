import pytest
from serpytor.components.events import EventCapture


def test_event_capture():
    ec = EventCapture()

    @ec.capture_event
    def hi():
        print("Hello")
        raise Exception("Random bs gooooooo!")

    hi()


if __name__ == "__main__":
    test_event_capture()
