import pandas as pd
import streamlit as st

from database import add_student, get_students, get_student
from services import calculate_grade, calculate_statistics


st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


def display_statistics(students):
    """Statistik göstəriciləri interfeysdə göstərir."""
    statistics = calculate_statistics(students)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", statistics["total_students"])
    col2.metric("Average Score", statistics["average_score"])
    col3.metric("Highest Score", statistics["highest_score"])
    col4.metric("Lowest Score", statistics["lowest_score"])


def display_students(students):
    """Tələbələri cədvəl şəklində göstərir."""
    if not students:
        st.info("Tələbə tapılmadı.")
        return

    student_data = []

    for student in students:
        student_data.append({
            "Name": student["name"],
            "Score": student["score"],
            "Grade": calculate_grade(student["score"])
        })

    dataframe = pd.DataFrame(student_data)
    st.dataframe(dataframe, use_container_width=True, hide_index=True)


def main():
    st.title("🎓 Student Performance Dashboard")
    st.write("Tələbə nəticələrinin idarə edilməsi sistemi")

    # Tələbə əlavə etmək
    st.header("Add Student")

    with st.form("add_student_form"):
        student_name = st.text_input("Student Name")

        student_score = st.number_input(
            "Score",
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not student_name.strip():
                st.error("Tələbənin adını daxil edin.")
            else:
                try:
                    add_student(student_name.strip(), student_score)
                    st.success("Tələbə uğurla əlavə edildi.")
                    st.rerun()
                except Exception:
                    st.error("Tələbə əlavə edilərkən xəta baş verdi.")

    # Bütün tələbələr
    st.header("Student List")

    try:
        students = get_students()

        display_statistics(students)
        display_students(students)

        # Tələbə axtarışı
        st.header("Search Student")

        search_name = st.text_input("Student Name", key="search_name")

        if search_name.strip():
            search_results = get_student(search_name.strip())
            display_students(search_results)

    except Exception:
        st.error(
            "Database ilə əlaqə yaratmaq mümkün olmadı. "
            "Bağlantı parametrlərini və database-i yoxlayın."
        )


if __name__ == "__main__":
    main()