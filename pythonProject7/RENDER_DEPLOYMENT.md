# Deploy to Render.com

## Steps to Deploy:

### 1. Push Your Code to GitHub
First, ensure all files are committed and pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Web Service on Render

1. Go to [https://render.com/](https://render.com/) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

   - **Name**: `color-matcher-app` (or any name you prefer)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `pythonProject7` (since your files are in this subdirectory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid based on your needs)

### 3. Environment Variables (Optional)
If needed, you can set environment variables in the Render dashboard:
- `PORT` - Automatically set by Render (default: 10000)

### 4. Deploy
Click **"Create Web Service"** and Render will automatically:
- Install dependencies from `requirements.txt`
- Start your Flask app using Gunicorn
- Provide you with a public URL

## Important Notes:

✅ **Fixed Issues:**
- Updated `requirements.txt` to include Flask (was using Streamlit by mistake)
- Added `gunicorn` for production WSGI server
- Disabled debug mode for production
- Made port configurable via environment variable

🔍 **What Changed:**
- `requirements.txt` - Now has Flask, numpy, opencv-python-headless, and gunicorn
- `app.py` - Added `import os` and updated run command to use PORT environment variable with debug=False

## Alternative Start Commands:

If the default doesn't work, try these in Render's "Start Command" field:

```bash
# Option 1 (Recommended):
gunicorn app:app

# Option 2 (with specific binding):
gunicorn --bind 0.0.0.0:$PORT app:app

# Option 3 (with workers):
gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app
```

## Troubleshooting:

### If deployment fails:
1. Check Render logs for specific error messages
2. Ensure your repository has the correct file structure:
   ```
   pythonProject7/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   └── index.html
   └── static/
       └── style.css
   ```
3. Verify all dependencies install correctly
4. Make sure the root directory is set to `pythonProject7` in Render settings

### Common Issues:
- **Build fails**: Check if `opencv-python-headless` installs correctly
- **App won't start**: Verify the start command is `gunicorn app:app`
- **404 errors**: Ensure templates and static folders are present

## Testing Locally:

Before deploying, test locally with Gunicorn:
```bash
pip install -r requirements.txt
gunicorn app:app
```

Visit `http://localhost:8000` to test.
