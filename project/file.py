import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Record Management System", layout="wide")
st.title("Student Record Management System")
st.sidebar.image("sms.png", width=200)
if 'students' not in st.session_state:
    st.session_state.students = []

students = st.session_state.students

def add_student(students):
    with st.form("add_form"):
        st.subheader("Add New Student")
        ID = st.number_input("Enter your ID:", min_value=0, step=1)
        name = st.text_input("Enter your name:")
        age = st.number_input("Enter your age:", min_value=0, step=1)
        marks = st.number_input("Enter your marks:", min_value=0, max_value=100)
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if any(s['ID'] == ID for s in students):
                st.error(f"Student with ID {ID} already exists!")
            elif name == "":
                st.warning("Name cannot be empty.")
            else:
                students.append({"ID": ID, "Name": name, "Age": age, "Marks": marks})
                st.success("Student Added Successfully!")

def view_students(students):
    if len(students) == 0:
        st.warning("No data found")
    else:
        st.table(students)

def update_student(students):
    if len(students) == 0:
        st.warning("No students available to update.")
        return
        
    ids = [s['ID'] for s in students]
    selected_id = st.selectbox("Select ID to update", ids)
    
 
    student = next((s for s in students if s['ID'] == selected_id), None)
    
    if student:
        with st.form("update_form"):
            new_name = st.text_input("Enter new name", value=student['Name'])
            new_age = st.number_input("Enter new age", min_value=0, value=student['Age'])
            new_marks = st.number_input("Enter new marks", min_value=0, max_value=100, value=student['Marks'])
            
            if st.form_submit_button("Save Changes"):
                student['Name'] = new_name
                student['Age'] = new_age
                student['Marks'] = new_marks
                st.success("Student updated successfully!")

def delete_student(students):
    if len(students) == 0:
        st.warning("No students available to delete.")
        return
        
    ids = [s['ID'] for s in students]
    selected_id = st.selectbox("Select ID to remove", ids)
    
    if st.button("Delete"):
        st.session_state.students = [s for s in students if s['ID'] != selected_id]
        st.success(f"Student ID {selected_id} deleted successfully. Please refresh or navigate away.")

def find_student(students):
    name = st.text_input("Enter name to search")
    if name:
        matches = [s for s in students if name.lower() in s['Name'].lower()]
        if matches:
            st.write(matches)
        else:
            st.error("Name not found")

def average_marks(students):
    if len(students) == 0:
        st.write("No data found")
    else:
        total_marks = sum(student['Marks'] for student in students)
        average = total_marks / len(students)
        st.write(f"Average Marks: {average:.2f}")

def highest_marks(students):
    if len(students) == 0:
        st.write("No data found")
    else:
   
        topper = max(students, key=lambda s: s['Marks'])
        st.write(f"Highest marks scored are {topper['Marks']} by {topper['Name']}")

def download_file(students):
    if len(students) == 0:
        st.warning("No data available to download.")
    else:
        df = pd.DataFrame(students)

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Student Data",
            data=csv,
            file_name="student_records.csv",
            mime="text/csv"
        )

user_input = st.sidebar.selectbox("Menu", [
    "Add Student", "View Students", "Update Student", 
    "Delete Student", "Search Student", "Average Marks", "Topper","Download File"
])

if user_input == "Add Student":
    add_student(students)
elif user_input == "View Students":
    view_students(students)
elif user_input == "Update Student":
    update_student(students)
elif user_input == "Delete Student":
    delete_student(students)
elif user_input == "Search Student":
    find_student(students)
elif user_input == "Average Marks":
    average_marks(students)
elif user_input == "Topper":
    highest_marks(students)
elif user_input == "Download File":
    download_file(students)