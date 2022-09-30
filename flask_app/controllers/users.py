from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, case
import datetime

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/library')
    return render_template("index.html")

@app.route('/registration/')
def registration_form():
    if 'user_id' in session:
        return redirect('/library')
    return render_template("registration.html")

@app.route('/user_register/', methods=["POST"])
def register_new_user():
    if not user.User.validate_user_form(request.form):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect('/registration')
    
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password_hash": user.User.hash_password(request.form)
    }
    session.clear()
    session["user_id"] = user.User.save(data)
    return redirect('/landing_page')

@app.route('/user_login/', methods=["POST"])
def log_user_in():
    if not user.User.validate_login_form(request.form):
        session["email_login"] = request.form["email"]
        return redirect('/')
    
    session["user_id"] = user.User.verify_login_credentials(request.form)
    if not session["user_id"]:
        session["email_login"] = request.form["email"]
        session.pop("user_id")
    if request.form["email"] == 'guestaccount@mail.com':
        return redirect('/landing_page')
    return redirect('/library')

@app.route('/landing_page/')
def landing_page():
    if 'user_id' not in session:
        return redirect('/')
    if 'other_user_excerpt' in session:
        session.pop('other_user_excerpt')
    users = user.User.get_user_by_id( {"id": session["user_id"]})
    example_library = user.User.get_user_with_notes_by_id( {"id": 15} )
    example_library.posts[40].created_at = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=2, minutes=27)
    cases = case.Case.get_all()
    example_friends = user.User.get_user_with_friends_by_id( {"id": 15} )
    all_users = user.User.get_all()
    example_quorum = user.User.get_user_with_viewable_posts_by_id( {"id": 15} )
    return render_template("landingpage.html", users=users, example_library=example_library, cases=cases, example_friends=example_friends, all_users=all_users, example_quorum=example_quorum)

@app.route('/library/')
def library():
    if 'user_id' not in session:
        return redirect('/')
    if 'other_user_excerpt' in session:
        session.pop('other_user_excerpt')
    users = user.User.get_user_with_notes_by_id( {"id": session["user_id"]})
    
    return render_template("library.html", users=users)

@app.route('/user_logout/')
def log_user_out():
    session.clear()
    return redirect('/')