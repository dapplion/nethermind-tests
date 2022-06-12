#!/usr/bin/python

import sys
import re
from eth_abi import encode_abi
from eth_utils import to_wei, is_address


# TODO: For test
# address: 0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541
# privKey: 81ca4772bbf26b62ce49f539ba603bab170f2a6fbc2661c7446c656eabcb6400


# To be changed arguments ##
############################
ownerAddress = "0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"
miningAddresses = ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
stakingAddresses = ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
firstValidatorIsUnremovable = True
delegatorMinStake = to_wei(1000, 'ether')
candidateMinStake = to_wei(20000, 'ether')
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

# TEMPLATE ARGS
OWNER_ADDRESS_TAG = "{{OWNER_ADDRESS}}"
INITIALIZER_AURA_CONSTRUCTOR_ARGS_ENCODED_TAG = "{{INITIALIZER_AURA_CONSTRUCTOR_ARGS_ENCODED}}"


# Parse CLI args. Example:
# ```
# python make_spec.py spec-posdao-template.json configs/spec.json
# ```
SOURCE_SPEC_FILEPATH = sys.argv[1]
OUT_SPEC_FILEPATH = sys.argv[2]


# Same ar String.replace() but ensures that there have been at least 1 substitution
def ensureReplace(str_before, oldvalue, newvalue):
  str_after = str.replace(str_before, oldvalue, newvalue)
  if str_before == str_after:
    raise Exception("str.replace did not change str with tag {0}".format(oldvalue))
  return str_after


# Read source file
source_spec_file = open(SOURCE_SPEC_FILEPATH, mode="r")
source_spec_str = source_spec_file.read()
source_spec_file.close()

# Replace owner
if not is_address(ownerAddress):
  raise Exception("Invalid address for ownerAddress {0}".format(ownerAddress))

source_spec_str = ensureReplace(
  source_spec_str,
  OWNER_ADDRESS_TAG,
  ownerAddress.replace("0x", "").lower()
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

source_spec_str = ensureReplace(
  source_spec_str,
  INITIALIZER_AURA_CONSTRUCTOR_ARGS_ENCODED_TAG,
  encode_abi(InitializerAuRaConstructorAbi, InitializerAuRaConstructorArgs).hex()
)

# Ensure there are no tags left to replace
if re.match("{{.*}}", source_spec_str):
  raise Exception("Not all tags are replaced")

out_spec_file = open(OUT_SPEC_FILEPATH, "w")
out_spec_file.write(source_spec_str)
out_spec_file.close()
