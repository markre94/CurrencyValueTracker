import tempfile

import pytest
from currency_monitor import PriceTracker
from datetime import datetime, timedelta

@pytest.fixture()
def provide_test_tracker():
    pass

@pytest.fixture
def provide_test_file():
    with tempfile.NamedTemporaryFile(suffix='.csv') as fp:
        yield fp