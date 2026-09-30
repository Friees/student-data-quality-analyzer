
import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

st.title("Student Data Quality Analyzer")

st.write("Upload a student CSV file to check its data quality.")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    total_records = len(df)

    missing_values = df.isnull().sum().sum()

    duplicate_records = df.duplicated().sum()

    def valid_email(email):
        if pd.isna(email):
            return False

        return bool(
            re.match(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                str(email)
            )
        )

    invalid_emails = (~df["Email"].apply(valid_email)).sum()

    completeness = (
        1 -
        (missing_values / (len(df) * len(df.columns)))
    ) * 100

    uniqueness = (
        1 -
        (duplicate_records / len(df))
    ) * 100

    validity = (
        1 -
        (invalid_emails / len(df))
    ) * 100

    overall_quality = (
        completeness +
        validity +
        uniqueness
    ) / 3

    st.subheader("Data Quality Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", total_records)
    col2.metric("Missing Values", missing_values)
    col3.metric("Duplicate Records", duplicate_records)

    st.metric("Invalid Emails", invalid_emails)

    st.subheader("Quality Scores")

    st.write(
        "Completeness:",
        round(completeness, 2),
        "%"
    )

    st.write(
        "Validity:",
        round(validity, 2),
        "%"
    )

    st.write(
        "Uniqueness:",
        round(uniqueness, 2),
        "%"
    )

    st.success(
        "Overall Data Quality Score: "
        + str(round(overall_quality, 2))
        + "%"
    )

    st.subheader("Data Quality Bar Chart")

    metrics = [
        "Completeness",
        "Validity",
        "Uniqueness"
    ]

    scores = [
        completeness,
        validity,
        uniqueness
    ]

    chart_data = pd.DataFrame({
        "Quality Dimension": metrics,
        "Score": scores
    })

    st.bar_chart(
        chart_data.set_index("Quality Dimension")
    )

    st.subheader("Data Quality Pie Chart")

    fig, ax = plt.subplots()

    ax.pie(
        scores,
        labels=metrics,
        autopct="%1.1f%%"
    )

    ax.set_title("Data Quality Distribution")

    st.pyplot(fig)

    st.subheader("Uploaded Dataset")

    st.dataframe(df)
