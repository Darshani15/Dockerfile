from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    menu = [
        {"id": 1, "name": "Margherita Pizza", "price": 299},
        {"id": 2, "name": "Veg Burger", "price": 149},
        {"id": 3, "name": "Pasta Alfredo", "price": 199}
    ]
    return jsonify(menu)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
