from flask import Blueprint, request, jsonify
from services.chatbot_handler import handle_crime_query

bp = Blueprint("prediction_routes", __name__, url_prefix="/predict_crimes")

@bp.route("", methods=["POST"])
def predict_crime():
    data = request.get_json()
    user_input = data.get("user_input", "")
    print("\n----- Debug: /predict_crimes called -----")
    print("Received user_input:", user_input)

    result = handle_crime_query(user_input)
    print("Result from handle_crime_query:", result)

    return jsonify(result)
