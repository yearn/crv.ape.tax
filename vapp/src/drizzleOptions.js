import ERC20 from './abi/ERC20.json'
import veCurveVault from './abi/veCurveVault.json'
import CurveVotingEscrow from './abi/CurveVotingEscrow.json'
import CurveVesting from './abi/CurveVesting.json'
import CurveYCRVVoter from './abi/CurveYCRVVoter.json'
import StrategyProxy from './abi/StrategyProxy.json'
import CurveBackzapper from './abi/CurveBackzapper.json'
import y3CrvZapper from './abi/y3CrvZapper.json'
import CurveRegistry from './abi/CurveRegistry.json'
import CurveMinter from './abi/CurveMinter.json'

import Web3 from 'web3'
let web3 = new Web3(Web3.givenProvider);

const options = {
  web3: {
    block: false,
  },
  syncAlways: true,
  contracts: [
    {
      contractName: 'veCurveVault',
      web3Contract: new web3.eth.Contract(veCurveVault, "0xc5bDdf9843308380375a611c18B50Fb9341f502A")
    },
    {
      contractName: 'CRV',
      web3Contract: new web3.eth.Contract(ERC20, "0xD533a949740bb3306d119CC777fa900bA034cd52")
    },
    {
      contractName: '3CRV',
      web3Contract: new web3.eth.Contract(ERC20, "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490")
    },
    {
      contractName: 'CurveVotingEscrow',
      web3Contract: new web3.eth.Contract(CurveVotingEscrow, "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2")
    },
    {
      contractName: 'CurveVesting',
      web3Contract: new web3.eth.Contract(CurveVesting, "0x575CCD8e2D300e2377B43478339E364000318E2c")
    },
    {
      contractName: 'StrategyProxy',
      web3Contract: new web3.eth.Contract(StrategyProxy, "0x7A1848e7847F3f5FfB4d8e63BdB9569db535A4f0")
    },
    {
      contractName: 'CurveYCRVVoter',
      web3Contract: new web3.eth.Contract(CurveYCRVVoter, "0xF147b8125d2ef93FB6965Db97D6746952a133934")
    },
    {
      contractName: 'CurveBackzapper',
      web3Contract: new web3.eth.Contract(CurveBackzapper, "0x5249dD8DB02EeFB08600C4A70110B0f6B9CDA3cA")
    },
    {
      contractName: 'y3CrvZapper',
      web3Contract: new web3.eth.Contract(y3CrvZapper, "0xc8Bd224A588cd2485EAeCc3a7b3d168A5d0217D8")
    },
    {
      contractName: 'CurveRegistry',
      web3Contract: new web3.eth.Contract(CurveRegistry, "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c")
    },
    {
      contractName: 'CurveMinter',
      web3Contract: new web3.eth.Contract(CurveMinter, "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")
    },
  ],
  events: {
  },
  polls: {
    accounts: 15000
  }
}

export default options
