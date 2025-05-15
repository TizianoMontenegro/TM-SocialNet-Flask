from config import app
from flask import request, jsonify
from models import User

@app.route("/")
def hello_world():
    try:
        users = User.query.all()
        json_users = list(map(lambda user: user.to_json(), users))
    except Exception as error:
        return jsonify({"message": str(error)}), 400
    
    return jsonify({"users": json_users})

@app.route("/signup")
def signup():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")

    if not first_name or not last_name or not email or not password:
        return (
            jsonify({"message": "You must include a first name, last name, email, and password"}), 
            400
        )

    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        return jsonify({"message": str(error)}), 400

    return jsonify({"message": "User created"}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)