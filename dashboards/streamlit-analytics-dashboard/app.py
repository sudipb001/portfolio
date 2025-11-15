import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from supabase import create_client, Client
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import tempfile

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric label {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c3e50;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")
    
    if url and key:
        return create_client(url, key)
    return None

# Load data from Supabase or use sample data
@st.cache_data(ttl=600)
def load_data():
    supabase = init_supabase()
    
    # Try to load from Supabase
    if supabase:
        try:
            response = supabase.table('sales_data').select("*").execute()
            if response.data:
                df = pd.DataFrame(response.data)
                df['date'] = pd.to_datetime(df['date'])
                return df
        except Exception as e:
            st.warning(f"Using sample data. Supabase connection: {str(e)}")
    
    # Generate sample data if Supabase is not configured
    return generate_sample_data()

def generate_sample_data():
    """Generate realistic sample sales data"""
    import numpy as np
    
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    categories = ['Electronics', 'Software', 'Services', 'Hardware', 'Accessories']
    
    data = []
    for date in dates:
        for _ in range(np.random.randint(3, 8)):
            data.append({
                'date': date,
                'region': np.random.choice(regions),
                'product': np.random.choice(products),
                'category': np.random.choice(categories),
                'revenue': np.random.uniform(1000, 50000),
                'units_sold': np.random.randint(1, 100),
                'customer_id': f'CUST-{np.random.randint(1000, 9999)}'
            })
    
    df = pd.DataFrame(data)
    df['profit_margin'] = np.random.uniform(0.15, 0.45, len(df))
    df['profit'] = df['revenue'] * df['profit_margin']
    
    return df

def create_pdf_report(df, filtered_df, date_range, selected_regions, selected_products):
    """Generate a professional PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("Sales Analytics Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    metadata = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
    metadata += f"Date Range: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}<br/>"
    metadata += f"Regions: {', '.join(selected_regions) if selected_regions else 'All'}<br/>"
    metadata += f"Products: {', '.join(selected_products) if selected_products else 'All'}"
    
    story.append(Paragraph(metadata, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Revenue', f"${filtered_df['revenue'].sum():,.2f}"],
        ['Total Profit', f"${filtered_df['profit'].sum():,.2f}"],
        ['Total Units Sold', f"{filtered_df['units_sold'].sum():,}"],
        ['Average Order Value', f"${filtered_df['revenue'].mean():,.2f}"],
        ['Number of Transactions', f"{len(filtered_df):,}"],
        ['Average Profit Margin', f"{filtered_df['profit_margin'].mean():.1%}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Revenue by Region
    story.append(Paragraph("Revenue by Region", heading_style))
    
    region_data = filtered_df.groupby('region').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'units_sold': 'sum'
    }).reset_index().sort_values('revenue', ascending=False)
    
    region_table_data = [['Region', 'Revenue', 'Profit', 'Units Sold']]
    for _, row in region_data.iterrows():
        region_table_data.append([
            row['region'],
            f"${row['revenue']:,.2f}",
            f"${row['profit']:,.2f}",
            f"{int(row['units_sold']):,}"
        ])
    
    region_table = Table(region_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    region_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(region_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Top Products
    story.append(Paragraph("Top 10 Products by Revenue", heading_style))
    
    product_data = filtered_df.groupby('product')['revenue'].sum().reset_index()
    product_data = product_data.sort_values('revenue', ascending=False).head(10)
    
    product_table_data = [['Product', 'Revenue']]
    for _, row in product_data.iterrows():
        product_table_data.append([row['product'], f"${row['revenue']:,.2f}"])
    
    product_table = Table(product_table_data, colWidths=[3*inch, 2*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(product_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main app
def main():
    st.title("📊 Sales Analytics Dashboard")
    st.markdown("### Real-time Business Intelligence & Reporting")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    # Region filter
    regions = ['All'] + sorted(df['region'].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Region",
        options=regions,
        default=['All']
    )
    
    # Product filter
    products = ['All'] + sorted(df['product'].unique().tolist())
    selected_products = st.sidebar.multiselect(
        "Product",
        options=products,
        default=['All']
    )
    
    # Category filter
    categories = ['All'] + sorted(df['category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Category",
        options=categories,
        default=['All']
    )
    
    # Apply filters
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) &
        (filtered_df['date'].dt.date <= end_date)
    ]
    
    if 'All' not in selected_regions:
        filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
    
    if 'All' not in selected_products:
        filtered_df = filtered_df[filtered_df['product'].isin(selected_products)]
    
    if 'All' not in selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    # Key Metrics
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_df['revenue'].sum()
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{(total_revenue / df['revenue'].sum() * 100):.1f}% of total"
        )
    
    with col2:
        total_profit = filtered_df['profit'].sum()
        avg_margin = filtered_df['profit_margin'].mean()
        st.metric(
            label="Total Profit",
            value=f"${total_profit:,.0f}",
            delta=f"{avg_margin:.1%} margin"
        )
    
    with col3:
        total_units = filtered_df['units_sold'].sum()
        st.metric(
            label="Units Sold",
            value=f"{total_units:,}",
            delta=f"{len(filtered_df):,} transactions"
        )
    
    with col4:
        avg_order = filtered_df['revenue'].mean()
        st.metric(
            label="Avg Order Value",
            value=f"${avg_order:,.2f}",
            delta=f"{filtered_df['units_sold'].mean():.1f} units/order"
        )
    
    # Charts row 1
    st.header("📊 Revenue Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue over time
        daily_revenue = filtered_df.groupby(filtered_df['date'].dt.date)['revenue'].sum().reset_index()
        daily_revenue.columns = ['Date', 'Revenue']
        
        fig_timeline = px.line(
            daily_revenue,
            x='Date',
            y='Revenue',
            title='Daily Revenue Trend',
            labels={'Revenue': 'Revenue ($)'},
            template='plotly_white'
        )
        fig_timeline.update_traces(line_color='#1f77b4', line_width=2)
        fig_timeline.update_layout(hovermode='x unified')
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Revenue by region
        region_revenue = filtered_df.groupby('region')['revenue'].sum().reset_index()
        region_revenue = region_revenue.sort_values('revenue', ascending=False)
        
        fig_region = px.bar(
            region_revenue,
            x='region',
            y='revenue',
            title='Revenue by Region',
            labels={'revenue': 'Revenue ($)', 'region': 'Region'},
            template='plotly_white',
            color='revenue',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Product performance
        product_stats = filtered_df.groupby('product').agg({
            'revenue': 'sum',
            'units_sold': 'sum'
        }).reset_index().sort_values('revenue', ascending=False)
        
        fig_products = px.bar(
            product_stats.head(10),
            x='product',
            y='revenue',
            title='Top 10 Products by Revenue',
            labels={'revenue': 'Revenue ($)', 'product': 'Product'},
            template='plotly_white',
            color='revenue',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        # Category distribution
        category_revenue = filtered_df.groupby('category')['revenue'].sum().reset_index()
        
        fig_category = px.pie(
            category_revenue,
            values='revenue',
            names='category',
            title='Revenue Distribution by Category',
            template='plotly_white',
            hole=0.4
        )
        fig_category.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Monthly comparison
    st.header("📅 Monthly Performance")
    
    monthly_data = filtered_df.copy()
    monthly_data['month'] = monthly_data['date'].dt.to_period('M').astype(str)
    
    monthly_metrics = monthly_data.groupby('month').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'units_sold': 'sum'
    }).reset_index()
    
    fig_monthly = go.Figure()
    
    fig_monthly.add_trace(go.Bar(
        x=monthly_metrics['month'],
        y=monthly_metrics['revenue'],
        name='Revenue',
        marker_color='#1f77b4'
    ))
    
    fig_monthly.add_trace(go.Bar(
        x=monthly_metrics['month'],
        y=monthly_metrics['profit'],
        name='Profit',
        marker_color='#2ca02c'
    ))
    
    fig_monthly.update_layout(
        title='Monthly Revenue vs Profit',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        barmode='group',
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Data table
    st.header("📋 Detailed Data")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Showing {len(filtered_df):,} records**")
    with col2:
        show_all = st.checkbox("Show all columns")
    
    if show_all:
        display_df = filtered_df
    else:
        display_df = filtered_df[['date', 'region', 'product', 'category', 'revenue', 'profit', 'units_sold']]
    
    st.dataframe(
        display_df.sort_values('date', ascending=False).head(100),
        use_container_width=True,
        hide_index=True
    )
    
    # Export section
    st.header("📥 Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV export
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    
    with col2:
        # Excel export
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Sales Data', index=False)
            
            # Add summary sheet
            summary_df = pd.DataFrame({
                'Metric': ['Total Revenue', 'Total Profit', 'Total Units Sold', 'Avg Order Value', 'Transactions'],
                'Value': [
                    f"${total_revenue:,.2f}",
                    f"${total_profit:,.2f}",
                    f"{total_units:,}",
                    f"${avg_order:,.2f}",
                    f"{len(filtered_df):,}"
                ]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        excel_buffer.seek(0)
        st.download_button(
            label="📊 Download Excel",
            data=excel_buffer,
            file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    
    with col3:
        # PDF export
        if st.button("📑 Generate PDF Report"):
            with st.spinner("Generating PDF report..."):
                pdf_buffer = create_pdf_report(
                    df, 
                    filtered_df, 
                    (start_date, end_date),
                    selected_regions if 'All' not in selected_regions else [],
                    selected_products if 'All' not in selected_products else []
                )
                
                st.download_button(
                    label="📑 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                )
                st.success("PDF report generated successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Built with Streamlit, Plotly & Supabase"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
