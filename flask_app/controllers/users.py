from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/library')
    return render_template("index.html")

@app.route('/user_register/', methods=["POST"])
def register_new_user():
    if not user.User.validate_user_form(request.form):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect('/')
    
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

    return redirect('/library')


@app.route('/landing_page/')
def landing_page():
    if 'user_id' not in session:
        return redirect('/')
    if 'other_user_excerpt' in session:
        session.pop('other_user_excerpt')
    users = user.User.get_user_by_id( {"id": session["user_id"]})
    return render_template("landingpage.html", users=users)


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