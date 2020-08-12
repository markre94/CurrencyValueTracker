from currency_monitor import PriceTracker
from unittest import mock

@mock.patch('currency_monitor.datetime')
def test_price_tracker_init(mocked_datetime):
    test_tracker = PriceTracker(min_value=4.23, track_to=mocked_datetime)

    assert test_tracker.track_to == mocked_datetime
    assert test_tracker.min_value == 4.23
    assert test_tracker.warnings == 0


