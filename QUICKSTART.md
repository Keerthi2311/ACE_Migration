# 🚀 Quick Start Guide - ACE Migration Estimator

Get up and running in 5 minutes!

## Prerequisites Checklist
- [ ] Docker Desktop installed and running
- [ ] OpenAI API key (or IBM watsonx.ai credentials)
- [ ] 8GB RAM available
- [ ] Ports 5173, 8000, 5432, 6333, 6379 available

## Step-by-Step Setup

### 1. Get the Code
```bash
cd "/Users/keerthi/Desktop/ACE Migration"
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp backend/.env.example .env

# Edit the .env file and add your API key
# Minimum required: OPENAI_API_KEY=sk-your-key-here
nano .env  # or use your favorite editor
```

### 3. Start Everything
```bash
# Start all services (this will take 2-3 minutes first time)
docker-compose up -d

# Wait for services to be healthy
docker-compose ps
```

### 4. Initialize Database
```bash
# Seed the database with sample historical projects
docker-compose exec backend python scripts/seed_database.py
```

### 5. Access the Application
Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎉 You're Ready!

Start using the application:
1. Fill in the questionnaire form
2. Watch the live estimate update in real-time
3. Generate a comprehensive report
4. View similar historical projects
5. Review risk assessments and recommendations

## Common First-Time Issues

### Docker containers not starting?
```bash
# Check if ports are available
lsof -i :5173
lsof -i :8000
lsof -i :5432

# Restart Docker Desktop
# Then try again:
docker-compose down
docker-compose up -d
```

### Can't access the frontend?
- Make sure you're using http:// not https://
- Try http://localhost:5173 instead of 127.0.0.1
- Check if the frontend container is running: `docker-compose ps frontend`

### API connection errors?
- Verify backend is healthy: http://localhost:8000/health
- Check backend logs: `docker-compose logs backend`
- Ensure .env file is in the root directory (not in backend/)

### Database not initialized?
```bash
# Run the seed script again
docker-compose exec backend python scripts/seed_database.py

# Check if data was loaded
docker-compose exec postgres psql -U postgres -d ace_estimator -c "SELECT COUNT(*) FROM historical_projects;"
```

## Development Mode (Optional)

### Run Frontend Locally
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:5173
```

### Run Backend Locally
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Make sure PostgreSQL, Qdrant, Redis are running in Docker
docker-compose up -d postgres qdrant redis

# Start backend
uvicorn app.main:app --reload
# Access at http://localhost:8000
```

## Next Steps

1. **Read the full README.md** for comprehensive documentation
2. **Explore the API** at http://localhost:8000/docs
3. **Test the questionnaire** with sample data
4. **Review the estimation logic** in `backend/app/core/rules_engine.py`
5. **Customize for your needs** - modify rules, add new fields, etc.

## Getting Help

- Check **README.md** for detailed documentation
- View **API documentation** at http://localhost:8000/docs
- Check **logs**: `docker-compose logs -f`
- View **troubleshooting section** in README.md

---

**Happy Estimating! 🎯**
