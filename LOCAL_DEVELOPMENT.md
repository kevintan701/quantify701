# Local Development Guide

## Quick Start (No Docker Required!)

You can develop this app locally **without Docker**. Here's the simple way:

### Step 1: Set Up Virtual Environment (One Time Only)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### Step 2: Install Dependencies (One Time Only)

```bash
pip install -r requirements.txt
```

### Step 3: Run the App (Every Time You Develop)

**Option A: Use the convenience script:**
```bash
./run_app.sh
```

**Option B: Run directly:**
```bash
# Make sure venv is activated first
source venv/bin/activate  # On macOS/Linux
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## Why You Don't Need Docker

- **Docker is ONLY for deployment** to cloud platforms (AWS, Google Cloud, etc.)
- **Streamlit Cloud doesn't use Docker** - it runs your code directly
- **Local development is faster** without Docker - just use Python + virtual environment

---

## Troubleshooting

### "Command not found: streamlit"
- Make sure your virtual environment is activated
- Run: `pip install -r requirements.txt` again

### Port 8501 already in use
- Stop any other Streamlit apps running
- Or use a different port: `streamlit run app.py --server.port=8502`

### Virtual environment issues
- Delete the `venv` folder and recreate it
- Make sure you're using Python 3.8 or higher

---

## Development Workflow

1. **Activate virtual environment** (if not already active)
   ```bash
   source venv/bin/activate
   ```

2. **Make your code changes** in your editor

3. **Run the app** to see changes
   ```bash
   streamlit run app.py
   ```

4. **Streamlit auto-reloads** when you save files - no need to restart!

---

## When Would You Use Docker?

Only if you want to:
- Test the containerized version before deploying
- Deploy to platforms that require Docker (AWS ECS, Google Cloud Run, etc.)
- Ensure consistent environment across different machines

For normal development, **just use the virtual environment method above**.

