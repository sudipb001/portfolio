# 📊 Sales Analytics Dashboard

A beautiful, interactive analytics dashboard built with Streamlit and Supabase. This project demonstrates professional data visualization, real-time filtering, and comprehensive reporting capabilities.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-red)

## 🌟 Features

### 📈 Interactive Visualizations

- **Real-time KPI Cards**: Revenue, profit, units sold, and average order value
- **Time Series Analysis**: Daily revenue trends with interactive hover details
- **Regional Performance**: Bar charts showing revenue distribution across regions
- **Product Analysis**: Top-performing products with sortable metrics
- **Category Distribution**: Pie charts for category-wise revenue breakdown
- **Monthly Comparisons**: Grouped bar charts comparing revenue vs profit

### 🔍 Advanced Filtering

- **Date Range Picker**: Select custom date ranges for analysis
- **Multi-select Filters**: Filter by region, product, and category
- **Dynamic Updates**: All charts update instantly based on filter selections
- **Filter Combinations**: Apply multiple filters simultaneously

### 📊 Data Management

- **Supabase Integration**: Real-time data from Supabase PostgreSQL database
- **Sample Data Mode**: Automatically generates demo data if database not configured
- **Data Table View**: Interactive table with sorting and pagination
- **100+ records displayed**: Quick access to detailed transaction data

### 📥 Export Capabilities

- **CSV Export**: Download filtered data in CSV format
- **Excel Export**: Multi-sheet Excel files with summary statistics
- **PDF Reports**: Professional PDF reports with:
  - Executive summary with key metrics
  - Revenue breakdown by region
  - Top products analysis
  - Formatted tables with styling
  - Timestamp and filter information

### 🎨 Professional Design

- **Clean UI**: Modern, responsive interface
- **Custom Styling**: Branded colors and consistent design
- **Mobile Responsive**: Works on all device sizes
- **Dark Mode Support**: Streamlit's built-in theme compatibility

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Supabase account (optional - works with sample data)

### Installation

1. **Clone or download this project**

```bash
cd streamlit-analytics-dashboard
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables (optional)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Supabase credentials
# SUPABASE_URL=your_project_url
# SUPABASE_KEY=your_anon_key
```

5. **Run the application**

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 🗄️ Database Setup (Optional)

### Using Supabase

1. **Create a Supabase project**

   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Wait for setup to complete

2. **Run the SQL setup script**

   - In Supabase Dashboard, go to SQL Editor
   - Copy and paste the contents of `database/setup.sql`
   - Click "Run"

3. **Populate with sample data**

   ```bash
   python database/init_db.py
   ```

   - Follow the prompts to generate and upload sample data
   - Choose number of days to generate (default: 365)

4. **Get your credentials**
   - Go to Project Settings > API
   - Copy the Project URL and anon/public key
   - Add them to your `.env` file

### Database Schema

The `sales_data` table includes:

- `id`: Unique identifier (auto-generated)
- `date`: Transaction date
- `region`: Geographic region
- `product`: Product name
- `category`: Product category
- `revenue`: Transaction revenue
- `units_sold`: Number of units
- `customer_id`: Customer identifier
- `profit_margin`: Profit margin percentage
- `profit`: Calculated profit
- `created_at`: Record creation timestamp

## 📁 Project Structure

```
streamlit-analytics-dashboard/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
└── database/
    ├── setup.sql              # Supabase table creation script
    └── init_db.py             # Data population script
```

## 🎯 Use Cases

This dashboard is perfect for:

- **Portfolio Projects**: Demonstrate data visualization and dashboard building skills
- **Sales Analysis**: Real-world sales data analysis and reporting
- **Business Intelligence**: Executive-level reporting with KPIs
- **Data Science Interviews**: Showcase technical and analytical abilities
- **Client Demos**: Professional-looking analytics platform
- **Learning**: Understand Streamlit, Plotly, and Supabase integration

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[Plotly](https://plotly.com/python/)**: Interactive charts and graphs
- **[Supabase](https://supabase.com/)**: PostgreSQL database and backend
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[ReportLab](https://www.reportlab.com/)**: PDF generation
- **[OpenPyXL](https://openpyxl.readthedocs.io/)**: Excel file creation

## 📊 Dashboard Features in Detail

### Key Performance Indicators (KPIs)

The dashboard displays four primary metrics:

1. **Total Revenue**: Sum of all sales in the selected period
2. **Total Profit**: Total profit with average margin
3. **Units Sold**: Total units and transaction count
4. **Average Order Value**: Mean transaction value and units per order

### Visualization Components

1. **Daily Revenue Trend**

   - Line chart showing revenue over time
   - Hover for exact values and dates
   - Helps identify trends and seasonality

2. **Revenue by Region**

   - Horizontal bar chart comparing regional performance
   - Color-coded by revenue amount
   - Sortable by revenue

3. **Top Products**

   - Shows top 10 products by revenue
   - Useful for inventory and marketing decisions
   - Color-gradient visualization

4. **Category Distribution**

   - Donut chart showing revenue split by category
   - Percentage and value labels
   - Interactive legend

5. **Monthly Performance**
   - Grouped bar chart comparing revenue and profit
   - Side-by-side comparison for easy analysis
   - Shows trends across months

### Export Formats

**CSV Export**

- Raw data export
- Compatible with Excel, Google Sheets
- Includes all filtered records

**Excel Export**

- Professional multi-sheet workbook
- Sheet 1: Full sales data
- Sheet 2: Summary statistics
- Formatted and ready for presentations

**PDF Report**

- Executive summary page
- Key metrics table
- Regional breakdown
- Top products analysis
- Professional formatting
- Timestamped and branded

## 🔧 Customization

### Modify the Date Range

Edit the default date range in `app.py`:

```python
date_range = st.sidebar.date_input(
    "Date Range",
    value=(your_start_date, your_end_date),
    min_value=min_date,
    max_value=max_date
)
```

### Add New Metrics

Add custom KPIs in the metrics section:

```python
with col5:
    custom_metric = filtered_df['your_column'].sum()
    st.metric(
        label="Your Metric",
        value=f"${custom_metric:,.0f}"
    )
```

### Change Color Scheme

Modify the custom CSS in `app.py`:

```python
st.markdown("""
    <style>
    h1 {
        color: #your_color;  /* Change primary color */
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Charts

Use Plotly Express or Graph Objects:

```python
fig = px.bar(your_data, x='column1', y='column2', title='Your Chart')
st.plotly_chart(fig, use_container_width=True)
```

## 🐛 Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'streamlit'"

- **Solution**: Make sure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue**: Dashboard shows sample data instead of Supabase data

- **Solution**: Check your `.env` file has correct credentials. Test connection with `database/init_db.py`

**Issue**: "Error connecting to Supabase"

- **Solution**: Verify your Supabase project is active, credentials are correct, and RLS policies are configured

**Issue**: Charts not displaying

- **Solution**: Check browser console for errors. Try clearing browser cache or using a different browser

**Issue**: PDF export button doesn't work

- **Solution**: Ensure ReportLab is installed: `pip install reportlab`

## 📈 Performance Tips

- **Large Datasets**: The dashboard caches data for 10 minutes. Adjust TTL in `@st.cache_data(ttl=600)`
- **Slow Loading**: Reduce date range or add more specific filters
- **Memory Usage**: For datasets >1M rows, consider server-side aggregation in Supabase

## 🤝 Contributing

Suggestions and improvements are welcome! Some ideas:

- Add user authentication
- Implement real-time data streaming
- Add more chart types (heatmaps, scatter plots)
- Create custom themes
- Add email report scheduling
- Implement data forecasting

## 📄 License

This project is open source and available for portfolio and educational purposes.

## 🙏 Acknowledgments

- Built with ❤️ using Streamlit
- Powered by Supabase
- Visualizations by Plotly
- PDF generation by ReportLab

## 📞 Support

For questions or issues:

1. Check the Troubleshooting section
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Check Supabase docs: [supabase.com/docs](https://supabase.com/docs)

## 🎓 Learning Resources

- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)
- [Plotly Python Guide](https://plotly.com/python/)
- [Supabase Quickstart](https://supabase.com/docs/guides/getting-started)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Built for Portfolio**  
_Demonstrating: Data Visualization • Dashboard Development • Database Integration • PDF Reporting_
