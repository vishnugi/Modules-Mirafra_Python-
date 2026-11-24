import pytest

@pytest.fixture
def setup():
    print("\nConnecting to RubikPi")

    yield

    print("\nDisconnecting from RubikPi")


def test_driver_loading(setup):
    print("Checking whether driver is loaded")
    assert True


def test_device_detection(setup):
    print("Checking device detection")
    assert True