# Streamlit Analytics Dashboard (Enhanced v2)

This is an enhanced, GitHub-ready portfolio project showcasing a multi-page Streamlit dashboard backed by Supabase.
Features:
- Multi-page Streamlit app (Overview, Product Insights, Region Trends)
- Exports PDF reports with embedded chart images (where supported)
- README with badges and place for screenshots
- `.gitignore` to protect secrets and artifacts

See `/assets` for demo screenshots (add your images there before publishing).

## Run locally
1. Create and activate a venv.
2. Install requirements: `pip install -r requirements.txt`
3. Create `.env` with `SUPABASE_URL` and `SUPABASE_KEY`
4. Run: `streamlit run app.py`

## Notes
- Chart-to-PNG conversion requires `altair_saver` + a renderer (selenium or node). If PNG export fails in your environment, PDF will still include available content.
- Never commit your `service_role` key. Use anon key for read-only dashboards.
