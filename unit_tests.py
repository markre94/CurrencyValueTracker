import pytest

from currency_monitor import PriceTracker
from unittest import mock
from unittest.mock import MagicMock
from datetime import datetime, timedelta


@mock.patch('currency_monitor.datetime')
def test_price_tracker_init(mocked_datetime):
    test_tracker = PriceTracker(min_value=4.23, track_to=mocked_datetime, emergency_number="111")

    assert test_tracker.track_to == mocked_datetime
    assert test_tracker.min_value == 4.23
    assert test_tracker.warning_calls == 0


@mock.patch('currency_monitor.requests')
def test_track_price_failed(requests_mock: MagicMock()):
    get_mock = MagicMock()
    get_mock.text = "test_text"
    get_mock.status_code = 404
    requests_mock.get = MagicMock(return_value=get_mock)
    with pytest.raises(ConnectionError):
        PriceTracker.track_price()


@mock.patch('currency_monitor.requests')
def test_track_price_success(requests_mock: MagicMock()):
    get_mock = MagicMock()
    get_mock.text = "test_text"
    get_mock.status_code = 200
    requests_mock.get = MagicMock(return_value=get_mock)

    PriceTracker.track_price()


@pytest.mark.parametrize("price", [4.16, 4.1, 4.0, 4.2, 3.9])
@mock.patch('currency_monitor.PriceTracker.make_phone_call')
def test_min_value_call(mocked_phone_call, price):
    test_tracker = PriceTracker(min_value=4.23, track_to=datetime.today() + timedelta(days=1), emergency_number="111")
    test_tracker.check_min_value(price)
    assert mocked_phone_call.called_with(test_tracker.emergency_number)


@pytest.mark.parametrize("price", [4.11, 4.1, 4.0, 4.2, 3.9])
@mock.patch('currency_monitor.PriceTracker.send_a_message')
def test_min_value_mess(mocked_message, price):
    test_track = PriceTracker(min_value=4.23, track_to=datetime.today() + timedelta(days=1), emergency_number="111")
    test_track.warning_calls = 3
    test_track.check_min_value(price)
    assert mocked_message.called_with(test_track.emergency_number)


@pytest.mark.parametrize("price", [4.25, 4.34, 4.33, 4.24, 4.35])
@mock.patch('currency_monitor.print')
def test_min_value_print(mocked_print, price):
    test_tracker = PriceTracker(min_value=4.23, track_to=datetime.today() + timedelta(days=1), emergency_number="111")
    test_tracker.check_min_value(price)
    assert mocked_print.called_once_with(price)


@mock.patch('currency_monitor.PriceTracker.check_min_value')
def test_write_to_file(mocked_check_value: MagicMock()):
    test_tracker = PriceTracker(min_value=4.23, track_to=datetime.today() + timedelta(seconds=1),
                                emergency_number="111")

    test_price = PriceTracker.track_price()

    test_tracker.write_to_file()
    mocked_check_value.assert_called_with(tracked_price=test_price)


@mock.patch('currency_monitor.PriceTracker.generate_report')
def test_write_to_outside_while(mocked_check_value: MagicMock(), provide_test_file):
    test_tracker = PriceTracker(min_value=4.23, track_to=datetime.today() - timedelta(days=1), emergency_number="111")

    test_tracker.write_to_file()
    mocked_check_value.assert_called_with(f'{datetime.today().date()}.csv')



