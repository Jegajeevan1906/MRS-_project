import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ============================
# GOOGLE SHEET CONNECTION
# ============================
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet by NAME
sheet = client.open("MRS_Billing")  # <-- your sheet name here
worksheet = sheet.sheet1

# Get all data from sheet
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# ============================
# STREAMLIT UI
# ============================
st.title("📊 MRS Billing Dashboard")

if not df.empty:
    # Show data
    st.subheader("🔹 All Records")
    st.dataframe(df)

    # Today filter
    today = datetime.now().strftime("%d.%m.%Y")
    today_df = df[df['Date'] == today]

    st.subheader(f"📅 Today ({today})")
    st.write(today_df)

    st.write("✅ Total customers today:", today_df['Customer'].count())
    st.write("✅ Total sales today:", today_df['Amount'].sum())

    # Month filter
    this_month = datetime.now().strftime("%m.%Y")
    month_df = df[df['Date'].str.contains(this_month)]

    st.subheader(f"📅 This Month ({this_month})")
    st.write(month_df)

    st.write("✅ Total customers this month:", month_df['Customer'].count())
    st.write("✅ Total sales this month:", month_df['Amount'].sum())

    # Sort by highest sales
    st.subheader("🏆 Top Employees by Sales (Descending)")
    sorted_df = df.groupby('Employee', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False)
    st.bar_chart(sorted_df.set_index('Employee'))

else:
    st.warning("No data found in Google Sheet yet!")
