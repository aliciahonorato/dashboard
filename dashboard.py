import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dashboard Title
st.title("Performance Indicator Dashboard for SMEs")

# Load Data
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    # Carregar o arquivo CSV com ponto e vírgula como separador
    data = pd.read_csv(uploaded_file, delimiter=';')
    
    st.write("### Loaded Data:")
    st.dataframe(data)

    # Ensure necessary columns are present
    required_columns = ["Date", "Sales", "Revenue", "Customer_ID", "Region", "Retention Status"]
    if not all(col in data.columns for col in required_columns):
        st.error(f"The uploaded file must contain the following columns: {';'.join(required_columns)}")
    else:
        # Convert 'Date' to datetime format
        data["Date"] = pd.to_datetime(data["Date"])

        # Metrics
        total_sales = data["Sales"].sum()
        total_revenue = data["Revenue"].sum()
        customer_retention_rate = (data["Retention Status"].str.lower() == "yes").mean() * 100

        st.metric("Total Sales", f"{total_sales}")
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
        st.metric("Customer Retention Rate", f"{customer_retention_rate:.2f}%")

        # Sales Over Time (Daily, Weekly, Monthly)
        st.write("### Sales Performance Over Time")
        sales_timeframe = st.selectbox("Choose timeframe", ["Daily", "Weekly", "Monthly"])
        if sales_timeframe == "Daily":
            sales_over_time = data.groupby(data["Date"].dt.date)["Sales"].sum()
        elif sales_timeframe == "Weekly":
            sales_over_time = data.groupby(data["Date"].dt.to_period("W"))["Sales"].sum()
        else:
            sales_over_time = data.groupby(data["Date"].dt.to_period("M"))["Sales"].sum()

        fig, ax = plt.subplots()
        sales_over_time.plot(ax=ax, kind="line")
        ax.set_title(f"Sales ({sales_timeframe})")
        ax.set_ylabel("Sales")
        ax.set_xlabel("Time")
        st.pyplot(fig)

        # Sales by Region
        st.write("### Sales by Region")
        sales_by_region = data.groupby("Region")["Sales"].sum()
        fig, ax = plt.subplots()
        sales_by_region.plot(ax=ax, kind="bar", color="skyblue")
        ax.set_title("Sales by Region")
        ax.set_ylabel("Sales")
        ax.set_xlabel("Region")
        st.pyplot(fig)

        # Revenue Growth (if Growth Rate column is not available)
        if "Growth Rate" not in data.columns:
            data["Growth Rate"] = data["Revenue"].pct_change() * 100

        avg_growth_rate = data["Growth Rate"].mean()
        st.metric("Average Growth Rate", f"{avg_growth_rate:.2f}%")

        # Insights Section
        st.write("### Additional Insights")
        st.write("Top 5 Customers by Revenue:")
        top_customers = data.groupby("Customer_ID")["Revenue"].sum().nlargest(5)
        st.table(top_customers)

# Initial Message
else:
    st.write("Please upload a CSV file to get started.")
