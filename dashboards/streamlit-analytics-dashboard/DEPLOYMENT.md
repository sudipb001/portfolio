# 🚀 Deployment Guide

This guide explains how to deploy your Sales Analytics Dashboard to Streamlit Cloud for free.

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Supabase account (optional, but recommended for live data)

## 🔧 Option 1: Deploy with Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository

1. **Create a GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Sales Analytics Dashboard"
   git branch -M main
   git remote add origin https://github.com/yourusername/sales-analytics-dashboard.git
   git push -u origin main
   ```

2. **Ensure required files are present**
   - ✅ `app.py` (main application)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `.gitignore` (excludes sensitive files)
   - ✅ `README.md` (documentation)

### Step 2: Set Up Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Click "New app"**

3. **Configure deployment**
   - Repository: Select your GitHub repo
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom URL (e.g., `yourname-sales-dashboard`)

4. **Add secrets (if using Supabase)**
   - Click "Advanced settings"
   - Go to "Secrets"
   - Add your environment variables:
   ```toml
   SUPABASE_URL = "your_supabase_project_url"
   SUPABASE_KEY = "your_supabase_anon_key"
   ```

5. **Click "Deploy"**
   - Streamlit will install dependencies and launch your app
   - This usually takes 2-3 minutes

### Step 3: Verify Deployment

1. Your app will be live at: `https://yourname-sales-dashboard.streamlit.app`
2. Test all features:
   - ✅ Filters work
   - ✅ Charts display correctly
   - ✅ Data loads (from Supabase or sample data)
   - ✅ Exports function (CSV, Excel, PDF)

## 🐳 Option 2: Deploy with Docker

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build the image
docker build -t sales-dashboard .

# Run the container
docker run -p 8501:8501 \
  -e SUPABASE_URL="your_url" \
  -e SUPABASE_KEY="your_key" \
  sales-dashboard
```

### Deploy to Docker Hub

```bash
# Tag the image
docker tag sales-dashboard yourusername/sales-dashboard:latest

# Push to Docker Hub
docker push yourusername/sales-dashboard:latest
```

## ☁️ Option 3: Deploy to Cloud Platforms

### Heroku

1. **Create `Procfile`**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   port = $PORT\n\
   enableCORS = false\n\
   headless = true\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku config:set SUPABASE_URL="your_url"
   heroku config:set SUPABASE_KEY="your_key"
   ```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance and setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip python3-venv -y
   
   # Clone your repo
   git clone https://github.com/yourusername/sales-analytics-dashboard.git
   cd sales-analytics-dashboard
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set environment variables
   export SUPABASE_URL="your_url"
   export SUPABASE_KEY="your_key"
   
   # Run with nohup for background execution
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

3. **Configure security group**
   - Allow inbound traffic on port 8501
   - Access via: `http://your-ec2-public-ip:8501`

### Google Cloud Run

1. **Create `Dockerfile`** (see Docker section above)

2. **Deploy to Cloud Run**
   ```bash
   # Authenticate
   gcloud auth login
   
   # Set project
   gcloud config set project your-project-id
   
   # Build and deploy
   gcloud run deploy sales-dashboard \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars SUPABASE_URL="your_url",SUPABASE_KEY="your_key"
   ```

## 🔒 Security Best Practices

### 1. Environment Variables
- ❌ Never commit `.env` files to Git
- ✅ Use platform-specific secret management
- ✅ Rotate keys regularly

### 2. Supabase Security
- Enable Row Level Security (RLS) policies
- Use service role key only for backend operations
- Use anon key for frontend (dashboard)

### 3. Access Control
- Consider adding authentication (Streamlit supports OAuth)
- Implement user roles if needed
- Monitor usage and set rate limits

## 📊 Monitoring & Maintenance

### Streamlit Cloud
- View logs in the Streamlit Cloud dashboard
- Monitor app health and uptime
- Check resource usage (free tier has limits)

### Custom Deployment
- Set up application monitoring (e.g., New Relic, Datadog)
- Configure error logging
- Set up uptime monitoring (e.g., UptimeRobot)

## 🔄 Continuous Deployment

### Streamlit Cloud Auto-Deploy
Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update: Added new feature"
git push origin main

# Streamlit Cloud will automatically redeploy!
```

### GitHub Actions (Advanced)
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run tests
        run: |
          pip install -r requirements.txt
          python -m pytest tests/
      
      # Add your deployment steps here
```

## 🌐 Custom Domain (Optional)

### Streamlit Cloud
1. Go to app settings
2. Click "Custom domain"
3. Add your domain (requires DNS configuration)
4. Follow Streamlit's instructions to point your domain

### Other Platforms
Configure your DNS to point to:
- Heroku: `CNAME` to your Heroku app
- AWS: Use Route 53 or your DNS provider
- Cloud Run: Configure custom domain in Google Cloud Console

## 📈 Scaling Considerations

### Free Tier Limits
- **Streamlit Cloud**: 1 app, limited resources
- **Heroku**: 550-1000 dyno hours/month
- **Google Cloud Run**: 2M requests/month free

### When to Upgrade
- High traffic (>10k daily users)
- Large datasets (>1GB)
- Need for better performance
- Custom resource requirements

### Optimization Tips
1. **Cache data aggressively**
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   ```

2. **Lazy load visualizations**
   - Only load charts when needed
   - Implement pagination for large datasets

3. **Optimize database queries**
   - Use Supabase views for complex aggregations
   - Index frequently queried columns

4. **Use CDN for static assets**
   - Host images on CDN
   - Minimize file sizes

## 🐛 Troubleshooting Deployment

### Common Issues

**Issue**: "ModuleNotFoundError" on deployment
- **Solution**: Ensure all packages are in `requirements.txt` with version numbers

**Issue**: App crashes on startup
- **Solution**: Check logs for errors. Verify environment variables are set correctly

**Issue**: Slow performance
- **Solution**: Implement caching, optimize queries, consider upgrading hosting plan

**Issue**: Database connection fails
- **Solution**: Check Supabase URL and key. Verify network access from hosting platform

## ✅ Deployment Checklist

Before going live, ensure:
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.env` file not committed to Git
- [ ] Environment variables configured on platform
- [ ] Database credentials are correct
- [ ] RLS policies enabled on Supabase
- [ ] App tested locally with production settings
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] README updated with live URL
- [ ] Custom domain configured (if applicable)

## 🎉 Success!

Once deployed, your dashboard will be accessible 24/7. Share the link:
- **Add to portfolio**: Include in resume and LinkedIn
- **Share with recruiters**: Demonstrate your skills
- **Get feedback**: Share with peers for improvements

---

**Need Help?**
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Supabase Docs](https://supabase.com/docs)
- [Docker Documentation](https://docs.docker.com/)
