from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# if __name__ == '__main__':
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                        'root:root' + \
                                        '@localhost:3306/sbrp'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class Accounts(db.Model):
    __tablename__ = 'Accounts'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(10))
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Accesscontrol(db.Model):
    __tablename__ = 'Access_Control'

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_Control_Name = db.Column(db.String(20))

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50))
    Staff_LName = db.Column(db.String(50))
    Dept = db.Column(db.String(50))
    Country = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Access_Rights = db.Column(db.Integer)
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

# Testing
@app.route('/login')
def home():
    return "Testing"



@app.route('/check_account',methods=['POST'])
def check_account():
    data = request.get_json()
    staff_id = data.get('staff_id')
    password = data.get('password')
    staff_acc = db.session.execute(
                db.select(Accounts).
                filter_by(Staff_ID=staff_id)
             ).scalar_one_or_none().to_dict()
    # staff = Accounts.query.filter_by(Staff_ID=staff_id).first()
    staff_detail = db.session.execute(
                db.select(Staff).
                filter_by(Staff_ID=staff_id)
             ).scalar_one_or_none().to_dict()
    
    accesscontrol_detail = db.session.execute(
            db.select(Accesscontrol).
            filter_by(Access_ID=staff_detail['Access_Rights'])
            ).scalar_one_or_none()
    
    if staff_acc:
        if staff_acc['Password'] == password:
            return jsonify({
                "data": accesscontrol_detail.to_dict()
            }), 200
        else:
            return jsonify({
            "message": "Password is incorrect."
        }), 404
    else:
        return jsonify({
            "message": "Staff ID not found."
        }), 404

if __name__ == '__main__':
    app.run(debug=True)