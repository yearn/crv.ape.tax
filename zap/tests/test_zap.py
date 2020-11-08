def test_zap(zap, user, crv, vesting, vault, minter, gauges):
    before = vault.balanceOf(user)
    assert vesting.balanceOf(user) > 0
    minter.toggle_approve_mint(zap.address, {"from": user})
    crv.approve(zap, 2 ** 256 - 1, {"from": user})
    zap.zap(gauges, {"from": user})
    assert vault.balanceOf(user) > before
    assert crv.balanceOf(user) == 0
    assert vesting.balanceOf(user) == 0
