from flask import Flask, jsonify, request
import json 
from flask_cors import CORS
from database import Database

app = Flask(__name__)
CORS(app)
db = Database('pigeon_tycoon.db')
db.connect()
db.create_tables()
db.add_pigeon('Pigeon 1', 10, 5)
db.close()

@app.route('/api/game-data', methods=['GET'])
def get_game_data():
    game_data = {
        "pigeons": [
            {"name": "Pigeon 1", "speed": 10, "stamina": 5},
            {"name": "Pigeon 2", "speed": 15, "stamina": 3},
            {"name": "Pigeon 3", "speed": 20, "stamina": 2}
        ]
    }
    return jsonify(game_data)

@app.route('/api/add-pigeon', methods=['GET', 'POST'])
def add_pigeon():
    data = request.json
    name = data.get('name')
    speed = data.get('speed')
    stamina = data.get('stamina')
    db.connect()
    if db.add_pigeon(name, speed, stamina):
        db.close()
        return jsonify({'status': 'success'}), 201
    else:
        db.close()
        return jsonify({'error': 'Pigeon with this name already exists'}), 400
    


@app.route('/api/get-pigeons', methods=['GET'])
def get_pigeons():
    db.connect()
    pigeons = db.get_pigeons()
    db.close()
    pigeon_list = [{'id': row[0], 'name': row[1], 'speed': row[2], 'stamina': row[3]} for row in pigeons]
    return jsonify(pigeon_list)

@app.route('/api/game-data', methods=['POST'])
def post_game_data():
    game_data = request.json
    with open('game_data.json', 'w') as save_file:
        json.dump(game_data, save_file)
    return jsonify(game_data)

if __name__ == '__main__':
    app.run(debug=True)