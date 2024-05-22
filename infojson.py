import json

from flask import Flask, jsonify

def extract ():
    with open('global.json') as f:
        dab_in = json.load(f)
        return jsonify(dab_in)

