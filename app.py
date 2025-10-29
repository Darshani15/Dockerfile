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


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# In-memory order storage (sample default orders)
orders = [
    {"id": 1, "items": ["Margherita Pizza", "Garlic Bread"], "status": "Paid"},
    {"id": 2, "items": ["Veg Burger", "French Fries"], "status": "Pending"},
    {"id": 3, "items": ["Chocolate Cake", "Cappuccino"], "status": "Pending"}
]

# GET all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

# POST create order → return full orders list
@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or "items" not in data:
            return jsonify({"error": "Invalid request data"}), 400

        order_id = len(orders) + 1
        new_order = {"id": order_id, "items": data["items"], "status": "Pending"}
        orders.append(new_order)

        # Return full orders list
        return jsonify(orders), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST pay for an order → return full orders list
@app.route('/orders/<int:order_id>/pay', methods=['POST'])
def pay_order(order_id):
    try:
        order = next((o for o in orders if o["id"] == order_id), None)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Call payment service
        payment_url = "http://payment_service:5003/pay"
        payment_response = requests.post(payment_url, json={"order_id": order_id})

        if payment_response.status_code == 200:
            order["status"] = "Paid"
            # Return full updated orders list
            return jsonify(orders), 200
        else:
            return jsonify({"message": "Payment failed", "details": payment_response.text}), 400

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Payment service not reachable"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)



from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/pay', methods=['POST', 'GET'])
def pay():
    """
    Payment endpoint.
    GET → for testing in browser, returns a message.
    POST → expects JSON payload {"order_id": <id>} and returns success message.
    """
    if request.method == 'GET':
        return "Payment endpoint. Use POST with JSON payload: {\"order_id\": <id>}", 200

    # POST request handling
    data = request.get_json()
    if not data or "order_id" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    order_id = data["order_id"]
    
    # Simulate payment logic (always success for demo)
    return jsonify({"message": f"Payment received for order {order_id}"}), 200


if __name__ == '__main__':
    # 0.0.0.0 allows access from other Docker containers
    app.run(host='0.0.0.0', port=5003)


