import streamlit as st
import pandas as pd

# Initialize an example data store (in a real application, this would be a database)
if 'job_listings' not in st.session_state:
    st.session_state['job_listings'] = pd.DataFrame(columns=["Business Name", "Job Title", "Job Type", "Location", "Description"])

def display_job_seeker_view():
    st.header("Job Seeker Profile")
    st.write("Browse available job opportunities below:")

    # Display job listings
    if st.session_state['job_listings'].empty:
        st.write("No job listings available.")
    else:
        st.dataframe(st.session_state['job_listings'])

def display_business_view():
    st.header("Business Profile")
    st.write("Post a new job listing:")

    # Job posting form
    business_name = st.text_input("Business Name")
    job_title = st.text_input("Job Title")
    job_type = st.selectbox("Job Type", ["Internship", "Entry-level", "Senior", "Management"])
    location = st.text_input("Location")
    description = st.text_area("Job Description")

    if st.button("Post Job"):
        if business_name and job_title and location and description:
            new_job = {
                "Business Name": business_name,
                "Job Title": job_title,
                "Job Type": job_type,
                "Location": location,
                "Description": description,
            }
            # Append new job to the session state DataFrame
            st.session_state['job_listings'] = st.session_state['job_listings'].append(new_job, ignore_index=True)
            st.success("Job posted successfully!")
        else:
            st.error("Please fill out all fields before posting.")

# Main app function
def main():
    st.title("Job Portal Website")
    profile_type = st.sidebar.selectbox("Select Profile", ["Job Seeker", "Business"])

    if profile_type == "Job Seeker":
        display_job_seeker_view()
    elif profile_type == "Business":
        display_business_view()

if __name__ == "__main__":
    main()
