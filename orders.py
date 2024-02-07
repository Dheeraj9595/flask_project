from db import db
from pydantic import BaseModel
from db import User, Order
from flask import Blueprint, request, abort, jsonify

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


class OrderCreate(BaseModel):
    user_id: int
    order_name: str
    order_quantity: int


@orders_bp.route('/place-order/', methods=['POST'])
def place_order():
    order_data = OrderCreate(**request.json)
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        if not user:
            # Raise a 404 Not Found error
            abort(404, description="User not found")
    new_order = Order(name=order_data.order_name, quantity=order_data.order_quantity)
    user.orders.append(new_order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()

    return jsonify({"message": "Order placed successfully"})


def serialize_orders(order):
    return {"id": order.id, "order name": order.name, "order quantity": order.quantity}


@orders_bp.route('/all-orders/', methods=['GET'])
def get_orders():
    orders = db.query(Order).all()
    serialized_orders = [serialize_orders(order) for order in orders]
    return jsonify({"orders": serialized_orders})


@orders_bp.route('/update-order/<order_id>/', methods=['PATCH'])
def update_order(order_id: int):
    update_order_data = request.json
    order = db.query(Order).filter(Order.id == order_id).first()
    # CHECK USER EXISTING
    if order:
        # update user object with new data
        for key, value in update_order_data.items():
            setattr(order, key, value)
        db.commit()
        return jsonify({"message": f"User with ID {order_id} updated successfully"})
    else:
        return jsonify({"message": f"User with ID {order_id} not found"})


@orders_bp.route('/delete-order/<order_id>/', methods=['DELETE'])
def delete_order(order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    db.delete(order)
    db.commit()
    db.close()
    return {"message": "Order deleted successfully....!!!"}
