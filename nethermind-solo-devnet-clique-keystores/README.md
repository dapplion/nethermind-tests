# Nethermind solo node clique with keystores

Configures private key for account `0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b` in

```json
 "KeyStore": {
    "BlockAuthorAccount": "0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541",
    "PasswordFiles": ["./configs/password.txt"],
    "KeyStoreDirectory": "./configs/keystores",
    "UnlockAccounts": ["0x88dFc82CF71fdeb23f82C33a202f6E2D19AC0541"]
  },
```

Then this account is listed in genesis extraData to participate in the genesis validator set.

## How to

```
docker-compose up
```
