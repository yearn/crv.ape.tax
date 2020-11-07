import veCurveVault from './contracts/veCurveVault.json'
import IERC20 from './contracts/IERC20.json'

import Web3 from 'web3'
let web3 = new Web3(Web3.givenProvider);

const options = {
  web3: {
    block: false,
    fallback: {
      type: 'ws',
      url: 'ws://127.0.0.1:9545'
    }
  },
  contracts: [
    {
      contractName: 'veCurveVault',
      web3Contract: new web3.eth.Contract(veCurveVault.abi, "0xc5bDdf9843308380375a611c18B50Fb9341f502A")
    },
    {
      contractName: 'CRV',
      web3Contract: new web3.eth.Contract(IERC20.abi, "0xD533a949740bb3306d119CC777fa900bA034cd52")
    },
  ],
  events: {
  },
  polls: {
    accounts: 15000
  }
}

export default options
