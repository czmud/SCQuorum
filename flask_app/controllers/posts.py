from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import post, user

@app.route('/quorum/')
def view_quorum():
    if 'user_id' not in session:
        return redirect('/')
    if 'other_user_excerpt' in session:
        session.pop('other_user_excerpt')
    users = user.User.get_user_with_viewable_posts_by_id( {"id": session["user_id"]} )
    return render_template("quorum.html", users=users)