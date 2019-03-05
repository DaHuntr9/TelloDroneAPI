import pytest

from tests.MockDrone import MockDrone


@pytest.fixture
def drone():
    return MockDrone()


@pytest.mark.asyncio
async def test_connect(drone):
    assert await drone.connect() is True


@pytest.mark.asyncio
async def test_drone_command_fails_if_not_connected(drone: MockDrone):
    with pytest.raises(RuntimeError):
        await drone.connection.get_battery_level()


@pytest.mark.asyncio
async def test_battery(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_battery_level() == 95


@pytest.mark.asyncio
async def test_temperature(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_temperature() == "40-43 C"


@pytest.mark.asyncio
async def test_velocity(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_velocity() == 100.0
