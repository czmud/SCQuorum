from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import note, post

@app.route('/new_note/')
def draft_new_note():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("notenew.html")


@app.route('/save_note/', methods=["POST"])
def save_new_note():
    if not note.Note.validate_note(request.form):
        session["excerpt"] = request.form["excerpt"]
        session["url"] = request.form["url"]
        session["thought"] = request.form["thought"]
        return redirect('/new_note')
    
    data = {
        "user_id": session["user_id"],
        "excerpt": request.form["excerpt"],
        "url": request.form["url"],
        "thought": request.form["thought"]
    }
    note.Note.save( data )
    return redirect('/library')

@app.route('/post_note/<int:note_id>/')
def note_to_post( note_id ):
    if 'user_id' not in session:
        return redirect('/')
    notes = note.Note.get_note_by_id( {"id": note_id } )

    data = {
        "user_id": notes.user_id,
        "excerpt": notes.excerpt,
        "url": notes.url,
        "url_pointer": notes.url_pointer,
        "thought": notes.thought,
        "note_created_at": notes.created_at,
        "note_updated_at": notes.updated_at
    }

    post.Post.save( data )
    note.Note.delete_note_by_id( {"id": note_id} )
    return redirect('/library')


@app.route('/retract_post/<int:post_id>')
def post_to_note( post_id ):
    if 'user_id' not in session:
        return redirect('/')
    posts = post.Post.get_post_by_id( {"id": post_id } )
    if not post.Post.validate_post_retraction( posts ):
        return redirect('/library')

    data = {
        "user_id": posts.user_id,
        "excerpt": posts.excerpt,
        "url": posts.url,
        "url_pointer": posts.url_pointer,
        "thought": posts.thought,
        "created_at": posts.note_created_at,
        "updated_at": posts.note_updated_at
    }

    note.Note.save_from_post( data )
    post.Post.delete_post_by_id( {"id": post_id} )
    return redirect('/library')