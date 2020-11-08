def test_zap(zap, user, crv, vesting, vault):
    assert vesting.balanceOf(user) > 0
    before = vault.balanceOf(user)
    crv.approve(zap, 2 ** 256 - 1, {"from": user})
    zap.zap({"from": user})
    assert vault.balanceOf(user) > before
