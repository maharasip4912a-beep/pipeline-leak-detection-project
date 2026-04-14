# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Cloud

Streamlit Cloud is the easiest way to share your dashboard publicly. It's free and takes just a few minutes!

### Prerequisites
- GitHub account
- This repository pushed to GitHub

---

## Step 1: Push Code to GitHub

```bash
# If not already done
git init
git add .
git commit -m "Add Pipeline Leak Detection Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pipeline-leak-detection
git push -u origin main
```

---

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Sign in with GitHub (first time only)
4. Select:
   - **Repository**: `your-username/pipeline-leak-detection`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

✅ Your dashboard will be live in 1-2 minutes!

---

## Step 3: Access Your Dashboard

Your dashboard will be available at:
```
https://share.streamlit.io/YOUR_USERNAME/pipeline-leak-detection
```

Share this URL with your team!

---

## Configuration (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false

[logger]
level = "info"
```

---

## Update Your Dashboard

Any push to the main branch will automatically redeploy your dashboard!

```bash
# Make changes locally
git add .
git commit -m "Update dashboard"
git push
```

Your live dashboard updates automatically within seconds!

---

## Troubleshooting

### "Module not found" Error
Ensure `requirements.txt` includes all dependencies:
```
streamlit
pandas
numpy
joblib
scikit-learn
```

### "Model file not found" Error
Ensure these files are committed to GitHub:
- `random_forest_model.pkl`
- `scaler.pkl`

### Dashboard Loads Slowly
- First load caches the model in memory
- Subsequent requests are fast
- This is normal behavior

### Blue "Running" indicator
- The app is initializing
- Give it 30 seconds to load
- Works faster on subsequent visits

---

## Performance Tips

1. **Cache heavy operations** (already done with `@st.cache_resource`)
2. **Limit file size** for uploads
3. **Pre-load models** on startup
4. **Use CDN** for static assets

---

## Monitoring Your Deployment

Streamlit Cloud provides:
- View logs and errors
- Monitor resource usage
- Manage settings
- View your app stats

Visit your app settings on Streamlit Cloud dashboard!

---

## Advanced: Docker Deployment

For more control, deploy with Docker:

### Create Dockerfile
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy with Docker
```bash
# Build image
docker build -t leak-detection .

# Run container
docker run -p 8501:8501 leak-detection

# Or use Docker Compose
docker-compose up
```

---

## Advanced: AWS Deployment

### Using EC2
1. Launch EC2 instance (Ubuntu 20.04)
2. SSH into instance
3. Clone your repository
4. Install dependencies
5. Run dashboard with systemd

```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Install python and pip
sudo apt-get update
sudo apt-get install -y python3.8 python3-pip

# Clone repo
git clone https://github.com/YOUR_USERNAME/pipeline-leak-detection
cd pipeline-leak-detection

# Install dependencies
pip install -r requirements.txt

# Run in background
nohup streamlit run app.py --server.port 80 &
```

### Using Heroku (Legacy)
1. Create app on Heroku
2. Add Procfile:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Deploy with git push

---

## Advanced: Custom Domain

With Streamlit Cloud Pro or using a reverse proxy:

### Using Cloudflare
1. Add CNAME record pointing to Streamlit Cloud
2. Configure SSL/TLS
3. Access via custom domain

---

## Sharing Your Dashboard

### Private Sharing
- Use Streamlit Cloud's authentication
- Share URL with specific team members
- Control access per user

### Public Sharing
- Share URL openly
- Add to documentation
- Embed in websites (via iframe)

```html
<!-- Embed in website -->
<iframe 
    src="https://share.streamlit.io/YOUR_USERNAME/pipeline-leak-detection"
    height="600"
    width="100%"
></iframe>
```

---

## Monitoring & Analytics

### View Your Stats
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. View:
   - Sessions
   - Runtime
   - Error logs
   - Resource usage

### Set Up Alerts
- Email notifications for errors
- Integration with monitoring tools
- Custom logging

---

## Cost Considerations

| Platform | Cost | Best For |
|----------|------|----------|
| Streamlit Cloud | Free → $20/mo | Rapid deployment, hobby projects |
| AWS EC2 | $5-30+/mo | Production, scale, enterprise |
| Heroku | Free tier ended | Legacy apps |
| Docker | Cost of hosting | Full control, enterprise |

---

## Support

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Post issues in your repo

---

**Happy Deploying! 🚀**

Your Pipeline Leak Detection Dashboard is now ready for the world!
