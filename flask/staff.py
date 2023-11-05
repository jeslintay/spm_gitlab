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


class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50))
    Staff_LName = db.Column(db.String(50))
    Dept = db.Column(db.String(50))
    Country = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Access_Right = db.Column(db.Integer)

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

    def json(self):
        return {"Staff_ID": self.Staff_ID, "Staff_FName": self.Staff_FName, "Staff_LName": self.Staff_LName, "Dept": self.Dept,"Country": self.Country,"Email": self.Email,"Access_Right": self.Access_Right}



@app.route("/view_staffs/<int:staff_id>")
def view_applications(staff_id):
    try:
        staff_list = db.session.execute(db.select(Staff).filter_by(Staff_ID=staff_id)).scalars()
        print(staff_list)
        return jsonify(
            {
                "data": [listing.to_dict()
                        for listing in staff_list]
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
# holds values of selected roles    
# @app.route("/role", methods=['POST'])
# def role():
#     data = request.get_json()
#     print(data)
#     print(data["record"])
#     testDict = data["record"]
#     if not all (key in testDict for 
#                 key in('role_name','role_descr',
#                 'skills_required','role_deadline')):
#         return jsonify({
#             "message": "Incorrect JSON object provided."
#         }), 500
#     role = Listing(**testDict)
#     try:
#         return jsonify(role.to_dict()), 201
#     except Exception:
#         return jsonify({
#             "message": "Unable to commit to database."
#         }), 500

if __name__ == '__main__':
    app.run(debug=True,port=5200)

