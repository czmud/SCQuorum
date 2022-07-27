from flask_app.config.mysqlconnection import connectToMySQL

class Request:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.request_id = data['request_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO requests ( user_id, request_id ) \
            VALUES ( %(user_id)s, %(request_id)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def delete_request_by_user_id( cls, data ):
        query = "DELETE FROM requests WHERE user_id = %(user_id)s \
            and request_id = %(request_id)s"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def has_requested_to_be_friends( cls, data ):
        query = "SELECT * FROM requests WHERE user_id = %(user_id)s \
            AND request_id = %(request_id)s;"
        results = connectToMySQL(cls.db).query_db( query, data )
        if len(results) > 0:
            return True
        return False