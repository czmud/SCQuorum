from flask_app import app
from flask import render_template,redirect,session
from flask_app.models import user, friend, request


@app.route('/friends/')
def display_all_friends_by_user():
    if 'user_id' not in session:
        return redirect('/')
    if 'other_user_excerpt' in session:
        session.pop('other_user_excerpt')
    users = user.User.get_user_with_friends_by_id( {"id": session["user_id"]} )
    all_users = user.User.get_all()
    return render_template("friends.html", users=users, all_users=all_users)

@app.route('/accept_friend_request/<int:request_id>')
def accept_friend_request( request_id ):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "request_id": request_id
    }
    friend.Friend.save( data )
    request.Request.delete_request_by_user_id( data )
    return redirect('/friends')


@app.route('/decline_friend_request/<int:request_id>')
def decline_friend_request( request_id ):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "request_id": request_id
    }
    request.Request.delete_request_by_user_id( data )
    return redirect('/friends')

@app.route('/send_friend_request/<int:user_id>')
def send_friend_request( user_id ):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": user_id,
        "request_id": session["user_id"]
    }
    if friend.Friend.is_friend_with_user( data ):
        return redirect( '/friends')
    if request.Request.has_requested_to_be_friends( data ):
        return redirect( '/friends')

    request.Request.save( data )
    return redirect('/friends')
