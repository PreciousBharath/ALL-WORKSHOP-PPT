import '@nomicfoundation/hardhat-toolbox';
import 'dotenv/config';

export default {
  solidity: '0.8.24',
  networks: {
    hardhat: {},
    localhost: {
      url: process.env.HARDHAT_RPC_URL || 'http://127.0.0.1:8545',
      chainId: 31337
    }
  }
};
