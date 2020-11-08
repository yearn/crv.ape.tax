import pytest
from brownie import interface


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def user(accounts):
    return accounts.at("0x431e81e5dfb5a24541b5ff8762bdef3f32f96354", force=True)


@pytest.fixture
def crv(interface):
    return interface.ERC20("0xD533a949740bb3306d119CC777fa900bA034cd52")


@pytest.fixture
def vault(interface):
    return interface.veCurveVault("0xc5bDdf9843308380375a611c18B50Fb9341f502A")


@pytest.fixture
def vesting(interface):
    return interface.CurveVesting("0x575CCD8e2D300e2377B43478339E364000318E2c")


@pytest.fixture
def minter(interface):
    return interface.CurveMinter("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")


@pytest.fixture
def gauges(interface):
    registry = interface.CurveRegistry("0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c")

    pool_count = registry.pool_count()
    pools = []
    for i in range(pool_count):
        pools.append(registry.pool_list(i))
    
    gauges = []
    for pool in pools:
        gauges_found = registry.get_gauges(pool)
        for gauge in list(gauges_found[0]):
            if gauge != '0x0000000000000000000000000000000000000000':
                gauges.append(gauge)

    gauges += ['0x0000000000000000000000000000000000000000' for _ in range(20 - len(gauges))]
    return gauges


@pytest.fixture
def zap(accounts, CurveBackzapper):
    return CurveBackzapper.deploy({"from": accounts[0]})