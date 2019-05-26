import os
from web3 import Web3, HTTPProvider
from eth_abi import encode_abi, decode_abi
from flask import Flask, request, jsonify
import requests
from subprocess import check_output, CalledProcessError
from flask_cors import CORS


PRIVATE_KEY = "0x5025e86427484a9b3218d00f8680e99fb18f4a6c03b01479ebf97853c162bf58"
ADDRESS = "0x8208940DA3bDEfE1d3e4B5Ee5d4EeBf19AAe0468"

COMPANY_ADDR = "0x203D66c9b5e91C475499EE6E307F90E1BE25e501"

BASE_URL = "https://rinkeby.infura.io/v3/d3301689638b40dabad8395bf00d3945"
web3 = Web3(HTTPProvider(BASE_URL))

app = Flask(__name__)
CORS(app)


def rpc_call(data, value):
    raw_output = requests.post(
        BASE_URL,
        json={
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": COMPANY_ADDR, "data": data}, "latest"],
            "id": 12,
        },
    ).json()["result"]
    return raw_output


@app.route("/getCardInfo", methods=["GET"])
def status():
    try:
        timestamp = request.args.get("timestamp")
        hash_time = web3.soliditySha3(["uint256"], [int(timestamp, 0)])
        print(hash_time.hex())
        keycard_input = f"""
keycard-select
keycard-sign-pinless {hash_time.hex()}
"""
        data = check_output(
            ["./keycard-darwin-10.6-amd64", "shell"], input=keycard_input.encode()
        )
        for i, val in enumerate(data.decode().replace("\n", ":").split(":")):
            # print(i, val.strip())
            if i == 32:
                sig = val.strip()
            if i == 36:
                address = val.strip()
        # raw = rpc_call("0x6b7b44d7" + encode_abi(["address"], [address]).hex(), 0)
        # refine = decode_abi(["bool", "string", "uint256"], bytes.fromhex(raw[2:]))
    except:
        sig = ""
        address = ""
        # refine = (False, "", 0)

    return jsonify(
        result={
            "sig": sig,
            "address": address,
            # "whiteListed": refine[0],
            # "info": refine[1].decode(),
            # "latestClaim": refine[2],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, threaded=False, debug=True)

