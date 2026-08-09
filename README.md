# 🚀 NaMo Auto Share Script — Railway Edition

Auto-play script for NaMo API v2. Sends share requests with incrementing `post_id` values using concurrent workers with retry logic, rate limiting, and graceful shutdown.

## 📁 Project Structure

```
namo/
├── main.py           # Main script
├── requirements.txt  # Python dependencies
├── Procfile          # Railway process config
├── railway.toml      # Railway deploy config
├── Dockerfile        # Alternative Docker deploy
└── .gitignore
```

## ⚡ Features

- 🔄 **Concurrent Workers** — 10 threads by default (configurable)
- 🔁 **Auto Retry** — 3 retries with exponential backoff
- ⏸️ **Auto Pause** — Pauses 60s every 50 requests (configurable)
- 🛑 **Graceful Shutdown** — Handles SIGINT/SIGTERM cleanly
- 📊 **Live Stats** — Shows success/fail count and speed
- 🔌 **Proxy Support** — Optional proxy for cloud deployment
- 🔧 **Env Config** — All settings configurable via environment variables
- 🚂 **Railway Ready** — Auto-restart on failure

## 🚂 Deploy to Railway

### Step 1: Push to GitHub
```bash
cd namo
git init
git add .
git commit -m "NaMo auto share script"
git remote add origin https://github.com/YOUR_USERNAME/namo.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub Repo"**
3. Select your `namo` repo
4. Railway will auto-detect Python and deploy

### Step 3: Set Environment Variables (Optional)
In Railway dashboard → your service → **Variables** tab:

| Variable | Default | Description |
|---|---|---|
| `START_POST_ID` | `1` | Starting post ID |
| `END_POST_ID` | `100000010000` | Ending post ID |
| `CONCURRENT_WORKERS` | `10` | Number of threads |
| `DELAY_PER_REQUEST` | `0.1` | Seconds between submissions |
| `PAUSE_INTERVAL` | `50` | Pause every N requests |
| `PAUSE_DURATION` | `60` | Pause duration in seconds |
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |
| `MAX_RETRIES` | `3` | Max retry attempts |
| `USE_PROXY` | `False` | Enable proxy |
| `PROXY_URL` | `http://IP:PORT` | Proxy address |
| `X_ACCESS_TOKEN` | *(hardcoded)* | API access token |
| `ADDRESS_ID` | *(hardcoded)* | Address ID |
| `DEVICE_ID` | *(hardcoded)* | Device ID |
| `COOKIE` | *(hardcoded)* | Session cookies |
| `X_ACF_SENSOR_DATA` | *(hardcoded)* | Akamai sensor data |

## 🖥️ Run Locally
```bash
pip install -r requirements.txt
python main.py
```

## 🛑 Stop Gracefully
Press `Ctrl+C` — it will finish current tasks and show a summary.
