from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import post, user

@app.route('/quorum/')
def view_quorum():
    if 'user_id' not in session:
        return redirect('/')
    users = user.User.get_user_with_viewable_posts_by_id( {"id": session["user_id"]} )
    
    data = {
        "created_at": users.posts[1].created_at
    }
    print(post.Post.time_left_until_post( data ))
    print(77)
    # if post.Post.time_left_until_post( data ):
    #     return redirect('/library')
    return render_template("quorum.html", users=users)