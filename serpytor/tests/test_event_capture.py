import pytest
from serpytor.events import EventCapture

def test_event_capture():
    ec = EventCapture()

    @ec.capture_event
    def hi():
        print("Hello")
        raise Exception("Random bs gooooooo!")

    hi()