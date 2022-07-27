from flask_app.config.mysqlconnection import connectToMySQL


class Case:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.maj_opinion_justice_id = data['maj_opinion_justice_id']
        self.title = data['title']
        self.opinion_text = data['opinion_text']
        self.url = data['url']
        self.decision_date = data['decision_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all( cls ):
        query = "SELECT * FROM cases"
        results = connectToMySQL(cls.db).query_db( query )
        cases = []
        for row in results:
            cases.append( cls(row) )
        return cases
    @classmethod
    def get_case_by_id( cls, data ):
        query = "SELECT * FROM cases WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data )
        cases = False
        if len(results) > 0:
            cases = cls(results[0])
        return cases
