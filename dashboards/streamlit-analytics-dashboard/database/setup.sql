-- =====================================================
-- Supabase Database Setup Script
-- Sales Analytics Dashboard
-- =====================================================

-- Create the sales_data table
CREATE TABLE IF NOT EXISTS sales_data (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    region VARCHAR(100) NOT NULL,
    product VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    units_sold INTEGER NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    profit_margin DECIMAL(5, 4) NOT NULL,
    profit DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_data(date);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_data(region);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_data(product);
CREATE INDEX IF NOT EXISTS idx_sales_category ON sales_data(category);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales_data(customer_id);

-- Enable Row Level Security (RLS)
ALTER TABLE sales_data ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (adjust as needed for your security requirements)
CREATE POLICY "Enable all access for authenticated users" ON sales_data
    FOR ALL
    USING (auth.role() = 'authenticated');

-- For public read access (if needed for demo purposes)
CREATE POLICY "Enable read access for all users" ON sales_data
    FOR SELECT
    USING (true);

-- =====================================================
-- Sample Data Generation (Optional)
-- Run this if you want to populate with sample data
-- =====================================================

-- Function to generate random sales data
CREATE OR REPLACE FUNCTION generate_sample_sales_data()
RETURNS void AS $$
DECLARE
    v_date DATE;
    v_region VARCHAR;
    v_product VARCHAR;
    v_category VARCHAR;
    v_revenue DECIMAL;
    v_units INTEGER;
    v_margin DECIMAL;
    v_regions VARCHAR[] := ARRAY['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'];
    v_products VARCHAR[] := ARRAY['Product A', 'Product B', 'Product C', 'Product D', 'Product E'];
    v_categories VARCHAR[] := ARRAY['Electronics', 'Software', 'Services', 'Hardware', 'Accessories'];
    i INTEGER;
    j INTEGER;
BEGIN
    -- Generate data for the last 365 days
    FOR i IN 0..364 LOOP
        v_date := CURRENT_DATE - i;
        
        -- Generate 3-7 transactions per day
        FOR j IN 1..(3 + floor(random() * 5)::int) LOOP
            v_region := v_regions[1 + floor(random() * 5)::int];
            v_product := v_products[1 + floor(random() * 5)::int];
            v_category := v_categories[1 + floor(random() * 5)::int];
            v_revenue := 1000 + (random() * 49000);
            v_units := 1 + floor(random() * 100)::int;
            v_margin := 0.15 + (random() * 0.30);
            
            INSERT INTO sales_data (date, region, product, category, revenue, units_sold, customer_id, profit_margin, profit)
            VALUES (
                v_date,
                v_region,
                v_product,
                v_category,
                v_revenue,
                v_units,
                'CUST-' || (1000 + floor(random() * 9000)::int),
                v_margin,
                v_revenue * v_margin
            );
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Uncomment the line below to populate the table with sample data
-- SELECT generate_sample_sales_data();

-- =====================================================
-- Useful Views
-- =====================================================

-- Daily revenue summary
CREATE OR REPLACE VIEW daily_revenue_summary AS
SELECT 
    date,
    COUNT(*) as transaction_count,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(units_sold) as total_units,
    AVG(revenue) as avg_order_value,
    AVG(profit_margin) as avg_profit_margin
FROM sales_data
GROUP BY date
ORDER BY date DESC;

-- Regional performance
CREATE OR REPLACE VIEW regional_performance AS
SELECT 
    region,
    COUNT(*) as transaction_count,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(units_sold) as total_units,
    AVG(profit_margin) as avg_profit_margin
FROM sales_data
GROUP BY region
ORDER BY total_revenue DESC;

-- Product performance
CREATE OR REPLACE VIEW product_performance AS
SELECT 
    product,
    category,
    COUNT(*) as transaction_count,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(units_sold) as total_units,
    AVG(profit_margin) as avg_profit_margin
FROM sales_data
GROUP BY product, category
ORDER BY total_revenue DESC;

-- Monthly summary
CREATE OR REPLACE VIEW monthly_summary AS
SELECT 
    DATE_TRUNC('month', date) as month,
    COUNT(*) as transaction_count,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit,
    SUM(units_sold) as total_units,
    AVG(revenue) as avg_order_value
FROM sales_data
GROUP BY DATE_TRUNC('month', date)
ORDER BY month DESC;

-- =====================================================
-- Grant permissions to views
-- =====================================================

GRANT SELECT ON daily_revenue_summary TO authenticated;
GRANT SELECT ON regional_performance TO authenticated;
GRANT SELECT ON product_performance TO authenticated;
GRANT SELECT ON monthly_summary TO authenticated;

-- For public access (if needed)
GRANT SELECT ON daily_revenue_summary TO anon;
GRANT SELECT ON regional_performance TO anon;
GRANT SELECT ON product_performance TO anon;
GRANT SELECT ON monthly_summary TO anon;
