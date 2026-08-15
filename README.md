# Sales Data Streamlit App

1. Copy `.env.example` to `.env` and fill in your SQL Server details.
2. Install dependencies:
   ```bash
   python -m pip install streamlit python-dotenv pyodbc
   ```
3. Run:
   ```bash
   streamlit run dbdata.py
   ```

This app reads from the `dbo.customers` table in the `salesdb` database and displays it in the browser.
