import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random

# Page config
st.set_page_config(
    page_title="WasteFlow - Contract & Compliance Management",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 4px;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Sample data
@st.cache_data
def load_sample_data():
    contracts = [
        {
            "id": "WM-2024-001",
            "customer": "Metro City Municipal",
            "type": "Municipal Solid Waste",
            "value": 2500000,
            "start_date": "2024-01-01",
            "end_date": "2026-12-31",
            "status": "Active",
            "compliance_score": 95,
            "next_review": "2024-06-15",
            "service_frequency": "Daily",
            "locations": 45
        },
        {
            "id": "WM-2024-002",
            "customer": "TechCorp Industries",
            "type": "Commercial Waste",
            "value": 850000,
            "start_date": "2024-03-01",
            "end_date": "2025-02-28",
            "status": "Active",
            "compliance_score": 88,
            "next_review": "2024-07-01",
            "service_frequency": "3x Weekly",
            "locations": 12
        },
        {
            "id": "WM-2024-003",
            "customer": "GreenTech Manufacturing",
            "type": "Hazardous Waste",
            "value": 1200000,
            "start_date": "2024-02-15",
            "end_date": "2025-02-14",
            "status": "Renewal Required",
            "compliance_score": 92,
            "next_review": "2024-05-30",
            "service_frequency": "Weekly",
            "locations": 8
        },
        {
            "id": "WM-2024-004",
            "customer": "Hospital Network LLC",
            "type": "Medical Waste",
            "value": 650000,
            "start_date": "2024-01-15",
            "end_date": "2024-12-31",
            "status": "Compliance Issue",
            "compliance_score": 72,
            "next_review": "2024-05-15",
            "service_frequency": "2x Weekly",
            "locations": 25
        }
    ]
    
    compliance_alerts = [
        {
            "contract_id": "WM-2024-004",
            "customer": "Hospital Network LLC",
            "alert_type": "Regulatory Compliance",
            "severity": "High",
            "description": "Missing DOT hazmat certification renewal",
            "due_date": "2024-05-20",
            "days_overdue": 5
        },
        {
            "contract_id": "WM-2024-003",
            "customer": "GreenTech Manufacturing",
            "alert_type": "Contract Renewal",
            "severity": "Medium",
            "description": "Contract renewal required within 30 days",
            "due_date": "2024-06-15",
            "days_overdue": 0
        }
    ]
    
    return pd.DataFrame(contracts), pd.DataFrame(compliance_alerts)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>♻️ WasteFlow Contract & Compliance Management</h1>
        <p>Intelligent Contract Management for Waste Management Companies</p>
    </div>
    """, unsafe_allow_html=True)
    
    contracts_df, alerts_df = load_sample_data()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", [
        "Dashboard", 
        "Contract Management", 
        "Compliance Monitoring", 
        "Analytics & Reports"
    ])
    
    if page == "Dashboard":
        show_dashboard(contracts_df, alerts_df)
    elif page == "Contract Management":
        show_contract_management(contracts_df)
    elif page == "Compliance Monitoring":
        show_compliance_monitoring(alerts_df, contracts_df)
    elif page == "Analytics & Reports":
        show_analytics(contracts_df)

def show_dashboard(contracts_df, alerts_df):
    st.title("📊 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_value = contracts_df['value'].sum()
        st.metric("Total Contract Value", f"${total_value:,.0f}", "↑ 12%")
    
    with col2:
        active_contracts = len(contracts_df[contracts_df['status'] == 'Active'])
        st.metric("Active Contracts", active_contracts, "↑ 2")
    
    with col3:
        avg_compliance = contracts_df['compliance_score'].mean()
        st.metric("Avg Compliance Score", f"{avg_compliance:.1f}%", "↑ 3.2%")
    
    with col4:
        high_alerts = len(alerts_df[alerts_df['severity'] == 'High'])
        st.metric("Critical Alerts", high_alerts, "↓ 1")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Contract Value by Type")
        fig = px.pie(contracts_df, values='value', names='type', 
                    color_discrete_sequence=['#2E7D32', '#4CAF50', '#66BB6A', '#81C784'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Compliance Score Distribution")
        fig = px.bar(contracts_df, x='customer', y='compliance_score',
                    color='compliance_score', color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🚨 Recent Compliance Alerts")
    for _, alert in alerts_df.iterrows():
        severity_class = f"alert-{alert['severity'].lower()}"
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>{alert['severity']} Priority:</strong> {alert['customer']}<br>
            <strong>Issue:</strong> {alert['description']}<br>
            <strong>Due:</strong> {alert['due_date']}
        </div>
        """, unsafe_allow_html=True)

def show_contract_management(contracts_df):
    st.title("📋 Contract Management")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(contracts_df['status'].unique()))
    with col2:
        type_filter = st.selectbox("Filter by Type", ["All"] + list(contracts_df['type'].unique()))
    with col3:
        search_term = st.text_input("Search Customer")
    
    filtered_df = contracts_df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['type'] == type_filter]
    if search_term:
        filtered_df = filtered_df[filtered_df['customer'].str.contains(search_term, case=False)]
    
    for _, contract in filtered_df.iterrows():
        with st.expander(f"{contract['customer']} - {contract['id']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Contract Value:** ${contract['value']:,.0f}")
                st.write(f"**Service Type:** {contract['type']}")
                st.write(f"**Status:** {contract['status']}")
            
            with col2:
                st.write(f"**Start Date:** {contract['start_date']}")
                st.write(f"**End Date:** {contract['end_date']}")
                st.write(f"**Next Review:** {contract['next_review']}")
            
            with col3:
                st.write(f"**Compliance Score:** {contract['compliance_score']}%")
                st.write(f"**Service Frequency:** {contract['service_frequency']}")
                st.write(f"**Locations:** {contract['locations']}")

def show_compliance_monitoring(alerts_df, contracts_df):
    st.title("⚖️ Compliance Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Compliance Score Trends")
        dates = pd.date_range(start='2024-01-01', end='2024-05-01', freq='W')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Score': [88 + random.randint(-5, 5) for _ in range(len(dates))]
        })
        fig = px.line(trend_data, x='Date', y='Score', title="Weekly Compliance Scores")
        fig.add_hline(y=90, line_dash="dash", line_color="green", annotation_text="Target: 90%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Alert Distribution")
        alert_counts = alerts_df['severity'].value_counts()
        fig = px.bar(x=alert_counts.index, y=alert_counts.values,
                    color=alert_counts.index, 
                    color_discrete_map={'High': '#f44336', 'Medium': '#ff9800', 'Low': '#4caf50'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Active Compliance Alerts")
    
    for _, alert in alerts_df.iterrows():
        severity_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        
        with st.expander(f"{severity_color[alert['severity']]} {alert['customer']} - {alert['alert_type']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Contract ID:** {alert['contract_id']}")
                st.write(f"**Alert Type:** {alert['alert_type']}")
                st.write(f"**Severity:** {alert['severity']}")
            
            with col2:
                st.write(f"**Due Date:** {alert['due_date']}")
                st.write(f"**Days Overdue:** {alert['days_overdue']}")
                st.write(f"**Description:** {alert['description']}")

def show_analytics(contracts_df):
    st.title("📈 Analytics & Reports")
    
    st.subheader("Revenue Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [2.1, 2.3, 2.5, 2.4, 2.6, 2.8]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=revenue, mode='lines+markers', name='Revenue (M$)'))
        fig.update_layout(title="Monthly Revenue Projection", yaxis_title="Revenue (Millions $)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        renewal_data = contracts_df[contracts_df['status'].isin(['Renewal Required', 'Active'])]
        renewal_data['end_date'] = pd.to_datetime(renewal_data['end_date'])
        renewal_data['months_to_renewal'] = (renewal_data['end_date'] - pd.Timestamp.now()).dt.days / 30
        
        fig = px.scatter(renewal_data, x='months_to_renewal', y='value', 
                        color='type', size='locations',
                        title="Contract Renewal Timeline")
        fig.update_xaxis(title="Months to Renewal")
        fig.update_yaxis(title="Contract Value ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Contract Retention Rate", "94.2%", "↑ 2.1%")
        st.metric("Avg Contract Duration", "18 months", "↑ 1 month")
    
    with col2:
        st.metric("Revenue per Location", "$52,340", "↑ 8.3%")
        st.metric("Compliance Rate", "91.5%", "↑ 4.2%")
    
    with col3:
        st.metric("Customer Satisfaction", "4.6/5.0", "↑ 0.2")
        st.metric("Contract Processing Time", "3.2 days", "↓ 1.1 days")

if __name__ == "__main__":
    main()