import os

import pandas as pd
import pyodbc
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not server or not database:
        raise ValueError(
            "Missing DB_SERVER or DB_NAME in .env."
        )

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    if username and password:
        conn_str += f"UID={username};PWD={password};"

    return pyodbc.connect(conn_str)


@st.cache_data
def load_customers():
    with get_connection() as conn:
        query = "SELECT * FROM dbo.customers;"
        return pd.read_sql(query, conn)


st.title("Sales Database - Customers")

try:
    df = load_customers()

    if df.empty:
        st.warning("No rows found in the customers table.")
    else:
        st.subheader(f"Rows: {len(df)}")
        st.dataframe(df, use_container_width=True)

except Exception as exc:
    st.error(f"Connection failed: {exc}")
    st.code(
        """
        Check your .env file values and make sure SQL Server allows this login.
        Example values:
        DB_SERVER=localhost
        DB_NAME=salesdb
        DB_USER=sa
        DB_PASSWORD=YourStrongPassword
        DB_DRIVER=ODBC Driver 18 for SQL Server
        """
    )
