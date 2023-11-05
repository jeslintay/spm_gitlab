from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# if __name__ == '__main__':
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                        'root:' + \
                                        '@localhost:3306/sbrp'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                            'pool_recycle': 280}
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Accesscontrol(db.Model):
    __tablename__ = 'Access_Control'

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_Control_Name = db.Column(db.String(20))


    def json(self):
        return {"Access_ID": self.Access_ID, "Access_Control_Name": self.Access_Control_Name}


class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50))
    Staff_LName = db.Column(db.String(50))
    Dept = db.Column(db.String(50))
    Country = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Access_Right = db.Column(db.Integer)

    def json(self):
        return {"Staff_ID": self.Staff_ID, "Staff_FName": self.Staff_FName, "Staff_LName": self.Staff_LName, "Dept": self.Dept,"Country": self.Country,"Email": self.Email,"Access_Right": self.Access_Right}

# Testing
@app.route("/")
def test():
    return "testing"



@app.route('/getAccessID/<int:staff_id>')
def getAccessID(staff_id):
    staff = Staff.query.filter_by(Staff_ID=staff_id).first().json()
    accessright = Accesscontrol.query.filter_by(Access_ID=staff['Access_Right']).first()
    if accessright:
        return jsonify(
            {
                "code": 200,
                "data": accessright.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Access not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(debug=True,port=5100)