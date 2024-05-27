import json, os, random
from flask import Flask, request, jsonify, send_file
from make_prediction import make_prediction

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

@app.route('/')
def home():
    return "Hello! You've reached to the API for Music Recommendation System."

@app.route("/list_tracks")
def list_tracks():
    with open('tracks.json', 'r') as file:
        tracks = json.load(file)
    return jsonify(tracks)

@app.route("/get_track/<string:filename>")
def get_track(filename):
    if os.path.exists(f'Data/wav/{filename}'):
        return send_file(f'Data/wav/{filename}', as_attachment=False)
    else:
        return "Error."

@app.route("/find_matches", methods=["POST"])
def process_tracks():
    tracks = request.json
    return jsonify(make_prediction(tracks))

if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
