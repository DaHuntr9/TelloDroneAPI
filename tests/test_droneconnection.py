import asyncio

import pytest

from tests.MockDrone import MockDrone


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    return loop

@pytest.fixture
def drone():
    return MockDrone()


@pytest.mark.asyncio
async def test_connect(drone):
    assert await drone.connect() is True


@pytest.mark.asyncio
async def test_battery(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_battery_level() is 95
