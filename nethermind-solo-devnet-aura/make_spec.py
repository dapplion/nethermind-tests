#!/usr/bin/python

import sys
import inspect
from web3.auto import w3
from eth_abi import encode_abi


# TODO: Generate accounts from mnemonic
w3.eth.account.enable_unaudited_hdwallet_features()

# TODO: For test
# address: 0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541
# privKey: 81ca4772bbf26b62ce49f539ba603bab170f2a6fbc2661c7446c656eabcb6400


# To be changed arguments ##
############################
ownerAddress = "0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"
miningAddresses = ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
stakingAddresses = ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
firstValidatorIsUnremovable = True
delegatorMinStake = w3.toWei(1000, 'ether')
candidateMinStake = w3.toWei(20000, 'ether')
stakingEpochDuration = 76
stakingEpochStartBlock = 0
stakeWithdrawDisallowPeriod = 10
collectRoundLength = 38
############################


# Fixed arguments ##########
############################
VALIDATOR_SET_CONTRACT = "0x1000000000000000000000000000000000000001"
BLOCK_REWARD_CONTRACT = "0x2000000000000000000000000000000000000001"
RANDOM_CONTRACT = "0x3000000000000000000000000000000000000001"
STAKING_CONTRACT = "0x1100000000000000000000000000000000000001"
PERMISSION_CONTRACT = "0x4000000000000000000000000000000000000001"
CERTIFIER_CONTRACT = "0x5000000000000000000000000000000000000001"
GOVERNANCE_CONTRACT = "0x6100000000000000000000000000000000000001"
############################


SOURCE_SPEC_FILEPATH = sys.argv[1]
OUT_SPEC_FILEPATH = sys.argv[2]

source_spec_file = open(SOURCE_SPEC_FILEPATH, mode="r")
source_spec_str = source_spec_file.read()
source_spec_file.close()

# Replace owner
ownerAddressNoPrefix = ownerAddress.replace("0x", "")
source_spec_str = source_spec_str.replace(
  "{{OWNER_ADDRESS}}",
  ownerAddressNoPrefix
)

# Replace InitializerAuRa constructor arguments
# constructor(
#   address[] memory _contracts,
#   address _owner,
#   address[] memory _miningAddresses,
#   address[] memory _stakingAddresses,
#   bool _firstValidatorIsUnremovable,
#   uint256 _delegatorMinStake,
#   uint256 _candidateMinStake,
#   uint256 _stakingEpochDuration,
#   uint256 _stakingEpochStartBlock,
#   uint256 _stakeWithdrawDisallowPeriod,
#   uint256 _collectRoundLength
# )
InitializerAuRaConstructorAbi = [
  "address[]", # memory _contracts
  "address", # _owner
  "address[]", # memory _miningAddresses
  "address[]", # memory _stakingAddresses
  "bool", # _firstValidatorIsUnremovable
  "uint256", # _delegatorMinStake
  "uint256", # _candidateMinStake
  "uint256", # _stakingEpochDuration
  "uint256", # _stakingEpochStartBlock
  "uint256", # _stakeWithdrawDisallowPeriod
  "uint256", # _collectRoundLength
]
InitializerAuRaConstructorArgs = [
  [
    VALIDATOR_SET_CONTRACT,
    BLOCK_REWARD_CONTRACT,
    RANDOM_CONTRACT,
    STAKING_CONTRACT,
    PERMISSION_CONTRACT,
    CERTIFIER_CONTRACT,
    GOVERNANCE_CONTRACT
  ],
  ownerAddress,
  miningAddresses,
  stakingAddresses,
  firstValidatorIsUnremovable,
  delegatorMinStake,
  candidateMinStake,
  stakingEpochDuration,
  stakingEpochStartBlock,
  stakeWithdrawDisallowPeriod,
  collectRoundLength
]

source_spec_str = source_spec_str.replace(
  "{{INITIALIZER_AURA_CONSTRUCTOR_ARGS_ENCODED}}",
  w3.toHex(encode_abi(InitializerAuRaConstructorAbi, InitializerAuRaConstructorArgs))
)

out_spec_file = open(OUT_SPEC_FILEPATH, "w")
out_spec_file.write(source_spec_str)
out_spec_file.close()
