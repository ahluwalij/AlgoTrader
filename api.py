#Initialize the exchange information
import actions

# Load evironment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
PORT = os.getenv("PORT")

# Create an API to recieve webhooks from TradingView
import flask
from flask import Flask, request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['POST'])
def handleReq():
    body = request.json
    action = body.get('action')
    interval = body.get('interval')
    authToken = body.get('auth_token')
    if authToken == AUTH_TOKEN:
        # print("Authorized!")
        if action == 'Buy':
            print(f"Longing ETH {interval}")
            actions.long()
        elif action =='Sell':
            print(f"Shorting ETH {interval}")
            actions.short()
        else:
            print("Invalid action")
    else:
        print("Unauthorized attempt!")
    return 'Webhook received'

app.run(port=PORT)
