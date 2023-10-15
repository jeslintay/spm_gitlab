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

class Listing(db.Model):
    __tablename__ = 'role_listing'

    role_name = db.Column(db.String(20), primary_key=True)
    role_descr = db.Column(db.String(200))
    skills_required = db.Column(db.String(200))
    role_deadline = db.Column(db.Date)

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


@app.route("/view_role_listings")
def view_role_listings():
    try:
        # vrl_list = db.session.query(Listing).all()
        vrl_list = db.session.execute(db.select(Listing)).scalars()
        # print(vrl_list)
        return jsonify(
            {
                "data": [listing.to_dict()
                        for listing in vrl_list]
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
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

