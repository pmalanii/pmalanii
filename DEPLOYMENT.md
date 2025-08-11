# Deployment Guide - WasteFlow to Streamlit Community Cloud

## Prerequisites
1. GitHub account with repository: https://github.com/pmalanii/pmalanii.git
2. Streamlit Community Cloud account (free at https://share.streamlit.io)

## Step-by-Step Deployment Instructions

### 1. Push Code to GitHub
```bash
# Navigate to your project directory
cd c:\Users\pmalanii\Downloads\WMContractMngmt

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Add WasteFlow Smart Contract Management Platform"

# Add your GitHub repository as remote
git remote add origin https://github.com/pmalanii/pmalanii.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy to Streamlit Community Cloud

1. **Visit Streamlit Community Cloud**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `pmalanii/pmalanii`
   - Set branch: `main`
   - Set main file path: `app.py`
   - Set app URL (optional): `wasteflow-contract-management`

3. **Deploy**
   - Click "Deploy!"
   - Wait for deployment to complete (usually 2-3 minutes)

### 3. Access Your Deployed App
Your app will be available at:
`https://wasteflow-contract-management.streamlit.app`

## Files Required for Deployment
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `packages.txt` - System packages (if needed)
- ✅ `.gitignore` - Git ignore file
- ✅ `README.md` - Project documentation

## Troubleshooting

### Common Issues:
1. **Import Errors**: Check `requirements.txt` has all dependencies
2. **File Not Found**: Ensure `app.py` is in the root directory
3. **Memory Issues**: Streamlit Community Cloud has 1GB RAM limit

### Logs:
- View deployment logs in Streamlit Cloud dashboard
- Check for any missing dependencies or errors

## App Features
Once deployed, your WasteFlow platform will include:
- 📊 Executive Dashboard with real-time metrics
- 📋 Contract Management with filtering and search
- ⚖️ Compliance Monitoring with alerts
- 📈 Analytics & Reports with visualizations
- 🔍 AI Contract Analysis simulation

## Support
For deployment issues:
- Streamlit Community Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit forum: https://discuss.streamlit.io