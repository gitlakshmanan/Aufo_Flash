
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="KPI Tracking Board",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .metric-card {
    background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    margin: 5px 0;
    transition: all 0.3s ease;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .blink-card {
        animation: blink 1s infinite;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: 3px solid #ff4757;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.7; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
        100% { opacity: 1; }
    }
    .blink-date {
        animation: blink-date-animation 0.8s infinite;
        font-weight: bold;
        color: white;
        text-shadow: 0 0 10px rgba(255, 71, 87, 0.8);
    }
    @keyframes blink-date-animation {
        0% { 
            opacity: 1; 
            background: rgba(255, 71, 87, 0.2);
            color: white;
            text-shadow: 0 0 10px rgba(255, 71, 87, 0.8);
        }
        50% { 
            opacity: 0.5; 
            background: rgba(255, 71, 87, 0.6);
            color: #ffff00;
            text-shadow: 0 0 20px rgba(255, 113, 71, 1);
        }
        100% { 
            opacity: 1; 
            background: rgba(255, 71, 87, 0.2);
            color: white;
            text-shadow: 0 0 10px rgba(255, 71, 87, 0.8);
        }
    }
    .report-date {
        font-size: 14px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 6px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .service-type {
        font-size: 12px;
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-bottom: 8px;
        font-style: italic;
        padding: 2px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
    }
    .metric-value {
        font-size: 16px;
        font-weight: bold;
        color: white;
    }
    .metric-label {
        font-size: 10px;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-table {
        width: 100%;
        border-collapse: collapse;
    }
    .metric-table td {
        padding: 4px 3px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .metric-table tr:last-child td {
        border-bottom: none;
    }
    .sidebar-logo {
        text-align: center;
        padding: 25px 10px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    .sidebar-logo h2 {
        margin: 10px 0;
        font-size: 24px;
    }
    .sidebar-logo p {
        opacity: 0.9;
        font-size: 14px;
    }
    
    /* Alert section styles */
    .alert-container {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe3e3 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border-left: 5px solid #ff4757;
        box-shadow: 0 5px 15px rgba(255,71,87,0.1);
    }
    .alert-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(255,71,87,0.2);
    }
    .alert-header h3 {
        color: #ff4757;
        font-size: 24px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .alert-header span {
        background: #ff4757;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        margin-left: 15px;
    }
    .alert-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    .alert-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,71,87,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .alert-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(255,71,87,0.15);
    }
    .alert-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff4757, #ff6b81);
    }
    .alert-card.critical {
        border-left: 4px solid #ff4757;
    }
    .alert-card.warning {
        border-left: 4px solid #ffa502;
    }
    .alert-card.moderate {
        border-left: 4px solid #ffd32a;
    }
    .alert-date {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .alert-badge {
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    .badge-critical {
        background: #ff4757;
    }
    .badge-warning {
        background: #ffa502;
    }
    .badge-moderate {
        background: #ffd32a;
        color: #2c3e50;
    }
    .alert-details {
        display: flex;
        justify-content: space-between;
        margin: 10px 0;
        padding: 10px 0;
        border-top: 1px dashed #ddd;
        border-bottom: 1px dashed #ddd;
    }
    .alert-amount {
        text-align: center;
        flex: 1;
    }
    .alert-amount-label {
        font-size: 11px;
        color: #7f8c8d;
        text-transform: uppercase;
    }
    .alert-amount-value {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
    }
    .alert-amount-value.negative {
        color: #ff4757;
    }
    .alert-drop {
        text-align: center;
        padding: 10px;
        background: rgba(255,71,87,0.1);
        border-radius: 8px;
        margin-top: 10px;
    }
    .alert-drop-percentage {
        font-size: 24px;
        font-weight: bold;
        color: #ff4757;
    }
    .alert-drop-label {
        font-size: 12px;
        color: #7f8c8d;
    }
    .no-alerts {
        text-align: center;
        padding: 50px;
        background: linear-gradient(135deg, #f0f9f0 0%, #e6f3e6 100%);
        border-radius: 15px;
        border-left: 5px solid #2ecc71;
    }
    .no-alerts h4 {
        color: #27ae60;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .no-alerts p {
        color: #7f8c8d;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'sheet_names' not in st.session_state:
    st.session_state.sheet_names = []
if 'selected_sheet' not in st.session_state:
    st.session_state.selected_sheet = None

# Function to load and process data
@st.cache_data
def load_data(uploaded_file, sheet_name):
    try:
        if uploaded_file is not None:
            # Get sheet names first
            xl = pd.ExcelFile(uploaded_file)
            sheet_names = xl.sheet_names
            
            # Read the selected sheet
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            # Check if required columns exist (case-insensitive)
            required_columns = ['ServiceType', 'Reportdate', 'Total', 'Amount']
            df_columns_upper = [col.lower() for col in df.columns]
            required_columns_lower = [col.lower() for col in required_columns]
            
            if all(col in df_columns_upper for col in required_columns_lower):
                # Rename columns to match required format (preserve original case for display)
                column_mapping = {}
                for req_col in required_columns:
                    for df_col in df.columns:
                        if df_col.lower() == req_col.lower():
                            column_mapping[df_col] = req_col
                            break
                
                if column_mapping:
                    df = df.rename(columns=column_mapping)
                
                # Convert Reportdate to datetime
                df['Reportdate'] = pd.to_datetime(df['Reportdate'])
                
                return df, sheet_names
            else:
                missing_cols = [col for col in required_columns if col.lower() not in df_columns_upper]
                st.error(f"Sheet must contain columns: {', '.join(required_columns)}. Missing: {', '.join(missing_cols)}")
                return None, sheet_names
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None, []
    
    return None, []

# Function to filter data based on selections
def filter_data(df, from_date, to_date, service_type):
    mask = (df['Reportdate'].dt.date >= from_date) & \
           (df['Reportdate'].dt.date <= to_date) & \
           (df['ServiceType'] == service_type)
    return df.loc[mask]

# Function to detect drastic changes between dates
def detect_drastic_changes(current_data, prev_data=None):
    """Detect drastic changes in qty and amount"""
    if prev_data is None or prev_data.empty:
        return False
    
    curr_qty = current_data['Total'].sum()
    curr_amount = current_data['Amount'].sum()
    
    prev_qty = prev_data['Total'].sum()
    prev_amount = prev_data['Amount'].sum()
    
    # Calculate percentage changes
    qty_change = abs((curr_qty - prev_qty) / prev_qty * 100) if prev_qty > 0 else 0
    amount_change = abs((curr_amount - prev_amount) / prev_amount * 100) if prev_amount > 0 else 0
    
    # Trigger blink if change >= 20%
    return qty_change >= 20 or amount_change >= 20

# Function to create metric card with differences
def create_metric_card(data, report_date, service_type, prev_data=None, is_drastic=False):
    card_class = "metric-card"
    date_class = "blink-date" if is_drastic else ""
    
    # Calculate metrics
    total_qty = data['Total'].sum()
    sum_amount = data['Amount'].sum()
    
    # Calculate differences if previous data exists
    diff_qty = 0
    diff_amount = 0
    qty_change_pct = 0
    amount_change_pct = 0
    
    if prev_data is not None and not prev_data.empty:
        prev_qty = prev_data['Total'].sum()
        prev_amount = prev_data['Amount'].sum()
        
        diff_qty = total_qty - prev_qty
        diff_amount = sum_amount - prev_amount
        
        if prev_qty > 0:
            qty_change_pct = (diff_qty / prev_qty) * 100
        if prev_amount > 0:
            amount_change_pct = (diff_amount / prev_amount) * 100
    
    # Format date with day name
    date_str = report_date.strftime('%Y-%m-%d (%A)')
    
    # Determine color for differences
    qty_color = "#2ecc71" if diff_qty >= 0 else "#ff4757"
    amount_color = "#2ecc71" if diff_amount >= 0 else "#ff4757"
    
    card_html = f"""
    <div class="{card_class}">
        <div class="report-date {date_class}">📅 {date_str}</div>
        <div class="service-type">{service_type}</div>
        <table class="metric-table">
            <tr>
                <td><span class="metric-label">Total Qty</span><br><span class="metric-value">{total_qty:,.0f}</span></td>
                <td><span class="metric-label">Δ Qty</span><br><span class="metric-value" style="color: {qty_color};">{diff_qty:+.0f}</span></td>
            </tr>
            <tr>
                <td><span class="metric-label">Amount</span><br><span class="metric-value">${sum_amount:,.0f}</span></td>
                <td><span class="metric-label">Δ Amount</span><br><span class="metric-value" style="color: {amount_color};">${diff_amount:+,.0f}</span></td>
            </tr>
            <tr>
                <td colspan="2" style="text-align: center; font-size: 9px; color: rgba(255,255,255,0.7);">
                    Qty: {qty_change_pct:+.1f}% | Amount: {amount_change_pct:+.1f}%
                </td>
            </tr>
        </table>
    </div>
    """
    
    return card_html

# Function to detect daily and weekly changes
def detect_daily_and_weekly_changes(data):
    """Detect drastic changes in qty and amount at daily and weekly levels"""
    if len(data) < 2:
        return []
    
    data_sorted = data.sort_values('Reportdate')
    changes = []
    
    for i in range(1, len(data_sorted)):
        prev_row = data_sorted.iloc[i-1]
        curr_row = data_sorted.iloc[i]
        
        prev_qty = prev_row['Total']
        prev_amount = prev_row['Amount']
        curr_qty = curr_row['Total']
        curr_amount = curr_row['Amount']
        
        # Calculate percentage changes
        qty_change = ((curr_qty - prev_qty) / prev_qty * 100) if prev_qty > 0 else 0
        amount_change = ((curr_amount - prev_amount) / prev_amount * 100) if prev_amount > 0 else 0
        
        # Check for drastic changes (20% or more)
        if abs(qty_change) >= 20 or abs(amount_change) >= 20:
            # Determine severity
            max_change = max(abs(qty_change), abs(amount_change))
            if max_change >= 50:
                severity = "critical"
            elif max_change >= 30:
                severity = "warning"
            else:
                severity = "moderate"
            
            changes.append({
                'date': curr_row['Reportdate'],
                'prev_date': prev_row['Reportdate'],
                'qty_change': qty_change,
                'amount_change': amount_change,
                'prev_qty': prev_qty,
                'curr_qty': curr_qty,
                'prev_amount': prev_amount,
                'curr_amount': curr_amount,
                'severity': severity,
                'change_type': 'daily'
            })
    
    return changes

# Function to create change alert card
def create_change_alert_card(alert):
    severity = alert['severity']
    badge_class = f"badge-{severity}"
    change_type = alert['change_type'].upper()
    
    if severity == "critical":
        severity_text = "Critical Change"
    elif severity == "warning":
        severity_text = "Warning"
    else:
        severity_text = "Moderate Change"
    
    qty_color = "#2ecc71" if alert['qty_change'] >= 0 else "#ff4757"
    amount_color = "#2ecc71" if alert['amount_change'] >= 0 else "#ff4757"
    
    card_html = f"""
    <div class="alert-card {severity}">
        <div class="alert-date">
            <span>📅 {alert['date'].strftime('%Y-%m-%d (%A)')}</span>
            <span class="alert-badge {badge_class}">{severity_text}</span>
        </div>
        <div style="font-size: 10px; color: #95a5a6; text-align: center; margin: 5px 0;">
            {change_type}
        </div>
        <div class="alert-details">
            <div class="alert-amount">
                <div class="alert-amount-label">Qty Change</div>
                <div class="alert-amount-value" style="color: {qty_color};">{alert['qty_change']:+.1f}%</div>
                <div style="font-size: 9px; color: #95a5a6;">{alert['prev_qty']:.0f} → {alert['curr_qty']:.0f}</div>
            </div>
            <div class="alert-amount">
                <div class="alert-amount-label">Amount Change</div>
                <div class="alert-amount-value" style="color: {amount_color};">{alert['amount_change']:+.1f}%</div>
                <div style="font-size: 9px; color: #95a5a6;">${alert['prev_amount']:.0f} → ${alert['curr_amount']:.0f}</div>
            </div>
        </div>
    </div>
    """
    return card_html

# Function to create alert card
def create_alert_card(alert):
    severity = alert['severity']
    badge_class = f"badge-{severity}"
    
    if severity == "critical":
        severity_text = "Critical Drop"
    elif severity == "warning":
        severity_text = "Warning"
    else:
        severity_text = "Moderate Drop"
    
    card_html = f"""
    <div class="alert-card {severity}">
        <div class="alert-date">
            <span>📅 {alert['date'].strftime('%Y-%m-%d')}</span>
            <span class="alert-badge {badge_class}">{severity_text}</span>
        </div>
        <div class="alert-drop">
            <div class="alert-drop-percentage">{alert['drop_percentage']:.1f}%</div>
            <div class="alert-drop-label">Revenue Drop</div>
        </div>
        <div class="alert-details">
            <div class="alert-amount">
                <div class="alert-amount-label">Previous</div>
                <div class="alert-amount-value">${alert['prev_amount']:,.2f}</div>
            </div>
            <div class="alert-amount">
                <div class="alert-amount-label">→</div>
            </div>
            <div class="alert-amount">
                <div class="alert-amount-label">Current</div>
                <div class="alert-amount-value negative">${alert['curr_amount']:,.2f}</div>
            </div>
        </div>
        <div style="font-size: 11px; color: #95a5a6; text-align: center; margin-top: 5px;">
            Loss: ${alert['prev_amount'] - alert['curr_amount']:,.2f}
        </div>
    </div>
    """
    return card_html

# Sidebar
with st.sidebar:
    # Logo placeholder with enhanced styling
    st.markdown("""
    <div class="sidebar-logo">
        <h2>📊 Analytics Dashboard</h2>
        <p>Service Performance Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader("📁 Upload Excel File", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Get sheet names
        try:
            xl = pd.ExcelFile(uploaded_file)
            st.session_state.sheet_names = xl.sheet_names
            
            # Sheet selector
            if len(st.session_state.sheet_names) > 0:
                st.session_state.selected_sheet = st.selectbox(
                    "📑 Select Sheet",
                    st.session_state.sheet_names,
                    index=min(1, len(st.session_state.sheet_names)-1)  # Default to second sheet if available
                )
                
                # Load data with selected sheet
                if st.button("🔄 Load Data"):
                    with st.spinner("Loading data..."):
                        st.session_state.data, _ = load_data(uploaded_file, st.session_state.selected_sheet)
                        if st.session_state.data is not None:
                            st.success(f"✅ Data loaded successfully from '{st.session_state.selected_sheet}'")
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
    
    st.markdown("---")
    
    # Date and service type selectors
    if st.session_state.data is not None:
        st.markdown("### 🔍 Filters")
        
        # Get min and max dates
        min_date = st.session_state.data['Reportdate'].min().date()
        max_date = st.session_state.data['Reportdate'].max().date()
        
        # Date inputs
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date", min_date, min_value=min_date, max_value=max_date)
        with col2:
            to_date = st.date_input("To Date", max_date, min_value=min_date, max_value=max_date)
        
        # Service type selector
        service_types = st.session_state.data['ServiceType'].unique().tolist()
        selected_service = st.selectbox("Service Type", service_types)
        
        # Apply filters button
        if st.button("📊 Apply Filters", use_container_width=True):
            if from_date <= to_date:
                st.session_state.filtered_data = filter_data(
                    st.session_state.data, from_date, to_date, selected_service
                )
                if st.session_state.filtered_data.empty:
                    st.warning("No data available for the selected filters")
                else:
                    st.success(f"Found {len(st.session_state.filtered_data)} records")
            else:
                st.error("From Date must be less than or equal to To Date")
    else:
        st.info("👈Please upload an Excel file and load data to begin")

# Function: Time Series Forecast using Linear Regression
def forecast_revenue(daily_summary, forecast_days=30):
    df = daily_summary.copy()
    df = df.sort_values("Reportdate")

    # Convert date to ordinal (numeric)
    df["date_ordinal"] = df["Reportdate"].map(datetime.toordinal)

    X = df[["date_ordinal"]]
    y = df["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    # Create future dates
    last_date = df["Reportdate"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
    future_ordinals = [[d.toordinal()] for d in future_dates]

    predictions = model.predict(future_ordinals)

    forecast_df = pd.DataFrame({
        "Reportdate": future_dates,
        "PredictedAmount": predictions
    })

    return forecast_df


# Main content area
st.title("📊 KPI Dashboard")
#st.info("👈 Please upload Excel file => see the button on the left panel")

if st.session_state.filtered_data is not None and not st.session_state.filtered_data.empty:
    filtered_data = st.session_state.filtered_data
    
    # First Section - Metric Cards
    st.header("📈 Daily Performance Metrics")
    
    # Group by date
    grouped_data = filtered_data.groupby('Reportdate')
    unique_dates = sorted(list(grouped_data.groups.keys()))
    
    # Detect drastic changes for all dates
    drastic_dates = set()
    prev_group = None
    for date in unique_dates:
        group = grouped_data.get_group(date)
        is_drastic = detect_drastic_changes(group, prev_group)
        if is_drastic:
            drastic_dates.add(date)
        prev_group = group
    
    # Create rows of metric cards (4 per row)
    for i in range(0, len(unique_dates), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(unique_dates):
                date = unique_dates[i + j]
                group = grouped_data.get_group(date)
                
                # Get previous day data if available
                prev_data = None
                if i + j > 0:
                    prev_date = unique_dates[i + j - 1]
                    prev_data = grouped_data.get_group(prev_date)
                
                is_drastic = date in drastic_dates
                
                with cols[j]:
                    card_html = create_metric_card(group, date, selected_service, prev_data, is_drastic)
                    st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Second Section - Analysis Graphs
    st.header("📊 Revenue Analysis")
    
    # Prepare data for analysis
    daily_summary = filtered_data.groupby('Reportdate').agg({
        'Amount': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    daily_summary['Week'] = daily_summary['Reportdate'].dt.isocalendar().week
    daily_summary['Month'] = daily_summary['Reportdate'].dt.month
    daily_summary['Quarter'] = daily_summary['Reportdate'].dt.quarter
    daily_summary['DayOfWeek'] = daily_summary['Reportdate'].dt.day_name()
    daily_summary['WeekOfYear'] = daily_summary['Reportdate'].dt.isocalendar().week
    
    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Comparisons", "📉 Statistics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily Revenue Trend
            fig1 = px.line(daily_summary, x='Reportdate', y='Amount', 
                          title='📈 Daily Revenue Trend',
                          markers=True, line_shape='linear')
            fig1.update_traces(line=dict(color='#667eea', width=3), 
                              marker=dict(size=8, color='#764ba2'))
            fig1.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Daily Quantity Trend
            fig2 = px.line(daily_summary, x='Reportdate', y='Total',
                          title='📦 Daily Quantity Trend',
                          markers=True, line_shape='linear')
            fig2.update_traces(line=dict(color='#f093fb', width=3),
                              marker=dict(size=8, color='#f5576c'))
            fig2.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly Analysis
            weekly_avg = daily_summary.groupby('DayOfWeek')['Amount'].agg(['mean', 'sum']).reset_index()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_avg['DayOfWeek'] = pd.Categorical(weekly_avg['DayOfWeek'], categories=day_order, ordered=True)
            weekly_avg = weekly_avg.sort_values('DayOfWeek')
            
            fig3 = px.bar(weekly_avg, x='DayOfWeek', y='mean',
                         title='📊 Average Revenue by Day of Week',
                         color='mean', color_continuous_scale='Viridis',
                         labels={'mean': 'Avg Revenue ($)'})
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Monthly Comparison
            monthly_summary = daily_summary.groupby('Month')['Amount'].sum().reset_index()
            fig4 = px.bar(monthly_summary, x='Month', y='Amount',
                         title='📊 Monthly Revenue Comparison',
                         color='Amount', color_continuous_scale='Plasma',
                         labels={'Amount': 'Total Revenue ($)'})
            fig4.update_layout(height=400)
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Quarterly Analysis
            quarterly_summary = daily_summary.groupby('Quarter')['Amount'].sum().reset_index()
            fig5 = px.pie(quarterly_summary, values='Amount', names='Quarter',
                         title='🥧 Quarterly Revenue Distribution',
                         color_discrete_sequence=px.colors.qualitative.Set3,
                         hole=0.4)
            fig5.update_layout(height=400)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # Week over Week Comparison
            weekly_totals = daily_summary.groupby('WeekOfYear')['Amount'].sum().reset_index()
            if len(weekly_totals) > 1:
                fig6 = px.bar(weekly_totals, x='WeekOfYear', y='Amount',
                             title='📊 Weekly Revenue Comparison',
                             color='Amount', color_continuous_scale='Magma')
                fig6.update_layout(height=400)
                st.plotly_chart(fig6, use_container_width=True)
    
    # Key Insights
    st.subheader("💡 Key Insights")
    
    insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
    
    if not daily_summary.empty:
        # Highest revenue day
        max_revenue = daily_summary.loc[daily_summary['Amount'].idxmax()]
        with insight_col1:
            st.metric("🏆 Highest Revenue Day", 
                     max_revenue['Reportdate'].strftime('%Y-%m-%d'),
                     f"${max_revenue['Amount']:,.0f}")
        
        # Average daily revenue
        avg_revenue = daily_summary['Amount'].mean()
        with insight_col2:
            st.metric("📊 Avg Daily Revenue", 
                     f"${avg_revenue:,.0f}")
        
        # Total revenue
        total_revenue = daily_summary['Amount'].sum()
        with insight_col3:
            st.metric("💰 Total Revenue", 
                     f"${total_revenue:,.0f}")
        
        # Total quantity
        total_qty = daily_summary['Total'].sum()
        with insight_col4:
            st.metric("📦 Total Quantity", 
                     f"{total_qty:,.0f}")
        
        # Week over Week comparison (if enough data)
        if len(daily_summary) >= 14:
            last_week = daily_summary['Amount'].tail(7).sum()
            previous_week = daily_summary['Amount'].tail(14).head(7).sum()
            if previous_week > 0:
                week_change = ((last_week - previous_week) / previous_week) * 100
                st.info(f"📊 **Week-over-Week Change:** {week_change:+.1f}%")
    
    st.markdown("---")
    
    # Detect changes (Qty and Amount)
    changes = detect_daily_and_weekly_changes(filtered_data)
    
    # Third Section - Alerts (Daily and Weekly Changes)
    st.markdown("""
    <div class="alert-container">
        <div class="alert-header">
            <h3>🚨 Qty & Amount Changes</h3>
            <span>{}</span>
        </div>
    """.format(f"{len(changes)} Alert(s)"), unsafe_allow_html=True)
    
    if changes:
        # Sort changes by severity
        critical_changes = [c for c in changes if c['severity'] == 'critical']
        warning_changes = [c for c in changes if c['severity'] == 'warning']
        moderate_changes = [c for c in changes if c['severity'] == 'moderate']
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Changes", len(changes))
        with col2:
            st.metric("Critical (≥50%)", len(critical_changes), delta=f"{len(critical_changes)} critical")
        with col3:
            st.metric("Warning (30-49%)", len(warning_changes))
        with col4:
            st.metric("Moderate (20-29%)", len(moderate_changes))
        
        # Display critical changes first
        if critical_changes:
            st.markdown("#### 🔴 Critical Changes (≥50%)")
            critical_cols = st.columns(3)
            for idx, change in enumerate(critical_changes[:6]):
                with critical_cols[idx % 3]:
                    st.markdown(create_change_alert_card(change), unsafe_allow_html=True)
            if len(critical_changes) > 6:
                st.info(f"... and {len(critical_changes) - 6} more critical changes")
        
        # Display warning changes
        if warning_changes:
            st.markdown("#### 🟠 Warning Changes (30-49%)")
            warning_cols = st.columns(3)
            for idx, change in enumerate(warning_changes[:6]):
                with warning_cols[idx % 3]:
                    st.markdown(create_change_alert_card(change), unsafe_allow_html=True)
            if len(warning_changes) > 6:
                st.info(f"... and {len(warning_changes) - 6} more warning changes")
        
        # Display moderate changes
        if moderate_changes:
            st.markdown("#### 🟡 Moderate Changes (20-29%)")
            moderate_cols = st.columns(3)
            for idx, change in enumerate(moderate_changes[:6]):
                with moderate_cols[idx % 3]:
                    st.markdown(create_change_alert_card(change), unsafe_allow_html=True)
            if len(moderate_changes) > 6:
                st.info(f"... and {len(moderate_changes) - 6} more moderate changes")
        
        # Show change pattern analysis
        st.markdown("### 📊 Change Pattern Analysis")
        pattern_col1, pattern_col2 = st.columns(2)
        
        with pattern_col1:
            # Create a time series of changes
            change_dates = [c['date'] for c in changes]
            qty_changes = [c['qty_change'] for c in changes]
            
            fig_qty = px.scatter(x=change_dates, y=qty_changes,
                                title='Quantity Changes Over Time',
                                labels={'x': 'Date', 'y': 'Change (%)'},
                                color=qty_changes,
                                color_continuous_scale='RdYlGn',
                                color_continuous_midpoint=0)
            fig_qty.add_hline(y=50, line_dash="dash", line_color="red", 
                             annotation_text="Critical Threshold")
            fig_qty.add_hline(y=-50, line_dash="dash", line_color="red")
            fig_qty.add_hline(y=20, line_dash="dot", line_color="orange")
            fig_qty.add_hline(y=-20, line_dash="dot", line_color="orange")
            fig_qty.update_layout(height=300)
            st.plotly_chart(fig_qty, use_container_width=True)
        
        with pattern_col2:
            # Amount changes over time
            amount_changes = [c['amount_change'] for c in changes]
            
            fig_amount = px.scatter(x=change_dates, y=amount_changes,
                                   title='Amount Changes Over Time',
                                   labels={'x': 'Date', 'y': 'Change (%)'},
                                   color=amount_changes,
                                   color_continuous_scale='RdYlGn',
                                   color_continuous_midpoint=0)
            fig_amount.add_hline(y=50, line_dash="dash", line_color="red",
                                annotation_text="Critical Threshold")
            fig_amount.add_hline(y=-50, line_dash="dash", line_color="red")
            fig_amount.add_hline(y=20, line_dash="dot", line_color="orange")
            fig_amount.add_hline(y=-20, line_dash="dot", line_color="orange")
            fig_amount.update_layout(height=300)
            st.plotly_chart(fig_amount, use_container_width=True)
        
        # Change severity distribution
        st.markdown("### 📊 Change Severity Distribution")
        severity_counts = {
            'Critical (≥50%)': len(critical_changes),
            'Warning (30-49%)': len(warning_changes),
            'Moderate (20-29%)': len(moderate_changes)
        }
        fig_dist = px.pie(values=list(severity_counts.values()), 
                         names=list(severity_counts.keys()),
                         title='Change Severity Distribution',
                         color_discrete_sequence=['#ff4757', '#ffa502', '#ffd32a'])
        fig_dist.update_layout(height=350)
        st.plotly_chart(fig_dist, use_container_width=True)
        
    else:
        st.markdown("""
        <div class="no-alerts">
            <h4>✅ No Drastic Changes Detected</h4>
            <p>All changes are within normal range (less than 20% change)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
else:
    if st.session_state.data is not None:
        st.info("👆 Please apply filters using the sidebar to view data")
        
        # Show sample of available data
        st.subheader("📋 Available Data Sample:")
        st.info("👇 The uploaded data set is not real time data an its a sample data")
        st.dataframe(st.session_state.data.head(10), use_container_width=True)
        
        # Show data summary
        st.subheader("📊 Data Summary:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(st.session_state.data))
        with col2:
            st.metric("Date Range", f"{st.session_state.data['Reportdate'].min().date()} to {st.session_state.data['Reportdate'].max().date()}")
        with col3:
            st.metric("Service Types", len(st.session_state.data['ServiceType'].unique()))
    else:
        st.info("👈 Please upload an Excel file using the sidebar to begin analysis")
        
        # Sample data structure
        st.subheader("📋 Expected Excel Structure:")
        st.markdown("""
        Your Excel file should contain a sheet with the following columns:
        - **ServiceType** (e.g., Fulfillment, Clean & Screen)
        - **Reportdate** (date format)
        - **Total** (numeric quantity)
        - **Amount** (numeric amount/revenue)
        """)
        
        sample_data = pd.DataFrame({
            'ServiceType': ['Fulfillment', 'Fulfillment', 'Clean & Screen', 'Clean & Screen'],
            'Reportdate': [datetime.now().date(), datetime.now().date() - timedelta(days=1),
                          datetime.now().date(), datetime.now().date() - timedelta(days=1)],
            'Total': [100, 85, 150, 120],
            'Amount': [1000.00, 850.00, 2250.00, 1800.00]
        })
        st.dataframe(sample_data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 10px;'>
    Developed by Lakshmanan Chelliah | Data updates daily | Version 2.0
</div>
""", unsafe_allow_html=True)