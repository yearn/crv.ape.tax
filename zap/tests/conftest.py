import pytest


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
def zap(accounts, CurveVestingBackscratch):
    return CurveVestingBackscratch.deploy({"from": accounts[0]})
