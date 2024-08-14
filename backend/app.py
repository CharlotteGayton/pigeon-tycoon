from flask import Flask, jsonify, request
import json 
from flask_cors import CORS
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)
db = Database('pigeon_tycoon.db')
db.connect()
db.create_tables()
db.close()

def initialize_pigeons():
    db = Database('pigeon_tycoon.db')
    db.connect()
    for i in range(5):
        periodically_add_pigeon()
    db.close()

def initialize_finances():
    db = Database('pigeon_tycoon.db')
    db.connect()
    existing_finances = db.fetch_query('SELECT * FROM finances')
    if not existing_finances:
        db.execute_query('INSERT INTO finances (income, balance) VALUES (?, ?)', (0.001, 0))
    db.close()

def periodically_add_pigeon():
    db = Database('pigeon_tycoon.db')
    db.connect()
    pigeons_in_store = db.fetch_query('SELECT COUNT(*) FROM pigeon_store')[0][0]
    print(pigeons_in_store)
    if pigeons_in_store < 5:
        db.create_pigeon_for_sale()
    db.close()

def update_balance():
    db = Database('pigeon_tycoon.db')
    db.connect()
    db.update_balance()
    db.close()

# Setup a scheduler to add pigeons periodically
scheduler = BackgroundScheduler()
scheduler.add_job(func=periodically_add_pigeon, trigger="interval", minutes=1)
scheduler.add_job(func=update_balance, trigger="interval", seconds=1)
scheduler.start()

with app.app_context():
    initialize_pigeons()
    initialize_finances()

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
    db = Database('pigeon_tycoon.db')
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
    
@app.route('/api/get-pigeons-for-sale', methods=['GET', 'POST'])
def get_pigeons_for_sale():
    db = Database('pigeon_tycoon.db')
    db.connect()
    pigeons = db.get_pigeons_for_sale()
    print(pigeons)
    db.close()
    pigeon_list = [{'id': row[0], 'name': row[1], 'speed': row[2], 'stamina': row[3]} for row in pigeons]
    print(pigeon_list)
    return jsonify(pigeon_list)

@app.route('/api/get-pigeons', methods=['GET'])
def get_pigeons():
    db = Database('pigeon_tycoon.db')
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

@app.route('/api/get-balance', methods=['GET'])
def get_balance():
    db = Database('pigeon_tycoon.db')
    db.connect()
    balance = db.get_balance()
    db.close()
    return jsonify({'balance': balance[0][0]})

if __name__ == '__main__':
    app.run(debug=True)