# Quick Start Guide - Hosting Your AI Trading System

This guide will help you host your AI Multi-Domain Trading System online.

## Option 1: Deploy to Render.com (Recommended - Easiest)

Render.com offers free hosting for web applications and automatically detects your configuration.

### Steps:

1. **Sign up** at [render.com](https://render.com)

2. **Click "New +"** and select **"Web Service"**

3. **Connect your GitHub repository**:
   - Authorize Render to access your GitHub account
   - Select the `ai_project` repository

4. **Configure the service**:
   - **Name**: Choose a unique name (e.g., `ai-trading-system`)
   - **Branch**: `main` (or your default branch)
   - **Runtime**: Python 3
   - Render will automatically detect the `Procfile` and other configs

5. **Set Environment Variables** (optional, for API features):
   - Click "Advanced" → "Add Environment Variable"
   - Add any API keys from `.env.example` that you need

6. **Click "Create Web Service"**

7. **Wait for deployment** (2-5 minutes)

8. **Access your app** at: `https://your-app-name.onrender.com`

That's it! Your AI system is now hosted and accessible online.

---

## Option 2: Deploy to Railway.app

Railway is another excellent platform with generous free tier.

### Steps:

1. **Sign up** at [railway.app](https://railway.app)

2. **Click "New Project"** → **"Deploy from GitHub repo"**

3. **Select your repository**

4. **Railway will automatically**:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Start your app using the `Procfile`

5. **Generate a domain**:
   - Go to Settings → Generate Domain

6. **Access your app** at the generated domain

---

## Option 3: Deploy with Docker (Any Platform)

If you prefer using Docker, this project includes a `Dockerfile` and `docker-compose.yml`.

### Local Testing:

```bash
# Build and run with Docker Compose
docker-compose up

# Or build manually
docker build -t ai-trading-system .
docker run -p 5000:5000 ai-trading-system
```

### Deploy to any Docker-compatible platform:
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Instances
- DigitalOcean App Platform
- Fly.io

---

## Option 4: Traditional Heroku

### Steps:

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Deploy
git push heroku main

# Open your app
heroku open
```

---

## After Deployment

### Test Your Hosted API:

```bash
# Replace YOUR_URL with your actual deployment URL

# Health check
curl https://YOUR_URL/health

# System status
curl https://YOUR_URL/status

# Analyze crypto market
curl -X POST https://YOUR_URL/crypto/analyze \
     -H "Content-Type: application/json" \
     -d '{"symbol":"BTC/USDT"}'
```

### Access the Web Interface:

Simply navigate to your deployment URL in a browser to see the interactive documentation and test the API.

---

## Adding API Keys (Optional)

To enable full functionality (crypto trading, social media, etc.):

1. **On Render/Railway**:
   - Go to Environment Variables section
   - Add keys from `.env.example`

2. **On Heroku**:
   ```bash
   heroku config:set BINANCE_API_KEY=your_key_here
   heroku config:set TWITTER_API_KEY=your_key_here
   ```

3. **With Docker**:
   - Create a `.env` file locally
   - Mount it when running: `docker run --env-file .env -p 5000:5000 ai-trading-system`

---

## Monitoring Your Deployment

### Check Logs:

- **Render**: Dashboard → Logs tab
- **Railway**: Project → Deployments → View Logs
- **Heroku**: `heroku logs --tail`
- **Docker**: `docker logs <container-id>`

---

## Troubleshooting

### "Application Error" or Won't Start

1. Check that all dependencies in `requirements.txt` are installable
2. Review deployment logs for error messages
3. Ensure Python version is 3.8+ (specified in `runtime.txt`)

### API Endpoints Return Errors

1. The AI model may need time to initialize (wait 30-60 seconds after deployment)
2. Check that you're using the correct HTTP methods (POST vs GET)
3. Verify JSON format in request body

### Out of Memory

- The TensorFlow dependency can be memory-intensive
- Upgrade to a paid tier with more RAM
- Or use a lighter AI model in production

---

## Cost Estimates

- **Render Free Tier**: Free (with limitations)
- **Railway Free Tier**: $5 credit monthly
- **Heroku**: $5-7/month for basic tier
- **Docker on cloud**: Varies by provider

Most platforms offer free tiers perfect for testing and small-scale use!

---

## Need Help?

- Check the main README.md for detailed documentation
- Review deployment platform documentation
- Check logs for specific error messages
