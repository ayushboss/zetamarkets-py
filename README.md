# Zetamarkets

This project is intended to be a python SDK for `Zetamarkets` suite of tools. It is a loose port of the 
[Zetamarkets Javascript SDK](https://github.com/zetamarkets/sdk)

Please **Don't** use this project at the moment as it is a work in progress. 


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

## Devnet variables

| Key         |                    Value                     |
| ----------- | :------------------------------------------: |
| NETWORK_URL |        https://api.devnet.solana.com         |
| PROGRAM_ID  | BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7 |
| SERVER_URL  |         https://server.zeta.markets          |

## Mainnet variables

| Key         |                    Value                    |
| ----------- | :-----------------------------------------: |
| NETWORK_URL |     https://api.mainnet-beta.solana.com     |
| PROGRAM_ID  | ZETAxsqBRek56DhiGXrn75yj2NHU3aYUnxvHXpkf3aD |

PROGRAM_ID is subject to change based on redeployments.

## Context

Zeta is a protocol that allows the trading of undercollateralized options and futures on Solana, using the Serum DEX for its order matching. Zeta is only available on devnet with SOL as the underlying asset.

Each asset corresponds to a `ZetaGroup` account. A Zeta group contains all the respective data for its markets.

Zeta markets use a circular buffer of expirations, as the Serum markets are re-used after expiry.

| Field                 |       Value       |
| --------------------- | :---------------: |
| Expiration interval   |      1 Week       |
| Number of expiries    |         2         |
| Number of strikes     |        11         |
| Supported instruments | Call, Put, Future |

As such - there are 23 markets per expiry

- 11 calls, 11 puts, 1 future

## Install

`pip3 install zetamarkets`

## Examples

Complete basic example




## Check market mark price

This is the price that position is marked to - (This is calculated by our on chain black scholes pricing that is constantly being cranked.)

``` python
# Use the market index you wish to check.
print(exchange.get_mark_price(index));
# The fair price of this option is $8.202024.
`8.202024`;

```
