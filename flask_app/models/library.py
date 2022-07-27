from flask_app.config.mysqlconnection import connectToMySQL


class Library:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.case_id = data['case_id']
        self.progress = data['progress']
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO libraries ( user_id, case_id) \
            VALUES ( %(user_id)s, %(case_id)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def delete_from_library_by_case_id( cls, data ):
        query = "DELETE FROM libraries WHERE user_id = %(user_id)s \
            AND case_id = %(case_id)s;"
        return connectToMySQL(cls.db).query_db( query, data )