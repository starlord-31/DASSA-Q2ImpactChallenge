import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("Job Portal")

# Function to handle login
def login():
    st.header("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    role = st.selectbox("Role", ["Job Seeker", "Business"], key="login_role")
    login_button = st.button("Login", key="login_button")

    if login_button:
        if username and password:
            try:
                response = requests.post(
                    'http://localhost:5000/login',
                    json={"username": username, "password": password, "role": role}
                )
                if response.status_code == 200:
                    st.session_state['username'] = username
                    st.session_state['role'] = role
                    st.success(f"Login successful! Welcome, {username}.")
                    st.session_state['logged_in'] = True
                else:
                    error_message = response.json().get("message", "Invalid credentials.")
                    st.error(f"Login failed: {error_message}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter your username and password to log in.")

# Function to handle registration
def register():
    st.subheader("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["Job Seeker", "Business"], key="register_role")
    
    if st.button("Register"):
        if new_username and new_password:
            try:
                response = requests.post(
                    'http://localhost:5000/register', 
                    json={"username": new_username, "password": new_password, "role": new_role}
                )
                if response.status_code == 201:
                    st.success("User registered successfully!")
                else:
                    error_message = response.json().get("message", "Registration failed.")
                    st.error(f"Error: {error_message}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please fill out all fields to register.")

# Function to get user location using components.html
def get_user_location():
    geolocation_html = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            document.getElementById("demo").innerHTML = "Geolocation is not supported by this browser.";
        }
    }

    function showPosition(position) {
        var coords = position.coords.latitude + "," + position.coords.longitude;
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        urlParams.set('coords', coords);
        window.location.search = urlParams.toString();
    }

    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert("User denied the request for Geolocation.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Location information is unavailable.");
                break;
            case error.TIMEOUT:
                alert("The request to get user location timed out.");
                break;
            case error.UNKNOWN_ERROR:
                alert("An unknown error occurred.");
                break;
        }
    }
    </script>
    <button onclick="getLocation()">Get Current Location</button>
    <p id="demo"></p>
    """
    components.html(geolocation_html, height=0)

    coords = st.experimental_get_query_params().get('coords')
    if coords:
        latitude, longitude = map(float, coords[0].split(','))
        st.write(f"Your current location: Latitude {latitude}, Longitude {longitude}")
        return latitude, longitude
    else:
        return None, None

# Main app logic
def main():
    if st.session_state.get('logged_in'):
        st.session_state.pop('logged_in')

    if 'username' in st.session_state and 'role' in st.session_state:
        username = st.session_state['username']
        role = st.session_state['role']
        
        if role == "Business":
            st.subheader("Business Dashboard - Manage Jobs")

            if st.button("Logout"):
                st.session_state.clear()
                st.success("Logged out successfully!")
                return

            if st.button("View My Job Postings"):
                try:
                    jobs_response = requests.get(f'http://localhost:5000/jobs?username={username}')
                    if jobs_response.status_code == 200:
                        jobs = jobs_response.json()
                        if jobs:
                            for job in jobs:
                                st.subheader(f"Job ID: {job.get('id')}")
                                st.write(f"Business Name: {job.get('business_name')}")
                                st.write(f"Latitude: {job.get('lat')}")
                                st.write(f"Longitude: {job.get('lng')}")
                                edit_col, delete_col = st.columns(2)
                                with edit_col:
                                    if st.button(f"Edit Job {job['id']}", key=f"edit_{job['id']}"):
                                        st.session_state['edit_job_id'] = job['id']
                                        st.session_state['action'] = 'Edit'
                                with delete_col:
                                    if st.button(f"Delete Job {job['id']}", key=f"delete_{job['id']}"):
                                        delete_response = requests.delete(
                                            f'http://localhost:5000/jobs/{job["id"]}', 
                                            json={"created_by": username}
                                        )
                                        if delete_response.status_code == 200:
                                            st.success("Job deleted successfully!")
                                            st.session_state['refresh_jobs'] = True
                                        else:
                                            error_message = delete_response.json().get('message', 'Failed to delete job.')
                                            st.error(f"Error: {error_message}")
                        else:
                            st.info("No job postings found.")
                    else:
                        error_message = jobs_response.json().get('message', 'Failed to fetch job postings.')
                        st.error(f"Error: {error_message}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching job postings: {e}")

            if st.session_state.get('refresh_jobs'):
                st.session_state.pop('refresh_jobs')

            st.write("Click the button below to get your current location:")
            latitude, longitude = get_user_location()

            lat = latitude if latitude else 0.0
            lng = longitude if longitude else 0.0

            with st.form(key='job_form'):
                action = st.selectbox("Action", ["Add", "Edit"], index=0)
                if st.session_state.get('action'):
                    action = st.session_state.pop('action')

                job_id = st.text_input("Job ID (Required for Edit)", key="job_id")
                business_name = st.text_input("Business Name")
                latitude_input = st.number_input("Latitude", value=lat, format="%.6f")
                longitude_input = st.number_input("Longitude", value=lng, format="%.6f")
                
                # Adding the other input fields for a job
                governorate = st.text_input("Governorate")
                district = st.text_input("District")
                registered = st.text_input("Registered")
                registration_type = st.text_input("Registration Type")
                economic_sector = st.text_input("Economic Sector")
                sub_sector = st.text_input("Sub Sector")
                products_services = st.text_area("Products/Services")
                phone_number = st.text_input("Phone Number")
                business_phone = st.text_input("Business Phone")
                employee_count = st.text_input("Employee Count")
                enterprise_size = st.text_input("Enterprise Size")
                has_vacancies = st.selectbox("Has Vacancies", ["Yes", "No"])
                num_vacancies = st.number_input("Number of Vacancies", min_value=0)
                current_interns = st.number_input("Current Interns", min_value=0)
                current_seasonal = st.number_input("Current Seasonal Employees", min_value=0)
                current_entry_level = st.number_input("Current Entry Level Employees", min_value=0)
                current_mid_senior = st.number_input("Current Mid-Senior Level Employees", min_value=0)
                current_senior_mgmt = st.number_input("Current Senior Management", min_value=0)
                current_cust_service = st.number_input("Current Customer Service", min_value=0)
                current_sales = st.number_input("Current Sales Employees", min_value=0)
                current_priority_it = st.number_input("Current Priority IT", min_value=0)
                current_priority_marketing = st.number_input("Current Priority Marketing", min_value=0)
                current_priority_admin = st.number_input("Current Priority Admin", min_value=0)
                current_priority_finance = st.number_input("Current Priority Finance", min_value=0)
                current_priority_logistics = st.number_input("Current Priority Logistics", min_value=0)
                current_priority_technical = st.number_input("Current Priority Technical", min_value=0)
                current_priority_others = st.number_input("Current Priority Others", min_value=0)
                current_other_specify = st.text_area("Current Other Specify")
                youth_employment = st.text_input("Youth Employment")
                future_needs = st.text_area("Future Needs")
                future_num_vacancies = st.number_input("Future Number of Vacancies", min_value=0)
                future_interns = st.number_input("Future Interns", min_value=0)
                future_seasonal = st.number_input("Future Seasonal Employees", min_value=0)
                future_entry_level = st.number_input("Future Entry Level Employees", min_value=0)
                future_mid_senior = st.number_input("Future Mid-Senior Level Employees", min_value=0)
                future_senior_mgmt = st.number_input("Future Senior Management", min_value=0)
                future_total = st.number_input("Future Total Employees", min_value=0)
                future_cust_service = st.number_input("Future Customer Service", min_value=0)
                future_sales = st.number_input("Future Sales Employees", min_value=0)
                future_priority_it = st.number_input("Future Priority IT", min_value=0)
                future_priority_marketing = st.number_input("Future Priority Marketing", min_value=0)
                future_priority_admin = st.number_input("Future Priority Admin", min_value=0)
                future_priority_finance = st.number_input("Future Priority Finance", min_value=0)
                future_priority_logistics = st.number_input("Future Priority Logistics", min_value=0)
                future_priority_technical = st.number_input("Future Priority Technical", min_value=0)
                future_priority_others = st.number_input("Future Priority Others", min_value=0)
                future_other_specify = st.text_area("Future Other Specify")
                submitted = st.form_submit_button("Submit")

                if submitted:
                    if not business_name:
                        st.warning("Please provide a business name.")
                    else:
                        job_data = {
                            "id": job_id if job_id else None,
                            "business_name": business_name,
                            "lat": latitude_input,
                            "lng": longitude_input,
                            "governorate": governorate,
                            "district": district,
                            "registered": registered,
                            "registration_type": registration_type,
                            "economic_sector": economic_sector,
                            "sub_sector": sub_sector,
                            "products_services": products_services,
                            "phone_number": phone_number,
                            "business_phone": business_phone,
                            "employee_count": employee_count,
                            "enterprise_size": enterprise_size,
                            "has_vacancies": has_vacancies,
                            "num_vacancies": num_vacancies,
                            "current_interns": current_interns,
                            "current_seasonal": current_seasonal,
                            "current_entry_level": current_entry_level,
                            "current_mid_senior": current_mid_senior,
                            "current_senior_mgmt": current_senior_mgmt,
                            "current_cust_service": current_cust_service,
                            "current_sales": current_sales,
                            "current_priority_it": current_priority_it,
                            "current_priority_marketing": current_priority_marketing,
                            "current_priority_admin": current_priority_admin,
                            "current_priority_finance": current_priority_finance,
                            "current_priority_logistics": current_priority_logistics,
                            "current_priority_technical": current_priority_technical,
                            "current_priority_others": current_priority_others,
                            "current_other_specify": current_other_specify,
                            "youth_employment": youth_employment,
                            "future_needs": future_needs,
                            "future_num_vacancies": future_num_vacancies,
                            "future_interns": future_interns,
                            "future_seasonal": future_seasonal,
                            "future_entry_level": future_entry_level,
                            "future_mid_senior": future_mid_senior,
                            "future_senior_mgmt": future_senior_mgmt,
                            "future_total": future_total,
                            "future_cust_service": future_cust_service,
                            "future_sales": future_sales,
                            "future_priority_it": future_priority_it,
                            "future_priority_marketing": future_priority_marketing,
                            "future_priority_admin": future_priority_admin,
                            "future_priority_finance": future_priority_finance,
                            "future_priority_logistics": future_priority_logistics,
                            "future_priority_technical": future_priority_technical,
                            "future_priority_others": future_priority_others,
                            "future_other_specify": future_other_specify,
                            "created_by": username
                        }

                        if action == "Add":
                            response = requests.post('http://localhost:5000/jobs', json=job_data)
                            if response.status_code == 201:
                                st.success("Job added successfully!")
                            else:
                                error_message = response.json().get('message', 'Failed to add job.')
                                st.error(f"Failed to add job. Error: {error_message}")
                        elif action == "Edit":
                            if job_id:
                                response = requests.put(f'http://localhost:5000/jobs/{job_id}', json=job_data)
                                if response.status_code == 200:
                                    st.success("Job updated successfully!")
                                else:
                                    error_message = response.json().get('message', 'Failed to update job.')
                                    st.error(f"Failed to update job. Error: {error_message}")
                            else:
                                st.warning("Please provide a Job ID to edit.")

        elif role == "Job Seeker":
            st.subheader("Job Seeker Dashboard")

            if st.button("Logout"):
                st.session_state.clear()
                st.success("Logged out successfully!")
                return

            try:
                jobs_response = requests.get('http://localhost:5000/jobs')
                if jobs_response.status_code == 200:
                    jobs = jobs_response.json()
                    if jobs:
                        for job in jobs:
                            st.subheader(job.get("business_name", "Business Name"))
                            st.write(f"Latitude: {job.get('lat', 'N/A')}")
                            st.write(f"Longitude: {job.get('lng', 'N/A')}")
                            st.write(f"Governorate: {job.get('governorate', 'N/A')}")
                            st.write(f"District: {job.get('district', 'N/A')}")
                            st.write(f"Products/Services: {job.get('products_services', 'N/A')}")
                    else:
                        st.info("No jobs available at the moment.")
                else:
                    error_message = jobs_response.json().get('message', 'Failed to fetch jobs.')
                    st.error(f"Error: {error_message}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching jobs: {e}")

    else:
        option = st.selectbox("Select an option", ["Login", "Register"])

        if option == "Login":
            login()
        elif option == "Register":
            register()

if __name__ == "__main__":
    main()
