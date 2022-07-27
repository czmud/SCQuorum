from flask_app.config.mysqlconnection import connectToMySQL

class Justice:
    db = "SCQuorum_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.appointment_date = data['appointment_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'