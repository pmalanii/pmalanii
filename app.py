import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="WasteFlow - Contract Management",
    page_icon="♻️",
    layout="wide"
)

@st.cache_data
def load_sample_data():
    contracts = [
        {
            "id": "WM-2024-001",
            "customer": "Metro City Municipal",
            "type": "Municipal Solid Waste",
            "value": 2500000,
            "status": "Active",
            "compliance_score": 95,
            "locations": 45
        },
        {
            "id": "WM-2024-002",
            "customer": "TechCorp Industries",
            "type": "Commercial Waste",
            "value": 850000,
            "status": "Active",
            "compliance_score": 88,
            "locations": 12
        }
    ]
    
    alerts = [
        {
            "customer": "Hospital Network LLC",
            "severity": "High",
            "description": "Missing DOT certification renewal"
        }
    ]
    
    return pd.DataFrame(contracts), pd.DataFrame(alerts)

def main():
    st.title("♻️ WasteFlow Contract & Compliance Management")
    st.markdown("Intelligent Contract Management for Waste Management Companies")
    
    contracts_df, alerts_df = load_sample_data()
    
    page = st.sidebar.selectbox("Select Page", [
        "Dashboard", 
        "Contract Management", 
        "Analytics"
    ])
    
    if page == "Dashboard":
        show_dashboard(contracts_df, alerts_df)
    elif page == "Contract Management":
        show_contracts(contracts_df)
    elif page == "Analytics":
        show_analytics(contracts_df)

def show_dashboard(contracts_df, alerts_df):
    st.header("📊 Executive Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_value = contracts_df['value'].sum()
        st.metric("Total Contract Value", f"${total_value:,.0f}")
    
    with col2:
        active_contracts = len(contracts_df)
        st.metric("Active Contracts", active_contracts)
    
    with col3:
        avg_compliance = contracts_df['compliance_score'].mean()
        st.metric("Avg Compliance Score", f"{avg_compliance:.1f}%")
    
    st.subheader("Contract Value by Type")
    fig = px.pie(contracts_df, values='value', names='type')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🚨 Recent Alerts")
    for _, alert in alerts_df.iterrows():
        st.warning(f"**{alert['severity']}:** {alert['customer']} - {alert['description']}")

def show_contracts(contracts_df):
    st.header("📋 Contract Management")
    
    for _, contract in contracts_df.iterrows():
        with st.expander(f"{contract['customer']} - {contract['id']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Value:** ${contract['value']:,.0f}")
                st.write(f"**Type:** {contract['type']}")
            
            with col2:
                st.write(f"**Status:** {contract['status']}")
                st.write(f"**Locations:** {contract['locations']}")

def show_analytics(contracts_df):
    st.header("📈 Analytics & Reports")
    
    st.subheader("Revenue Projection")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    revenue = [2.1, 2.3, 2.5, 2.4, 2.6, 2.8]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=revenue, mode='lines+markers'))
    fig.update_layout(title="Monthly Revenue (Millions $)")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Contract Retention", "94.2%")
    with col2:
        st.metric("Customer Satisfaction", "4.6/5.0")

if __name__ == "__main__":
    main()