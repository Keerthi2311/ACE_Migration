# IBM ACE Migration Estimator

> AI-powered intelligent estimation tool for IBM App Connect Enterprise (ACE) migration projects using RAG (Retrieval-Augmented Generation) technology.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The IBM ACE Migration Estimator is an intelligent tool designed to accurately estimate the effort required for migrating IBM App Connect Enterprise (formerly WebSphere Message Broker) projects. It combines:

- **Rules-based estimation engine** for baseline calculations
- **RAG (Retrieval-Augmented Generation)** for intelligent insights from historical data
- **LLM-powered analysis** for risk assessment and recommendations
- **Real-time estimation** as users fill in questionnaire data
- **80-20 manual review split** to identify high-risk items requiring architect oversight

### Business Value

- **Reduces estimation time** from days to minutes
- **Improves accuracy** by leveraging historical project data
- **Identifies risks early** with AI-powered analysis
- **Provides transparency** with detailed breakdowns and similar project references
- **Supports multiple versions** (WMB v6/7/8, IIB v9/10, ACE v11/12)

---

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Semantic Search**: Finds similar historical projects using vector embeddings
- **Free Text Analysis**: Extracts structured data from unstructured input
- **Risk Assessment**: Identifies high-priority items needing manual review
- **Smart Suggestions**: Provides real-time validation and recommendations

### 📊 Comprehensive Estimation
- **Multi-Phase Breakdown**: Analysis, Design, Development, Testing, Deployment
- **Environment Considerations**: DEV, QA, UAT, PROD configurations
- **Infrastructure Factors**: On-Premise, Cloud, Container, Mainframe
- **Universal Rate Calculation**: 5 flows per 2 days with dynamic buffer scaling
- **Complexity Multipliers**: Legacy source (+15%), Mainframe (+20%), Custom plugins (+10%)

### 🎨 Modern User Interface
- **IBM Carbon Design System**: Professional, accessible UI components
- **Progressive Questionnaire**: Step-by-step data collection
- **Live Estimation Widget**: Real-time updates as you type
- **Interactive Reports**: Expandable sections, charts, and insights

### 🔧 Enterprise-Ready
- **Docker Support**: Complete containerized deployment
- **PostgreSQL Database**: Reliable data persistence
- **Qdrant Vector DB**: High-performance semantic search
- **Redis Caching**: Optimized performance
- **API-First Design**: RESTful APIs with OpenAPI/Swagger documentation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  IBM Carbon Design System │ TypeScript │ React Hook Form    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Rules Engine│  │  RAG Service │  │  LLM Service │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└──────┬───────────────┬────────────────────┬─────────────────┘
       │               │                    │
       │               │                    │
┌──────▼──────┐ ┌──────▼──────┐    ┌──────▼──────┐
│ PostgreSQL  │ │   Qdrant    │    │   Redis     │
│  Database   │ │  Vector DB  │    │   Cache     │
└─────────────┘ └─────────────┘    └─────────────┘
                       │
                       │ Embeddings
                ┌──────▼──────┐
                │   OpenAI    │
                │ or watsonx  │
                └─────────────┘
```

---

## 💻 Technology Stack

### Frontend
- **Framework**: React 18.2 with TypeScript 5.3
- **UI Library**: IBM Carbon Design System v1.50
- **Build Tool**: Vite 5.0
- **Form Management**: React Hook Form 7.49
- **HTTP Client**: Axios
- **State Management**: React Query

### Backend
- **Framework**: FastAPI 0.109 (Python 3.11+)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0
- **Vector DB**: Qdrant 1.7
- **Cache**: Redis 7
- **AI/LLM**: OpenAI API / IBM watsonx.ai
- **Testing**: Pytest 7.4

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx (production)
- **CI/CD**: GitHub Actions (recommended)

---

## 📦 Prerequisites

### Required
- **Docker Desktop** 4.0+ (includes Docker Compose)
- **Node.js** 18+ and npm 9+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **OpenAI API Key** (for AI features) or IBM watsonx.ai credentials

### Optional
- **Git** 2.30+
- **VS Code** with Python and TypeScript extensions
- **PostgreSQL Client** (for database inspection)

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "ACE Migration"
   ```

2. **Create environment file**
   ```bash
   cp backend/.env.example .env
   ```

3. **Configure API keys** (edit `.env`)
   ```bash
   # Add your OpenAI API key
   OPENAI_API_KEY=sk-your-api-key-here
   
   # Or use IBM watsonx.ai
   LLM_PROVIDER=watsonx
   WATSONX_API_KEY=your-watsonx-key
   WATSONX_PROJECT_ID=your-project-id
   ```

4. **Start all services**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Qdrant UI: http://localhost:6333/dashboard

6. **Initialize the database** (first time only)
   ```bash
   docker-compose exec backend python scripts/seed_database.py
   ```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Start PostgreSQL, Qdrant, and Redis (via Docker)
docker-compose up -d postgres qdrant redis

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_database.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

## ⚙️ Configuration

### Environment Variables

#### Application Settings
```bash
APP_NAME=IBM ACE Migration Estimator
APP_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
FRONTEND_URL=http://localhost:5173
```

#### Database Configuration
```bash
POSTGRES_HOST=postgres          # Use 'localhost' for local dev
POSTGRES_PORT=5432
POSTGRES_DB=ace_estimator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
```

#### Vector Database (Qdrant)
```bash
QDRANT_HOST=qdrant             # Use 'localhost' for local dev
QDRANT_PORT=6333
QDRANT_API_KEY=                # Optional for local
QDRANT_COLLECTION_NAME=historical_projects
```

#### Redis Cache
```bash
REDIS_HOST=redis               # Use 'localhost' for local dev
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=                # Optional
CACHE_TTL=3600                 # 1 hour
```

#### LLM Configuration
```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=2000

# IBM watsonx.ai (alternative)
WATSONX_API_KEY=your-watsonx-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-chat-v2

# Select provider (openai or watsonx)
LLM_PROVIDER=openai
```

#### RAG & Estimation
```bash
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
VECTOR_SEARCH_TOP_K=10
VECTOR_SEARCH_SCORE_THRESHOLD=0.7
CONFIDENCE_THRESHOLD_HIGH=0.8
CONFIDENCE_THRESHOLD_MEDIUM=0.6
MANUAL_REVIEW_PERCENTAGE=0.2   # 20%
MAX_ESTIMATE_ADJUSTMENT=0.2    # ±20%
```

---

## 📁 Project Structure

```
ACE Migration/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes/
│   │   │       ├── questionnaire.py
│   │   │       ├── estimation.py
│   │   │       └── insights.py
│   │   ├── core/              # Core modules
│   │   │   ├── config.py      # Configuration
│   │   │   ├── security.py    # Authentication
│   │   │   └── rules_engine.py # Estimation rules
│   │   ├── schemas/           # Pydantic models
│   │   │   ├── questionnaire_schema.py
│   │   │   └── estimation_schema.py
│   │   ├── services/          # Business logic
│   │   │   ├── llm_service.py         # LLM integration
│   │   │   ├── rag_service.py         # RAG functionality
│   │   │   ├── estimation_service.py  # Estimation logic
│   │   │   └── vector_db_service.py   # Vector DB ops
│   │   └── main.py            # FastAPI app entry
│   ├── scripts/               # Utility scripts
│   │   ├── seed_database.py   # Seed historical data
│   │   └── add_project_example.py
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── .env.example          # Environment template
│
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── EstimationReport.tsx
│   │   │   │   ├── EstimationReport.scss
│   │   │   │   ├── LiveEstimateWidget.tsx
│   │   │   │   └── LiveEstimateWidget.scss
│   │   │   └── Questionnaire/
│   │   │       ├── QuestionnaireForm.tsx
│   │   │       ├── SourceEnvironment.tsx
│   │   │       ├── TargetEnvironment.tsx
│   │   │       └── GeneralInfo.tsx
│   │   ├── services/
│   │   │   ├── api.ts         # Axios instance
│   │   │   └── types.ts       # TypeScript types
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # React entry point
│   │   └── index.scss         # Carbon theme config
│   ├── package.json           # Node dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── tsconfig.json          # TypeScript config
│   └── Dockerfile             # Frontend container
│
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

---

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Questionnaire Validation
```http
POST /api/questionnaire/validate
Content-Type: application/json

{
  "question_id": "total_flows",
  "answer": 150,
  "context": {}
}
```

#### Live Estimation
```http
POST /api/estimation/live-calculate
Content-Type: application/json

{
  "source_environment": {
    "product_version": "IIB_v10",
    "total_flows": 150
  },
  "target_environment": {
    "product_version": "ACE_v12"
  }
}
```

#### Generate Full Report
```http
POST /api/estimation/generate-report
Content-Type: application/json

{
  "source_environment": { ... },
  "target_environment": { ... },
  "general_info": { ... }
}
```

#### Find Similar Projects
```http
GET /api/insights/similar-projects?source_version=IIB_v10&target_version=ACE_v12&flow_count=150&infrastructure=on_premise
```

#### Risk Assessment
```http
POST /api/insights/risk-assessment
Content-Type: application/json

{
  "source_environment": { ... },
  "target_environment": { ... }
}
```

---

## 🛠️ Development

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and format code
npm run lint
```

### Backend Development

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app/
isort app/

# Type checking
mypy app/
```

### Database Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Adding Historical Data

```bash
# Seed the database with sample data
docker-compose exec backend python scripts/seed_database.py

# Add a single project example
docker-compose exec backend python scripts/add_project_example.py
```

---

## 🚢 Deployment

### Docker Production Deployment

1. **Update docker-compose.yml for production**
   ```yaml
   services:
     backend:
       environment:
         - DEBUG=false
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
     
     frontend:
       command: npm run build && npm run preview
   ```

2. **Use production environment file**
   ```bash
   cp backend/.env.example .env.production
   # Edit .env.production with production values
   docker-compose --env-file .env.production up -d
   ```

3. **Set up SSL/TLS** (recommended)
   - Use nginx reverse proxy
   - Configure Let's Encrypt certificates
   - Enable HTTPS redirects

### Cloud Deployment Options

- **AWS**: ECS/Fargate, RDS, ElastiCache, OpenSearch
- **Azure**: Container Instances, PostgreSQL, Redis Cache, Cognitive Search
- **IBM Cloud**: Code Engine, Databases for PostgreSQL, watsonx.ai
- **Google Cloud**: Cloud Run, Cloud SQL, Memorystore, Vertex AI

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_estimation_service.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Frontend Tests

```bash
cd frontend

# Run unit tests (if configured)
npm test

# Run E2E tests (if configured)
npm run test:e2e
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Docker containers won't start
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Restart all services
docker-compose down
docker-compose up -d

# Rebuild containers
docker-compose up -d --build
```

#### 2. Frontend can't connect to backend
- Check VITE_API_URL in frontend environment
- Verify backend is running: http://localhost:8000/health
- Check CORS settings in backend/.env

#### 3. Database connection errors
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U postgres -d ace_estimator

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 4. Vector DB (Qdrant) issues
```bash
# Check Qdrant health
curl http://localhost:6333/health

# View collections
curl http://localhost:6333/collections

# Reset Qdrant data
docker-compose down
docker volume rm ace-migration_qdrant_data
docker-compose up -d qdrant
```

#### 5. OpenAI API errors
- Verify OPENAI_API_KEY is set correctly
- Check API quota and billing
- Test with watsonx.ai as alternative: `LLM_PROVIDER=watsonx`

#### 6. Frontend build errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 7. Python import errors
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Performance Optimization

### Backend Optimization
- Enable Redis caching for repeated queries
- Use connection pooling for databases
- Implement rate limiting to prevent abuse
- Cache embedding results in Qdrant

### Frontend Optimization
- Code splitting with React.lazy()
- Optimize Carbon component imports
- Use React Query for intelligent caching
- Implement virtual scrolling for large lists

---

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Authentication**: Implement JWT tokens for production
3. **CORS**: Restrict allowed origins in production
4. **Rate Limiting**: Configure appropriate rate limits
5. **Input Validation**: All inputs validated via Pydantic
6. **SQL Injection**: Protected by SQLAlchemy ORM
7. **XSS Protection**: React automatically escapes content

---

## 📈 Monitoring & Logging

### Application Logs
```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View all logs
docker-compose logs -f
```

### Health Checks
- Backend: http://localhost:8000/health
- Qdrant: http://localhost:6333/health
- PostgreSQL: `docker-compose exec postgres pg_isready`
- Redis: `docker-compose exec redis redis-cli ping`

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Follow Airbnb style guide
- **Commits**: Use conventional commits format

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **IBM Carbon Design System** for the beautiful UI components
- **OpenAI** for powerful LLM capabilities
- **FastAPI** for the excellent Python web framework
- **Qdrant** for vector database technology
- **React** and the amazing React ecosystem

---

## 📞 Support

For issues, questions, or feature requests:
- 📧 Email: support@example.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🗺️ Roadmap

### Version 1.1 (Q4 2025)
- [ ] Multi-language support (i18n)
- [ ] Export reports to PDF/Excel
- [ ] Custom rules engine configuration
- [ ] Integration with Jira/ServiceNow

### Version 1.2 (Q1 2026)
- [ ] Advanced analytics dashboard
- [ ] Machine learning model training
- [ ] Multi-tenant support
- [ ] Mobile app (React Native)

### Version 2.0 (Q2 2026)
- [ ] Real-time collaboration
- [ ] Project timeline visualization
- [ ] Resource allocation optimizer
- [ ] Integration with IBM Cloud Pak

---

**Made with ❤️ for IBM ACE Migration Teams**

*Last Updated: October 14, 2025*
