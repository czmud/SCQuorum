from flask_app import app
from flask import jsonify, request
from flask_app.models import user

@app.route('/api/friends/<int:user_id>/<search_text>')
def get_friends_by_user(user_id, search_text):
    users = user.User.get_five_by_search({"user_id": user_id, "search_text": search_text+"%%" })
    return jsonify(message=users)

