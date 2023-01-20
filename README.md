# Description

This AlgoTrader will purchase short or long contracts based on famous algorithms or your own algorithm.
The exchange used in this specific code is [Phemex](https://phemex.com/) but since we are using [ccxt](https://github.com/ccxt/ccxt),
there is support for every exchange that ccxt supports like [Binance](https://www.binance.com/en), [ByBit](https://www.bybit.com/en-US/), [Coinbase](https://www.coinbase.com/), and many others.

# Usage and Setup

## Bot Configuration

```
An example config file is avaliable for each algorithm in it's respective folder if you decide to use them.
If you are using your own signals, then use a .env file in the parent folder. (files are highlighted below)
```
<img width="158" alt="Screen Shot 2023-01-19 at 6 56 57 PM" src="https://user-images.githubusercontent.com/65431368/213588430-04058959-b514-4e21-844d-0d7937eb0fa5.png">


## TradingView Webhook Compatability
```
In order to use your own algorithm, implement it into a TradingView Chart and place Buy and Sell alerts.

Below you can see and example of my Algo setup on TradingView:
```
<img width="1133" alt="Screen Shot 2023-01-19 at 6 47 29 PM" src="https://user-images.githubusercontent.com/65431368/213587036-26d9fc2b-4f47-471d-80ae-effe31128b8f.png">

```
Set up webhook alerts using the alert feature on your Buy and Sell Signals, like displayed below.

Make up an auth token to make sure that no one can send webhooks to your endpoint and buy and sell 
options without your permission.
```

<img width="522" alt="Screen Shot 2023-01-19 at 6 49 45 PM" src="https://user-images.githubusercontent.com/65431368/213587297-e0e68cae-b032-4bb7-b09e-1a48e610cf46.png">

## Running the Bot with TradingView

```
After ensuring that your TradingView alert setup is correct, run api.py to start your API to recieve Buy and 
Sell signals.

Example Output Below:
```
<img width="715" alt="Screen Shot 2023-01-19 at 7 04 31 PM" src="https://user-images.githubusercontent.com/65431368/213589094-4737ddf9-8551-44f9-8fcc-5bf006d2687b.png">

```
Now, if the API gets a request with the correct auth token and a string saying either "Buy" or "Sell", the bot 
will perform the respective of longing or shorting!

Example of a "Buy" request below:
```
<img width="373" alt="Screen Shot 2023-01-19 at 7 07 12 PM" src="https://user-images.githubusercontent.com/65431368/213589376-5fb5a843-209e-476d-906d-0d0d9bde15c6.png">


## Running the Bot with a preset algorithm

```
After ensuring that your config files are correct, just run the respective file of the algorithm and conditions
on your given token and long/short based on it.

Example Output of the Consolidaiton Pop Algorithm Below:
```
<img width="798" alt="Screen Shot 2023-01-19 at 7 16 23 PM" src="https://user-images.githubusercontent.com/65431368/213590352-56180b68-d509-4b82-b778-3b431e417176.png">

**Happy Trading!** :+1:
