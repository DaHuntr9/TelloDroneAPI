import pytest

from tests.MockDrone import MockDrone


@pytest.fixture
def drone():
    return MockDrone()


@pytest.mark.asyncio
async def test_connect(drone):
    assert await drone.connect() is True


@pytest.mark.asyncio
async def test_drone_command_fails_silently_if_set_and_not_connected(drone):
    drone.silent_errors = True
    assert await drone.connection.get_battery_level() is not None


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


@pytest.mark.asyncio
async def test_altitude(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_altitude() == 12.00


@pytest.mark.asyncio
async def test_height(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_height() == "100cm"


@pytest.mark.asyncio
async def test_attitude(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_attitude() == (-5, 0, 0)


@pytest.mark.asyncio
async def test_pitch(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_pitch() == -5


@pytest.mark.asyncio
async def test_roll(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_roll() == 0


@pytest.mark.asyncio
async def test_yaw(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_yaw() == 0


@pytest.mark.asyncio
async def test_wifi_strength(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_wifi_strength() == 90


@pytest.mark.asyncio
async def test_distance_from_floor(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_distance_from_floor() == "100dm"


@pytest.mark.asyncio
async def test_acceleration(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_acceleration() == (-50.00, 11.00, -999.00)


@pytest.mark.asyncio
async def test_acceleration_x(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_acceleration_x() == -50.00


@pytest.mark.asyncio
async def test_acceleration_y(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_acceleration_y() == 11.00


@pytest.mark.asyncio
async def test_acceleration_z(drone: MockDrone):
    await drone.connect()
    assert await drone.connection.get_acceleration_z() == -999.00
