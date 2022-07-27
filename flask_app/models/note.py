from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Note:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.excerpt = data['excerpt']
        self.url = data['url']
        self.url_pointer = data['url_pointer']
        self.thought = data['thought']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO notes ( user_id, excerpt, url, thought ) \
            VALUES (%(user_id)s, %(excerpt)s, %(url)s, %(thought)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def save_from_post( cls, data ):
        query = "INSERT INTO notes ( user_id, excerpt, url, url_pointer, thought, \
            created_at, updated_at ) VALUES (%(user_id)s, %(excerpt)s, %(url)s, \
            %(url_pointer)s, %(thought)s, %(created_at)s, %(updated_at)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def get_note_by_id( cls, data ):
        query = "SELECT * FROM notes WHERE id=%(id)s;"
        results = results = connectToMySQL(cls.db).query_db( query, data )
        notes = False
        if len(results) > 0:
            notes = cls(results[0])
        return notes

    @classmethod
    def edit_note_by_id( cls, data ):
        query = "UPDATE notes SET excerpt=%(excerpt)s, url=%(url)s, \
            thought=%(thought)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def validate_note( cls, data ):
        is_valid = True
        return is_valid

    @classmethod
    def delete_note_by_id( cls, data ):
        query = "DELETE FROM notes WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )