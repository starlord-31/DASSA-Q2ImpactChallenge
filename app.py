from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ensure you use a secure secret key
CORS(app)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:casper@localhost/challenge2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# Define Job model that interacts with `challenge2_table`
class Job(db.Model):
    __tablename__ = 'challenge2_table'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    record_date = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    governorate = db.Column(db.String(255))
    district = db.Column(db.String(255))
    registered = db.Column(db.String(50))
    registration_type = db.Column(db.String(255))
    business_name = db.Column(db.String(255))  # Ensure business_name is correctly used for filtering
    economic_sector = db.Column(db.String(255))
    sub_sector = db.Column(db.String(255))
    products_services = db.Column(db.Text)
    phone_number = db.Column(db.String(50))
    business_phone = db.Column(db.String(50))
    employee_count = db.Column(db.String(50))
    enterprise_size = db.Column(db.String(50))
    has_vacancies = db.Column(db.String(50))
    num_vacancies = db.Column(db.Integer)
    current_interns = db.Column(db.Integer)
    current_seasonal = db.Column(db.Integer)
    current_entry_level = db.Column(db.Integer)
    current_mid_senior = db.Column(db.Integer)
    current_senior_mgmt = db.Column(db.Integer)
    current_cust_service = db.Column(db.Integer)
    current_sales = db.Column(db.Integer)
    current_priority_it = db.Column(db.Integer)
    current_priority_marketing = db.Column(db.Integer)
    current_priority_admin = db.Column(db.Integer)
    current_priority_finance = db.Column(db.Integer)
    current_priority_logistics = db.Column(db.Integer)
    current_priority_technical = db.Column(db.Integer)
    current_priority_others = db.Column(db.Integer)
    current_other_specify = db.Column(db.Text)
    youth_employment = db.Column(db.String(50))
    future_needs = db.Column(db.Text)
    future_num_vacancies = db.Column(db.Integer)
    future_interns = db.Column(db.Integer)
    future_seasonal = db.Column(db.Integer)
    future_entry_level = db.Column(db.Integer)
    future_mid_senior = db.Column(db.Integer)
    future_senior_mgmt = db.Column(db.Integer)
    future_total = db.Column(db.Integer)
    future_cust_service = db.Column(db.Integer)
    future_sales = db.Column(db.Integer)
    future_priority_it = db.Column(db.Integer)
    future_priority_marketing = db.Column(db.Integer)
    future_priority_admin = db.Column(db.Integer)
    future_priority_finance = db.Column(db.Integer)
    future_priority_logistics = db.Column(db.Integer)
    future_priority_technical = db.Column(db.Integer)
    future_priority_others = db.Column(db.Integer)
    future_other_specify = db.Column(db.Text)

# Create tables (if not already created)
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "User already exists"}), 400

    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(username=username, password=password, role=role).first()
    if user:
        session['username'] = username
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route('/jobs', methods=['GET', 'POST'])
def handle_jobs():
    if request.method == 'POST':
        data = request.json
        try:
            new_job = Job(
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                record_date=data.get('record_date'),
                lat=data.get('lat'),
                lng=data.get('lng'),
                governorate=data.get('governorate'),
                district=data.get('district'),
                registered=data.get('registered'),
                registration_type=data.get('registration_type'),
                business_name=session.get('username'),  # Assign the username as the business_name
                economic_sector=data.get('economic_sector'),
                sub_sector=data.get('sub_sector'),
                products_services=data.get('products_services'),
                phone_number=data.get('phone_number'),
                business_phone=data.get('business_phone'),
                employee_count=data.get('employee_count'),
                enterprise_size=data.get('enterprise_size'),
                has_vacancies=data.get('has_vacancies'),
                num_vacancies=data.get('num_vacancies'),
                current_interns=data.get('current_interns'),
                current_seasonal=data.get('current_seasonal'),
                current_entry_level=data.get('current_entry_level'),
                current_mid_senior=data.get('current_mid_senior'),
                current_senior_mgmt=data.get('current_senior_mgmt'),
                current_cust_service=data.get('current_cust_service'),
                current_sales=data.get('current_sales'),
                current_priority_it=data.get('current_priority_it'),
                current_priority_marketing=data.get('current_priority_marketing'),
                current_priority_admin=data.get('current_priority_admin'),
                current_priority_finance=data.get('current_priority_finance'),
                current_priority_logistics=data.get('current_priority_logistics'),
                current_priority_technical=data.get('current_priority_technical'),
                current_priority_others=data.get('current_priority_others'),
                current_other_specify=data.get('current_other_specify'),
                youth_employment=data.get('youth_employment'),
                future_needs=data.get('future_needs'),
                future_num_vacancies=data.get('future_num_vacancies'),
                future_interns=data.get('future_interns'),
                future_seasonal=data.get('future_seasonal'),
                future_entry_level=data.get('future_entry_level'),
                future_mid_senior=data.get('future_mid_senior'),
                future_senior_mgmt=data.get('future_senior_mgmt'),
                future_total=data.get('future_total'),
                future_cust_service=data.get('future_cust_service'),
                future_sales=data.get('future_sales'),
                future_priority_it=data.get('future_priority_it'),
                future_priority_marketing=data.get('future_priority_marketing'),
                future_priority_admin=data.get('future_priority_admin'),
                future_priority_finance=data.get('future_priority_finance'),
                future_priority_logistics=data.get('future_priority_logistics'),
                future_priority_technical=data.get('future_priority_technical'),
                future_priority_others=data.get('future_priority_others'),
                future_other_specify=data.get('future_other_specify')
            )
            db.session.add(new_job)
            db.session.commit()
            return jsonify({"success": True, "message": "Job created", "job": {"id": new_job.id}}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Error creating job: {str(e)}"}), 400

    elif request.method == 'GET':
        try:
            username = session.get('username')  # Retrieve username from session

            if username:
                jobs = Job.query.filter_by(business_name=username).all()
            else:
                return jsonify({"success": False, "message": "User not authenticated"}), 401

            job_list = [{"id": job.id, "business_name": job.business_name, "lat": job.lat, "lng": job.lng} for job in jobs]
            return jsonify(job_list), 200
        except Exception as e:
            return jsonify({"success": False, "message": f"Error fetching jobs: {str(e)}"}), 500

   
@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    job = Job.query.get_or_404(job_id)

    # Ensure only the owner can update their job
    username = session.get('username')
    if not username or job.business_name != username:
        return jsonify({"success": False, "message": "Permission denied"}), 403

    # Update fields
    job.start_date = data.get('start_date', job.start_date)
    job.end_date = data.get('end_date', job.end_date)
    job.record_date = data.get('record_date', job.record_date)
    job.lat = data.get('lat', job.lat)
    job.lng = data.get('lng', job.lng)
    job.governorate = data.get('governorate', job.governorate)
    job.district = data.get('district', job.district)
    job.registered = data.get('registered', job.registered)
    job.registration_type = data.get('registration_type', job.registration_type)
    job.business_name = data.get('business_name', job.business_name)
    job.economic_sector = data.get('economic_sector', job.economic_sector)
    job.sub_sector = data.get('sub_sector', job.sub_sector)
    job.products_services = data.get('products_services', job.products_services)
    job.phone_number = data.get('phone_number', job.phone_number)
    job.business_phone = data.get('business_phone', job.business_phone)
    job.employee_count = data.get('employee_count', job.employee_count)
    job.enterprise_size = data.get('enterprise_size', job.enterprise_size)
    job.has_vacancies = data.get('has_vacancies', job.has_vacancies)
    job.num_vacancies = data.get('num_vacancies', job.num_vacancies)
    job.current_interns = data.get('current_interns', job.current_interns)
    job.current_seasonal = data.get('current_seasonal', job.current_seasonal)
    job.current_entry_level = data.get('current_entry_level', job.current_entry_level)
    job.current_mid_senior = data.get('current_mid_senior', job.current_mid_senior)
    job.current_senior_mgmt = data.get('current_senior_mgmt', job.current_senior_mgmt)
    job.current_cust_service = data.get('current_cust_service', job.current_cust_service)
    job.current_sales = data.get('current_sales', job.current_sales)
    job.current_priority_it = data.get('current_priority_it', job.current_priority_it)
    job.current_priority_marketing = data.get('current_priority_marketing', job.current_priority_marketing)
    job.current_priority_admin = data.get('current_priority_admin', job.current_priority_admin)
    job.current_priority_finance = data.get('current_priority_finance', job.current_priority_finance)
    job.current_priority_logistics = data.get('current_priority_logistics', job.current_priority_logistics)
    job.current_priority_technical = data.get('current_priority_technical', job.current_priority_technical)
    job.current_priority_others = data.get('current_priority_others', job.current_priority_others)
    job.current_other_specify = data.get('current_other_specify', job.current_other_specify)
    job.youth_employment = data.get('youth_employment', job.youth_employment)
    job.future_needs = data.get('future_needs', job.future_needs)
    job.future_num_vacancies = data.get('future_num_vacancies', job.future_num_vacancies)
    job.future_interns = data.get('future_interns', job.future_interns)
    job.future_seasonal = data.get('future_seasonal', job.future_seasonal)
    job.future_entry_level = data.get('future_entry_level', job.future_entry_level)
    job.future_mid_senior = data.get('future_mid_senior', job.future_mid_senior)
    job.future_senior_mgmt = data.get('future_senior_mgmt', job.future_senior_mgmt)
    job.future_total = data.get('future_total', job.future_total)
    job.future_cust_service = data.get('future_cust_service', job.future_cust_service)
    job.future_sales = data.get('future_sales', job.future_sales)
    job.future_priority_it = data.get('future_priority_it', job.future_priority_it)
    job.future_priority_marketing = data.get('future_priority_marketing', job.future_priority_marketing)
    job.future_priority_admin = data.get('future_priority_admin', job.future_priority_admin)
    job.future_priority_finance = data.get('future_priority_finance', job.future_priority_finance)
    job.future_priority_logistics = data.get('future_priority_logistics', job.future_priority_logistics)
    job.future_priority_technical = data.get('future_priority_technical', job.future_priority_technical)
    job.future_priority_others = data.get('future_priority_others', job.future_priority_others)
    job.future_other_specify = data.get('future_other_specify', job.future_other_specify)

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Job updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error updating job: {str(e)}"}), 400

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    # Ensure only the owner can delete their job
    username = session.get('username')
    if not username or job.business_name != username:
        return jsonify({"success": False, "message": "Permission denied"}), 403

    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({"success": True, "message": "Job deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error deleting job: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
