# Zetamarkets

This project is intended to be a python SDK for `Zetamarkets` suite of tools. It is a loose port of the 
[Zetamarkets Javascript SDK](https://github.com/zetamarkets/sdk)

Please **Don't** use this project at the moment as it is a work in progress. 

## Install

`pip3 install zetamarkets`


### Setting up a wallet

```sh
# Generate new keypair at ./bot-key.json
solana-keygen new -o bot-key.json

# View new pubkey address
solana-keygen pubkey bot-key.json

# Put private key into .env file used by script
# (Make sure you are in the same directory as where you are running the script.)
echo private_key=`cat bot-key.json` >> .env
```


## TODO

- [x] Basic Setup boilerplate
- [ ] Display Exchange State
- [ ] User Margin Accounts
- [ ] Trade and View positions
- [ ] Check Market Mark Price
- [ ] Calculate User Margin Account State
- [ ] Callbacks and State tracking
- [ ] Native Polling


## Examples

Complete basic example

