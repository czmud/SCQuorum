from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import request

class Friend:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO friends ( user_id, friend_id ) \
            VALUES ( %(user_id)s, %(request_id)s ), \
                ( %(request_id)s, %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def is_friend_with_user( cls, data ):
        query = "SELECT * FROM friends WHERE user_id = %(user_id)s \
            AND friend_id = %(request_id)s;"
        results = connectToMySQL(cls.db).query_db( query, data )
        if len(results) > 0:
            return True
        return False

