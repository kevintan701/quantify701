# Deployment Guide - Quantify 701

**Quantify 701** is built with Streamlit and deployed on Streamlit Cloud.

## Live App

🌐 **Live URL**: [https://quantify701.streamlit.app/](https://quantify701.streamlit.app/)  
📦 **GitHub**: [https://github.com/kevintan701/quantify701](https://github.com/kevintan701/quantify701)

## Current Status

The app is deployed and publicly accessible. When running locally, it creates a web server at `http://localhost:8501`.

## Deployment Options

### Option 1: Streamlit Cloud (Easiest & Free) ⭐ Recommended

Streamlit Cloud is the official hosting platform for Streamlit apps. It's free and very easy to use.

#### Steps:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/quant-stock-selector.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at:** `https://YOUR_APP_NAME.streamlit.app`

**Advantages:**
- ✅ Free tier available
- ✅ Automatic deployments on git push
- ✅ No server management needed
- ✅ HTTPS included
- ✅ Easy to set up

---

### Option 2: Heroku

Heroku is a popular platform for deploying web apps.

#### Steps:

1. **Create a `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

**Note:** Heroku removed their free tier, so this requires a paid plan.

---

### Option 3: AWS EC2 / DigitalOcean / Linode

Deploy to a VPS (Virtual Private Server) for full control.

#### Steps:

1. **Create a VPS instance** (Ubuntu recommended)

2. **SSH into your server:**
   ```bash
   ssh user@your-server-ip
   ```

3. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```

4. **Clone and set up:**
   ```bash
   git clone YOUR_REPO_URL
   cd quant-stock-selector
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run with nohup or systemd:**
   ```bash
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

6. **Set up Nginx reverse proxy** (optional but recommended):
   - Install Nginx
   - Configure to proxy requests to `localhost:8501`
   - Set up SSL with Let's Encrypt

---

### Option 4: Docker + Cloud Platform

Containerize the app for easier deployment.

#### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Create `.dockerignore`:

```
venv/
__pycache__/
*.pyc
.git/
.DS_Store
```

#### Build and run:

```bash
docker build -t quant-stock-selector .
docker run -p 8501:8501 quant-stock-selector
```

Then deploy the Docker image to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

### Option 5: Railway / Render

Modern platforms that make deployment easy.

#### Railway:
1. Connect your GitHub repo
2. Railway auto-detects Streamlit
3. Deploy with one click

#### Render:
1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

---

## Quick Start: Streamlit Cloud (Recommended)

The fastest way to get your app online:

1. **Create a GitHub repository** (if you haven't already)

2. **Add a `.streamlit/config.toml` file** (optional but recommended):
   ```toml
   [server]
   headless = true
   port = 8501
   enableCORS = false
   
   [theme]
   primaryColor = "#667eea"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   font = "sans serif"
   ```

3. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

4. **Deploy on Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Deploy your app
   - Share the URL with others!

---

## Important Notes

### Security Considerations:
- The app uses free Yahoo Finance data (no API keys needed)
- No sensitive data is stored
- Consider adding authentication if needed for production

### Performance:
- First load may be slow (fetching stock data)
- Data is cached for 1 hour to improve performance
- Consider upgrading server resources for faster response times

### Cost:
- **Streamlit Cloud**: Free tier available
- **Heroku**: Paid plans only
- **VPS**: $5-20/month depending on provider
- **Railway/Render**: Free tier available with limitations

---

## Testing Locally Before Deployment

Make sure everything works:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run app.py

# Test in browser at http://localhost:8501
```

---

## Troubleshooting

### Port Issues:
- Make sure to use `--server.port=$PORT` for cloud platforms
- Use `--server.address=0.0.0.0` to allow external connections

### Import Errors:
- Ensure all dependencies are in `requirements.txt`
- Check that Python version matches (3.8+)

### Data Fetching Issues:
- Yahoo Finance may have rate limits
- Consider adding retry logic or delays between requests

---

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Community: https://discuss.streamlit.io/
- Deployment Help: Check platform-specific documentation

