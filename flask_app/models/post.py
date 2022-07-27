from flask_app.config.mysqlconnection import connectToMySQL


class Post:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.excerpt = data['excerpt']
        self.url = data['url']
        self.url_pointer = data['url_pointer']
        self.thought = data['thought']
        self.note_created_at = data['note_created_at']
        self.note_updated_at = data['note_updated_at']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO posts ( user_id, excerpt, url, url_pointer, thought, note_created_at, note_updated_at ) \
            VALUES (%(user_id)s, %(excerpt)s, %(url)s, %(url_pointer)s, %(thought)s, %(note_created_at)s, %(note_updated_at)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    @classmethod
    def get_post_by_id( cls, data ):
        query = "SELECT * FROM posts WHERE id=%(id)s;"
        results = results = connectToMySQL(cls.db).query_db( query, data )
        notes = False
        if len(results) > 0:
            notes = cls(results[0])
        return notes
    @classmethod
    def delete_post_by_id( cls, data ):
        query = "DELETE FROM posts WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @staticmethod
    def validate_post_retraction( data ):
        is_valid = True
        
        return is_valid