def test_backzapper(backzapper, user, crv, vesting, vault, minter, gauges):
    before = vault.balanceOf(user)
    assert vesting.balanceOf(user) > 0
    minter.toggle_approve_mint(backzapper.address, {"from": user})
    crv.approve(backzapper, 2 ** 256 - 1, {"from": user})
    backzapper.zap(gauges, {"from": user})
    assert vault.balanceOf(user) > before
    assert crv.balanceOf(user) == 0
    assert vesting.balanceOf(user) == 0
    assert crv.balanceOf(backzapper) == 0


def test_3crv_zapper(three_crv_zapper, user, three_crv, three_crv_vault, vault):
    claimable = vault.claimable(user)
    assert claimable > 0
    three_crv.approve(backzapper, 2 ** 256 - 1, {"from": user})
    three_crv_zapper.zap({"from": user})
    assert three_crv.balanceOf(user) == 0
    assert three_crv.balanceOf(three_crv_zapper) == 0
    assert three_crv_vault.balanceOf(user) > 0
    assert three_crv_vault.balance(three_crv_zapper) == 0
    assert vault.claimable(user) == 0