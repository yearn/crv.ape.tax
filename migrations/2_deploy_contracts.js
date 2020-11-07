const yvecrv = artifacts.require("veCurveVault");

module.exports = function(deployer) {
  deployer.deploy(yvecrv);
};
