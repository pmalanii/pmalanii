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
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
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
    .contract-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #2E7D32;
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
        },
        {
            "contract_id": "WM-2024-001",
            "customer": "Metro City Municipal",
            "alert_type": "Rate Adjustment",
            "severity": "Low",
            "description": "Annual rate review scheduled",
            "due_date": "2024-06-30",
            "days_overdue": 0
        }
    ]
    
    return pd.DataFrame(contracts), pd.DataFrame(compliance_alerts)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>♻️ WasteFlow Contract & Compliance Management</h1>
        <p>Intelligent Contract Management for Waste Management Companies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    contracts_df, alerts_df = load_sample_data()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", [
        "Dashboard", 
        "Contract Management", 
        "Compliance Monitoring", 
        "Analytics & Reports",
        "Contract Analysis"
    ])
    
    if page == "Dashboard":
        show_dashboard(contracts_df, alerts_df)
    elif page == "Contract Management":
        show_contract_management(contracts_df)
    elif page == "Compliance Monitoring":
        show_compliance_monitoring(alerts_df, contracts_df)
    elif page == "Analytics & Reports":
        show_analytics(contracts_df)
    elif page == "Contract Analysis":
        show_contract_analysis()

def show_dashboard(contracts_df, alerts_df):
    st.title("📊 Executive Dashboard")
    
    # Key Metrics
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
    
    # Charts
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
    
    # Recent Alerts
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
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(contracts_df['status'].unique()))
    with col2:
        type_filter = st.selectbox("Filter by Type", ["All"] + list(contracts_df['type'].unique()))
    with col3:
        search_term = st.text_input("Search Customer")
    
    # Apply filters
    filtered_df = contracts_df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['type'] == type_filter]
    if search_term:
        filtered_df = filtered_df[filtered_df['customer'].str.contains(search_term, case=False)]
    
    # Contract cards
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
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"View Details", key=f"view_{contract['id']}"):
                    st.info("Contract details would open in a new window")
            with col2:
                if st.button(f"Edit Contract", key=f"edit_{contract['id']}"):
                    st.info("Contract editing interface would open")
            with col3:
                if st.button(f"Generate Report", key=f"report_{contract['id']}"):
                    st.success("Contract report generated successfully!")

def show_compliance_monitoring(alerts_df, contracts_df):
    st.title("⚖️ Compliance Monitoring")
    
    # Compliance overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Compliance Score Trends")
        # Simulate trend data
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
    
    # Detailed alerts
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
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Resolve Alert", key=f"resolve_{alert['contract_id']}"):
                    st.success("Alert marked as resolved!")
            with col2:
                if st.button("Assign Task", key=f"assign_{alert['contract_id']}"):
                    st.info("Task assignment interface would open")
            with col3:
                if st.button("View Details", key=f"details_{alert['contract_id']}"):
                    st.info("Detailed compliance report would open")

def show_analytics(contracts_df):
    st.title("📈 Analytics & Reports")
    
    # Revenue analytics
    st.subheader("Revenue Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly revenue projection
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [2.1, 2.3, 2.5, 2.4, 2.6, 2.8]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=revenue, mode='lines+markers', name='Revenue (M$)'))
        fig.update_layout(title="Monthly Revenue Projection", yaxis_title="Revenue (Millions $)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Contract renewal timeline
        renewal_data = contracts_df[contracts_df['status'].isin(['Renewal Required', 'Active'])]
        renewal_data['end_date'] = pd.to_datetime(renewal_data['end_date'])
        renewal_data['months_to_renewal'] = (renewal_data['end_date'] - pd.Timestamp.now()).dt.days / 30
        
        fig = px.scatter(renewal_data, x='months_to_renewal', y='value', 
                        color='type', size='locations',
                        title="Contract Renewal Timeline")
        fig.update_xaxis(title="Months to Renewal")
        fig.update_yaxis(title="Contract Value ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
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

def show_contract_analysis():
    st.title("🔍 AI Contract Analysis")
    
    st.markdown("""
    Upload a contract document for automated analysis and key term extraction.
    Our AI system will identify critical clauses, compliance requirements, and potential risks.
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload Contract Document", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        st.success("Contract uploaded successfully!")
        
        # Simulate AI analysis
        with st.spinner("Analyzing contract..."):
            import time
            time.sleep(2)
        
        # Analysis results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Terms Extracted")
            st.json({
                "Contract Value": "$1,250,000",
                "Term Length": "24 months",
                "Service Type": "Commercial Waste Collection",
                "Payment Terms": "Net 30 days",
                "Termination Clause": "90 days notice required",
                "Renewal Option": "Automatic renewal",
                "Compliance Requirements": ["EPA regulations", "DOT certification", "State permits"]
            })
        
        with col2:
            st.subheader("Risk Assessment")
            risks = [
                {"Risk": "Late payment penalty", "Severity": "Medium", "Clause": "Section 4.2"},
                {"Risk": "Unlimited liability", "Severity": "High", "Clause": "Section 8.1"},
                {"Risk": "Auto-renewal without notice", "Severity": "Low", "Clause": "Section 12.3"}
            ]
            
            for risk in risks:
                severity_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                st.markdown(f"""
                {severity_color[risk['Severity']]} **{risk['Risk']}** ({risk['Severity']})  
                *Found in: {risk['Clause']}*
                """)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Generate Summary Report"):
                st.success("Contract summary report generated!")
        with col2:
            if st.button("Flag for Legal Review"):
                st.info("Contract flagged for legal team review")
        with col3:
            if st.button("Create Contract Record"):
                st.success("New contract record created in system!")

if __name__ == "__main__":
    main()