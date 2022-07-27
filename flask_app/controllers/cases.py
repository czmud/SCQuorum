from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import case, user, library

@app.route('/archives/')
def view_all_opinions():
    if 'user_id' not in session:
        return redirect('/')
    users = user.User.get_user_by_id( {"id": session["user_id"]} )
    cases = case.Case.get_all()
    return render_template("archives.html", users=users, cases=cases)


@app.route('/cases/<int:case_id>/')
def read_case( case_id ):
    if 'user_id' not in session:
        return redirect('/')
    users = user.User.get_user_with_library_by_id( {"id": session["user_id"]} )
    cases = case.Case.get_case_by_id( {"id": case_id} )
    return render_template("caseread.html", users=users, cases=cases)

@app.route('/add_to_library/<int:case_id>/')
def add_case_to_library( case_id ):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "case_id": case_id
    }
    library.Library.save( data )
    return redirect('/cases/'+str(case_id))

@app.route('/remove_from_library/<int:case_id>/')
def remove_case_from_library( case_id ):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "case_id": case_id
    }
    library.Library.delete_from_library_by_case_id( data )
    return redirect('/cases/'+str(case_id))