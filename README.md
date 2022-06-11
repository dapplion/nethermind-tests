# nethermind-tests

## FAQ:

#### clique - Why so many accounts have 1 wei?

Clique genesis JSON files Allocate 1 wei to all possible pre-compiles. See https://github.com/ethereum/EIPs/issues/716 "SpuriousDragon RIPEMD bug"

E.g. Rinkeby allocates it like this. See https://github.com/ethereum/go-ethereum/blob/092856267067dd78b527a773f5b240d5c9f5693a/core/genesis.go#L370

#### clique - How is genesis extra data computed?

```py
  signers = ''.join(str(i) for i in signerAddresses)
  out["genesis"]["extraData"] = ''.join(["0x", "0" * 64, signers, "0" *130])
```

From https://github.com/skylenet/ethereum-genesis-generator/blob/42765fcb31c605a01e7ba1e40c5b0590fd47e6eb/apps/el-gen/genesis_chainspec.py#L120

#### How to configure keys

**KeyStore.TestNodeKey**

Set to the 0x prefixed secret key of the validator to unlock and produce blocks with

Example in `nethermind-solo-devnet-clique`

pubkey: 0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541
privkey: 0x81ca4772bbf26b62ce49f539ba603bab170f2a6fbc2661c7446c656eabcb6400
password: testtest

```json
  "KeyStore": {
    "TestNodeKey": "0x81ca4772bbf26b62ce49f539ba603bab170f2a6fbc2661c7446c656eabcb6400"
  },
```

```json
 "KeyStore": {
    "BlockAuthorAccount": "0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541",
    "PasswordFiles": ["./configs/password.txt"],
    "KeyStoreDirectory": "./configs/keystores",
    "UnlockAccounts": ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
  },
```
