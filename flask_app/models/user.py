from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import note, post, case
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#define global reg expressions for data validation
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$')
class User:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.notes = {}
        self.posts = {}
        self.cases = {}
        self.friends = {}
        self.requests = {}
        self.requesteds = {}
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO users ( first_name, last_name, email, password_hash ) VALUES \
            ( %(first_name)s, %(last_name)s, %(email)s, %(password_hash)s );"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_all( cls ):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_user_by_id( cls, data ):
        query = "SELECT * FROM users LEFT JOIN notes on users.id = notes.user_id \
            WHERE users.id=%(id)s ORDER BY notes.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        return users

    @classmethod
    def get_user_with_notes_by_id( cls, data ):
        query = "SELECT * FROM users LEFT JOIN notes on users.id = notes.user_id \
            WHERE users.id=%(id)s ORDER BY notes.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        # get notes first
        for row in results:
            if row["notes.id"] != None:
                note_data = {
                    "id": row["notes.id"],
                    "user_id": row["id"],
                    "excerpt": row["excerpt"],
                    "url": row["url"],
                    "url_pointer": row["url_pointer"],
                    "thought": row["thought"],
                    "created_at": row["notes.created_at"],
                    "updated_at": row["notes.updated_at"]
                }
                users.notes[row["notes.id"]] = note.Note(note_data)
        # then separate query to get posts
        query = "SELECT posts.* FROM users JOIN posts on users.id = posts.user_id \
            WHERE users.id=%(id)s ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.posts[row["id"]] = post.Post(row)
        # and another query to get library items
        query = "SELECT cases.* FROM libraries JOIN cases ON libraries.case_id \
            = cases.id WHERE libraries.user_id = %(id)s ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.cases[row["id"]] = case.Case(row)
        return users
    
    @classmethod
    def get_user_with_friends_by_id( cls, data ):
        query = "SELECT users.*, users2.* FROM users LEFT JOIN friends on users.id = friends.user_id \
            LEFT JOIN users users2 on friends.friend_id = users2.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        for row in results:
            if row["users2.id"] != None:
                friend_data = {
                    "id": row["users2.id"],
                    "first_name": row["users2.first_name"],
                    "last_name": row["users2.last_name"],
                    "email": row["users2.email"],
                    "password_hash": row["users2.password_hash"],
                    "created_at": row["users2.created_at"],
                    "updated_at": row["users2.updated_at"]
                }
                users.friends[row["users2.id"]] = cls( friend_data )
        # then separate query for requests (others --request--> active user)
        query = "SELECT users.* FROM requests JOIN users on requests.request_id = users.id \
            WHERE requests.user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.requests[row["id"]] = cls( row )
        # and another query to get all requesteds (active user --requested--> others)
        query = "SELECT users.* FROM requests JOIN users on requests.user_id = users.id \
            WHERE requests.request_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.requesteds[row["id"]] = cls( row )
        return users
    
    @classmethod
    def get_user_with_library_by_id( cls, data ):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        query = "SELECT cases.* FROM libraries JOIN cases on libraries.case_id = cases.id \
            WHERE libraries.user_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.cases[row["id"]] = case.Case( row )
        return users

    @classmethod
    def get_user_with_viewable_posts_by_id( cls, data ):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        query = "SELECT * FROM posts JOIN users on posts.user_id = users.id \
            WHERE posts.user_id=%(id)s OR posts.user_id IN (SELECT friends.friend_id \
            FROM friends WHERE friends.user_id = %(id)s ) ORDER BY posts.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            post_data = {
                "id": row["id"],
                "user_id": row["user_id"],
                "excerpt": row["excerpt"],
                "url": row["url"],
                "url_pointer": row["url_pointer"],
                "thought": row["thought"],
                "note_created_at": row["note_created_at"],
                "note_updated_at": row["note_updated_at"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            users.posts[row["id"]] = post.Post( post_data )
            post_user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password_hash": row["password_hash"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            users.posts[row["id"]].users.append(User( post_user_data ))
        return users




    @classmethod
    def get_user_by_email( cls, data ):
        query = "SELECT * FROM users WHERE users.email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        users = False
        if len(results) > 0:
            users = cls(results[0])
        return users

    @staticmethod
    def validate_user_form(data):
        is_valid = True
        # name validations, must be at least 3 characters
        if len(data["first_name"]) < 3:
            flash("first name must be at least 3 characters long", "register")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("last name must be at least 3 characters long", "register")
            is_valid = False
        # email field must be present
        if len(data["email"]) < 1:
            flash("must enter valid email", "register")
            is_valid = False
        # must match reg expression
        elif not email_regex.match(data['email']):
            is_valid = False
            flash("must enter valid email", "register")
        # confirm it doesn't already exist in db
        elif User.get_user_by_email(data):
            flash("account already exists for this email", "register")
            is_valid = False
        # password validations, password must be 8 characters
        if len(data["password"]) < 8:
            is_valid = False
            flash("password must be at least 8 characters", "register")
        elif not password_regex.match(data['password']):
            is_valid = False
            flash("must enter valid password", "register")
        elif len(data["password_confirm"]) < 8:
            is_valid = False
            flash("passwords and confirmation do not match", "register")
        elif not password_regex.match(data['password_confirm']):
            is_valid = False
            flash("passwords and confirmation do not match", "register")
        # password and confirmation must match
        elif data['password'] != data['password_confirm']:
            is_valid = False
            flash("passwords and confirmation do not match", "register")
        return is_valid

    @staticmethod
    def hash_password(data):
        password_hash = bcrypt.generate_password_hash(data['password'])
        return password_hash
    @staticmethod
    def validate_login_form(data):
        if not email_regex.match(data['email']):
            flash("email and password combination did not match", "login")
            return False
        if len(data["password"]) < 8:
            flash("email and password combination did not match", "login")
            return False
        elif not password_regex.match(data['password']):
            flash("email and password combination did not match", "login")
            return False
        return True
    
    @staticmethod
    def verify_login_credentials( data ):
        users = User.get_user_by_email(data)
        if not users:
            flash("email and password combination did not match", "login")
            return False
        elif not bcrypt.check_password_hash(users.password_hash, data["password"]):
            flash("email and password combination did not match", "login")
            return False
        return users.id