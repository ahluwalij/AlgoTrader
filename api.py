# Load evironment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Create an API to recieve webhooks from TradingView
import flask
from flask import Flask, request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST'])
def handleReq():
    body = request.json
    action = body.get('action')
    interval = body.get('interval')
    authToken = body.get('auth_token')
    if authToken == AUTH_TOKEN:
        print("Authorized!")
        if action == 'buy':
            print(f"Buying ETH {interval}")
        elif action =='sell':
            print(f"Selling ETH {interval}")
        else:
            print("Invalid action")
    return 'Webhook received'

app.run()
