import pandas as pd
import streamlit as st

from database import add_student, get_students, get_student
from services import calculate_grade, calculate_statistics


st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #2563eb;
        margin-bottom: 5px;
    }

    .author-name {
        font-size: 30px;
        font-weight: 900;
        text-align: center;
        letter-spacing: 4px;
        color: #7c3aed;
        margin-top: 0;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #2563eb;
    }

    div[data-testid="stMetric"] {
        background-color: #f1f5f9;
        border: 1px solid #dbeafe;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #e2e8f0;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def display_header():
    """Dashboard başlığını və müəllifin adını göstərir."""
    st.markdown(
        '<div class="main-title">🎓 Student Performance Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="author-name">NURAN HUSEYNZADE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Student Management & Performance Analytics System'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()


def display_statistics(students):
    """Statistik göstəriciləri interfeysdə göstərir."""
    statistics = calculate_statistics(students)

    st.markdown(
        '<div class="section-title">📊 Performance Overview</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Total Students",
        statistics["total_students"]
    )

    col2.metric(
        "📈 Average Score",
        statistics["average_score"]
    )

    col3.metric(
        "🏆 Highest Score",
        statistics["highest_score"]
    )

    col4.metric(
        "📉 Lowest Score",
        statistics["lowest_score"]
    )

    st.write("")


def display_students(students):
    """Tələbələri cədvəl şəklində göstərir."""
    if not students:
        st.info("Tələbə tapılmadı.")
        return

    student_data = []

    for student in students:
        score = student["score"]

        if score >= 90:
            status = "Excellent"
        elif score >= 80:
            status = "Very Good"
        elif score >= 70:
            status = "Good"
        elif score >= 60:
            status = "Passing"
        else:
            status = "Needs Improvement"

        student_data.append({
            "ID": student["id"],
            "Name": student["name"],
            "Score": score,
            "Grade": calculate_grade(score),
            "Status": status
        })

    dataframe = pd.DataFrame(student_data)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID"),
            "Name": st.column_config.TextColumn("Student Name"),
            "Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=100,
                format="%d"
            ),
            "Grade": st.column_config.TextColumn("Grade"),
            "Status": st.column_config.TextColumn("Performance")
        }
    )


def display_add_student_form():
    """Yeni tələbə əlavə etmək üçün form göstərir."""
    st.subheader("➕ Add New Student")

    with st.form("add_student_form", clear_on_submit=True):
        student_name = st.text_input(
            "Student Name",
            placeholder="Enter student's full name"
        )

        student_score = st.number_input(
            "Score",
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )

        submitted = st.form_submit_button(
            "➕ Add Student",
            use_container_width=True
        )

        if submitted:
            if not student_name.strip():
                st.error("Tələbənin adını daxil edin.")
            else:
                try:
                    add_student(
                        student_name.strip(),
                        int(student_score)
                    )

                    st.success("Tələbə uğurla əlavə edildi.")
                    st.rerun()

                except Exception as error:
                    st.error("Tələbə əlavə edilərkən xəta baş verdi.")
                    st.exception(error)


def display_search():
    """Tələbəni adına görə axtarır."""
    st.subheader("🔎 Search Student")

    search_name = st.text_input(
        "Student Name",
        placeholder="Enter a name to search..."
    )

    if search_name.strip():
        try:
            search_results = get_student(search_name.strip())

            if search_results:
                st.success(
                    f"{len(search_results)} tələbə tapıldı."
                )
                display_students(search_results)
            else:
                st.warning("Bu ada uyğun tələbə tapılmadı.")

        except Exception as error:
            st.error("Axtarış zamanı xəta baş verdi.")
            st.exception(error)


def display_dashboard(students):
    """Əsas dashboard səhifəsini göstərir."""
    display_statistics(students)

    st.subheader("📋 Student List")

    display_students(students)

    if students:
        st.subheader("📊 Student Score Chart")

        chart_data = pd.DataFrame({
            "Student": [student["name"] for student in students],
            "Score": [student["score"] for student in students]
        })

        st.bar_chart(
            chart_data.set_index("Student"),
            y="Score"
        )


def main():
    display_header()

    with st.sidebar:
        st.markdown("## 🎓 Student Dashboard")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "👨‍🎓 Students",
                "➕ Add Student",
                "🔎 Search"
            ]
        )

        st.markdown("---")

        st.markdown("### 👨‍💻 Developer")
        st.markdown("**NURAN HUSEYNZADE**")

        st.caption("Student Performance Dashboard")

    try:
        students = get_students()

        if page == "📊 Dashboard":
            display_dashboard(students)

        elif page == "👨‍🎓 Students":
            st.subheader("👨‍🎓 All Students")
            display_students(students)

        elif page == "➕ Add Student":
            display_add_student_form()

        elif page == "🔎 Search":
            display_search()

    except Exception:
        st.error(
            "Database ilə əlaqə yaratmaq mümkün olmadı. "
            "Bağlantı parametrlərini və database-i yoxlayın."
        )

        st.info(
            "PostgreSQL bağlantısını, Streamlit Secrets "
            "parametrlərini və students cədvəlini yoxlayın."
        )

    st.markdown(
        '<div class="footer">'
        'Student Performance Dashboard<br>'
        'Developed by <b>NURAN HUSEYNZADE</b>'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
