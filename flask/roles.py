from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

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

class Listing(db.Model):
    __tablename__ = 'role_listing'

    role_name = db.Column(db.String(20), primary_key=True)
    role_descr = db.Column(db.String(200))
    skills_required = db.Column(db.String(200), primary_key=True)
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

class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'  
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Skill_Name = db.Column(db.String(50), primary_key=True)

class Applicants(db.Model):
    __tablename__ = 'applicants'
    app_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Staff_ID = db.Column(db.Integer,nullable=False)
    Staff_FName = db.Column(db.String(20),nullable=False)
    Staff_LName = db.Column(db.String(20),nullable=False)
    role_name = db.Column(db.String(20),nullable=False)

    def json(self):
        return {"app_ID":self.app_ID,"Staff_ID": self.Staff_ID, "Staff_FName": self.Staff_FName, "Staff_LName": self.Staff_LName,"role_name":self.role_name}

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

@app.route("/view_applicants/<string:role_name>")
def view_applicants(role_name):
    try:

        # vrl_list = db.session.query(Listing).all()
        app_list = db.session.execute(db.select(Applicants).filter_by(role_name=role_name)).scalars()

        
        return jsonify(
            {
                "data": [listing.to_dict()
                        for listing in app_list]
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500    

@app.route("/create_role_listing", methods=["POST"])
def create_role_listing():
    data=request.get_json()
    print(data)
    if not all(key in data.keys() for
               key in ('role_name','role_descr','skills_required','role_deadline')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }),500
    
    if validate_role_listing(data) == 200:
        Listings = []
        for skill in data['skills_required']:
            print(skill)
            roleListing=Listing(
                role_name=data['role_name'], role_descr=data['role_descr'],
                skills_required=skill, role_deadline= data['role_deadline'])
            Listings.append(roleListing.to_dict())
    

    # Commit to DB
        try:
            db.session.add(roleListing)
            db.session.commit()
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500
        
        return jsonify(Listings), 201
    
    else:
        return validate_role_listing(data)

def validate_role_listing(data):

    roleListing = Listing.query.filter_by(role_name=data['role_name']).first()
    if roleListing is not None:
        return jsonify({
            "message": "Role Listing already exists."
        }), 500
    
    if data['role_deadline'] == None or data['role_descr'] == "" or data['skills_required'] == "" or data['role_name'] == "":
        return jsonify({
            "message": "Input cannot be empty."
        }), 500
    
    today = datetime.today().strftime('%Y-%m-%d')
    if data['role_deadline'] < today:
        return jsonify({
            "message": "Deadline cannot be before today."
        }), 500
    
    return jsonify({
        "message": "OK"
    }), 200


@app.route("/apply_role", methods=['POST'])
def apply_role():
    data = request.get_json()
    staff_id = data['staff_id']
    role_name = data['role_name']

    # Query the staff record
    staff = Staff.query.filter_by(Staff_ID=staff_id).first()

    if staff is None:
        return jsonify({"message": "Staff not found"}), 404

    # Extract staff information
    Staff_FName = staff.Staff_FName
    Staff_LName = staff.Staff_LName

    job_app = Applicants(
        Staff_ID=staff_id, Staff_FName=Staff_FName, Staff_LName=Staff_LName, role_name=role_name
    )

    try:
        db.session.add(job_app)
        db.session.commit()
        return jsonify(job_app.to_dict()), 201
    except Exception as e:
        return jsonify({"message": "Unable to commit to database.", "error": str(e)}), 500

@app.route("/view_applications/<int:staff_id>")
def view_applications(staff_id):
    try:
        # vrl_list = db.session.query(Listing).all()
        vrl_list = db.session.execute(db.select(Applicants).filter_by(Staff_ID=staff_id)).scalars()
        # print(vrl_list)
        
        return jsonify(
            {
                "data": [listing.to_dict()
                        for listing in vrl_list]
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500


@app.route("/edit_role_listings/<string:role_name>/<string:skills_required>", methods=["PUT"])
def edit_role_listing(role_name, skills_required):
    data = request.get_json()
    
    # Assuming you have a unique combination of role_name and skills_required in your database
    roleListing = Listing.query.filter_by(role_name=role_name, skills_required=skills_required).first()

    if roleListing is None:
        return jsonify({
            "message": "Role listing not found."
        }), 404
    
    if (roleListing.role_name != data['role_name']):
        roleListing2 = Listing.query.filter_by(role_name=data['role_name']).first()
        if roleListing2 is not None:
            return jsonify({
                "message": "Role Listing already exists."
            }), 500
        
    if data['role_deadline'] == None or data['role_descr'] == "" or data['skills_required'] == "" or data['role_name'] == "":
        return jsonify({
            "message": "Input cannot be empty."
        }), 500
    
    today = datetime.today().strftime('%Y-%m-%d')
    if data['role_deadline'] < today:
        return jsonify({
            "message": "Deadline cannot be before today."
        }), 500

    if 'role_name' in data:
        roleListing.role_name = data['role_name']
    if 'role_descr' in data:
        roleListing.role_descr = data['role_descr']
    if 'skills_required' in data:
        roleListing.skills_required = data['skills_required']
    if 'role_deadline' in data:
        roleListing.role_deadline = data['role_deadline']

    

    # Commit to DB
    try:
        db.session.commit()
        return jsonify(roleListing.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to update role listing to database."
        }), 500

@app.route('/get_staff_skills/<int:staff_id>')
def get_staff_skills(staff_id):
    try:
        # Query the Staff_Skill table to retrieve skills for the specified Staff_ID
        staff_skills = db.session.query(Staff_Skill.Skill_Name).filter(Staff_Skill.Staff_ID == staff_id).all()
        skill_names = [skill[0] for skill in staff_skills]

        return jsonify({"skills": skill_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


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
    app.run(debug=True,port=5000)

