import pytest


def test_claim(user, lp_3crv, vault, accounts):
    three_gauge = accounts.at("0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A", force=True)
    lp_3crv.transfer(vault, "1000 ether", {"from": three_gauge})
    before = lp_3crv.balanceOf(user)
    vault.claim({"from": user})
    assert lp_3crv.balanceOf(user) > before


def test_backzapper(backzapper, user, crv, vesting, vault, minter, gauges):
    before = vault.balanceOf(user)
    assert vesting.balanceOf(user) > 0
    minter.toggle_approve_mint(backzapper, {"from": user})
    crv.approve(backzapper, 2 ** 256 - 1, {"from": user})
    backzapper.zap(gauges, {"from": user})
    assert vault.balanceOf(user) > before
    assert crv.balanceOf(user) == 0
    assert vesting.balanceOf(user) == 0
    assert crv.balanceOf(backzapper) == 0


def test_3crv_zapper(zap_3crv, lp_3crv, y3crv, vault, accounts, user):
    gauge_3crv = accounts.at("0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A", force=True)
    lp_3crv.transfer(vault, "1000 ether", {"from": gauge_3crv})
    before = y3crv.balanceOf(user)
    lp_3crv.approve(zap_3crv, 2 ** 256 - 1, {"from": user})
    zap_3crv.zap({"from": user})
    assert y3crv.balanceOf(user) > before
    assert lp_3crv.balanceOf(user) == 0
    assert lp_3crv.balanceOf(zap_3crv) == 0
    assert y3crv.balanceOf(zap_3crv) == 0
