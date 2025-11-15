# app.py
# Multi-page Streamlit analytics dashboard (Portfolio v2)
# Note: Ensure dependencies in requirements.txt are installed.
import streamlit as st
import pandas as pd
import altair as alt
from supabase import create_client
from datetime import date, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@st.cache_resource
def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("Set SUPABASE_URL and SUPABASE_KEY in your environment or .env file.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=300)
def load_sales(client):
    res = client.table("sales").select("*").order("sale_date").execute()
    data = res.get("data", []) if isinstance(res, dict) else getattr(res, "data", [])
    df = pd.DataFrame(data)
    if not df.empty:
        if "sale_date" in df.columns:
            df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.date
        if "revenue" in df.columns:
            df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
        if "quantity" in df.columns:
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    return df

def export_chart_png(chart):
    # Altair charts can be converted to PNG if altair_saver + selenium or node is available.
    # Here we attempt to use the built-in to_image (works when altair_saver is configured).
    try:
        png = chart.to_image(format="png")
        return png
    except Exception as e:
        st.warning("Chart export to PNG failed in this environment. PDF will include available charts only if PNG conversion works locally.")
        return None

def pdf_with_charts(title, summary, chart_images, table_df=None):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    y = h - 2*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, y, title)
    y -= 20
    c.setFont("Helvetica", 10)
    for k, v in summary.items():
        c.drawString(2*cm, y, f"{k}: {v}")
        y -= 12
    y -= 6
    for img in chart_images:
        if img is None:
            continue
        if y < 10*cm:
            c.showPage()
            y = h - 2*cm
        # Insert image (scale to fit)
        try:
            c.drawImage(BytesIO(img), 2*cm, y-8*cm, width=16*cm, height=8*cm, preserveAspectRatio=True, mask='auto')
            y -= 9*cm
        except Exception:
            # skip if drawImage fails for any reason
            pass
    if table_df is not None and not table_df.empty:
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, h-2*cm, "Details")
        c.setFont("Helvetica", 9)
        y = h - 2*cm - 18
        cols = table_df.columns.tolist()[:6]
        col_width = (w - 4*cm) / len(cols)
        # header
        x = 2*cm
        for col in cols:
            c.drawString(x, y, str(col))
            x += col_width
        y -= 14
        for _, row in table_df.head(40).iterrows():
            x = 2*cm
            for col in cols:
                txt = str(row.get(col, ""))[:30]
                c.drawString(x, y, txt)
                x += col_width
            y -= 12
            if y < 2*cm:
                break
    c.save()
    buf.seek(0)
    return buf.read()

st.set_page_config(page_title="Analytics Dashboard", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview Dashboard", "Product Insights", "Region Trends"])

client = get_supabase_client()
df = load_sales(client)

# Global filters
today = date.today()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=90))
end_date = st.sidebar.date_input("End date", today)
regions = st.sidebar.multiselect("Region", options=sorted(df["region"].dropna().unique().tolist()) if "region" in df.columns else [], default=None)
products = st.sidebar.multiselect("Product", options=sorted(df["product"].dropna().unique().tolist()) if "product" in df.columns else [], default=None)
min_revenue = st.sidebar.number_input("Min revenue", min_value=0.0, value=0.0, step=100.0)

if not df.empty:
    df = df[(df["sale_date"] >= start_date) & (df["sale_date"] <= end_date)]
    if regions:
        df = df[df["region"].isin(regions)]
    if products:
        df = df[df["product"].isin(products)]
    df = df[df["revenue"] >= min_revenue]

if page == "Overview Dashboard":
    st.title("Overview Dashboard")
    if df.empty:
        st.info("No data available for the selected filters.")
    else:
        total_rev = df["revenue"].sum()
        total_qty = df["quantity"].sum()
        num_orders = len(df)
        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue", f"₹{total_rev:,.2f}")
        c2.metric("Quantity", f"{total_qty:,}")
        c3.metric("Orders", f"{num_orders:,}")
        st.subheader("Revenue over Time")
        chart_time = alt.Chart(df).mark_line(point=True).encode(x="sale_date:T", y="revenue:Q")
        st.altair_chart(chart_time, use_container_width=True)
        st.subheader("Revenue by Region")
        chart_region = alt.Chart(df.groupby("region").agg(revenue=("revenue","sum")).reset_index()).mark_bar().encode(x="revenue:Q", y="region:N")
        st.altair_chart(chart_region, use_container_width=True)
        if st.button("Export PDF with Charts"):
            img1 = export_chart_png(chart_time)
            img2 = export_chart_png(chart_region)
            summary = {"Start": start_date.isoformat(), "End": end_date.isoformat(), "Revenue": f"₹{total_rev:,.2f}"}
            pdf = pdf_with_charts("Overview Report", summary, [img1, img2], table_df=df.sort_values("sale_date", ascending=False))
            st.download_button("Download PDF", pdf, "overview_report.pdf", mime="application/pdf")

elif page == "Product Insights":
    st.title("Product Insights")
    if df.empty:
        st.info("No data available for the selected filters.")
    else:
        prod = df.groupby("product").agg(revenue=("revenue","sum"), qty=("quantity","sum")).reset_index().sort_values("revenue", ascending=False)
        st.dataframe(prod, height=400)
        chart_prod = alt.Chart(prod).mark_bar().encode(x="revenue:Q", y="product:N")
        st.altair_chart(chart_prod, use_container_width=True)
        if st.button("Export Product PDF"):
            img = export_chart_png(chart_prod)
            summary = {"Start": start_date.isoformat(), "End": end_date.isoformat()}
            pdf = pdf_with_charts("Product Insights", summary, [img], table_df=prod)
            st.download_button("Download PDF", pdf, "product_insights.pdf", mime="application/pdf")

elif page == "Region Trends":
    st.title("Region Trends")
    if df.empty:
        st.info("No data available for the selected filters.")
    else:
        reg = df.groupby(["sale_date","region"]).agg(revenue=("revenue","sum")).reset_index()
        chart = alt.Chart(reg).mark_line().encode(x="sale_date:T", y="revenue:Q", color="region:N")
        st.altair_chart(chart, use_container_width=True)
        if st.button("Export Region PDF"):
            img = export_chart_png(chart)
            summary = {"Start": start_date.isoformat(), "End": end_date.isoformat()}
            pdf = pdf_with_charts("Region Trends", summary, [img], table_df=reg.head(100))
            st.download_button("Download PDF", pdf, "region_trends.pdf", mime="application/pdf")
