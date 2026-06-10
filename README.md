# 🚀 Agentic Revenue Intelligence Platform (ARIP)

<p align="center">
  <img src="app/assets/Home.png" width="850"/>
</p>

> **A production-grade AI system that autonomously prioritizes high-conversion leads and executes personalized outreach using machine learning, multi-agent orchestration, and real-world tool integrations.**

---

## 🏆 Why This Project Matters

Sales teams often have thousands of leads but limited outreach capacity.

For example:

* 10,000 potential customers
* Only 60 outreach opportunities per day

The core challenge:

> **Who should we contact today to maximize revenue?**

ARIP solves this problem by:

1. Predicting which leads are most likely to respond and convert.
2. Ranking and selecting the highest-priority leads.
3. Planning the best outreach strategy.
4. Generating personalized messages.
5. Validating message quality.
6. Executing outreach.
7. Tracking results and learning from outcomes.

---

# 🎯 Key Features

### 🧠 Machine Learning Decisioning

* Response probability prediction
* Conversion probability prediction
* Priority scoring and ranking

### 🤖 Multi-Agent Architecture

* Planner Agent
* Executor Agent
* Validator Agent
* Optimizer Agent (feedback-ready)

### ⚙️ Decision Orchestrator

* Coordinates end-to-end workflow
* Enforces business constraints
* Maintains state and traceability

### 🛠 Tool Execution Layer (mock)

* Email sending 
* CRM updates
* LinkedIn outreach 

### 🗄 Persistent Storage

* PostgreSQL for campaigns and results
* Redis for workflow state and progress

### 📈 Observability

* Structured JSON logging
* Agent traces
* Campaign analytics
* Health monitoring

### 🐳 Deployment Ready

* Dockerfile included
* Cloud-ready architecture

---

[WATCH DEMO VIDEO](https://drive.google.com/file/d/1_GCoRW8gYpeNa47RNOxJVGB8XtjwyzhD/view?usp=sharing)


---

# 🏗️ System Architecture

```text
Client (CRM / Streamlit Dashboard / API User)
                ↓
        FastAPI API Gateway
                ↓
      Decision Orchestrator
                ↓
    ┌───────────────────────┐
    │   Multi-Agent Layer   │
    │ Planner → Executor →  │
    │ Validator → Optimizer │
    └───────────────────────┘
                ↓
        ML Decision Layer
                ↓
         Tool Execution
                ↓
     PostgreSQL + Redis
                ↓
 Observability & Feedback
```

---

# 🔄 End-to-End Workflow

```text
Lead Input
   ↓
ML Scoring
   ↓
Lead Ranking
   ↓
Top-K Selection (e.g., top 60)
   ↓
Planner Agent
   ↓
Executor Agent
   ↓
Validator Agent
   ↓
Retry Loop (if validation fails)
   ↓
Tool Execution (email/CRM)
   ↓
Campaign Completion
   ↓
Metrics + Analytics
```

---

# 🧠 Multi-Agent System

## Planner Agent

Determines the best outreach strategy.

**Inputs**:

* Lead attributes
* ML scores
* Campaign objective

**Outputs**:

* Tone
* Channel
* Follow-up strategy
* Personalization level

---

## Executor Agent

Generates personalized messages and executes actions.

**Can use**:

* Deterministic templates
* External LLMs (OpenAI, Groq, Anthropic)

---

## Validator Agent

Ensures quality and safety.

**Checks**:

* Spam language
* Generic messaging
* Tone mismatch
* Missing personalization

---

## Optimizer Agent

Feedback-driven strategy improvement.

**Learns from**:

* Open rate
* Reply rate
* Conversion rate

---

# 📊 Machine Learning Layer

Each lead receives:

* `response_prob`
* `conversion_prob`
* `priority_score`

### Example Output

```json
{
  "user_id": 123,
  "response_prob": 0.72,
  "conversion_prob": 0.41,
  "priority_score": 0.63,
  "rank": 1
}
```

---

# 🛠 Tech Stack

## Backend

* FastAPI
* Uvicorn
* Pydantic

## Frontend

* Streamlit

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Database

* PostgreSQL
* SQLAlchemy

## Cache / State

* Redis

## AI / LLM

* Groq

## DevOps

* Docker
* Docker Compose 

## Observability

* Structured logging
* Custom metrics

---

# 📁 Project Structure

```text
A.R.I.P/
├── app
│   ├── agents
│   │   ├── base_agent.py
│   │   ├── executor_agent.py
│   │   ├── planner_agent.py
│   │   ├── validator_agent.py
│   │   └── __init__.py
│   ├── api
│   │   ├── health.py
│   │   ├── routes.py
│   │   ├── tracer.py
│   │   └── __init__.py
│   ├── assets
│   │   ├── c1e8bb76-a050-444a-a0d5-1b6add55605b.webm
│   │   └── Home.png
│   ├── core
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   ├── redis_client.py
│   │   └── __init__.py
│   ├── db
│   │   ├── base.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── frontend
│   │   ├── components
│   │   │   ├── analytics.py
│   │   │   ├── campaign_results.py
│   │   │   ├── lead_table.py
│   │   │   └── metrics_card.py
│   │   ├── utils
│   │   │   ├── api.py
│   │   │   └── sample_data.py
│   │   └── app.py
│   ├── langgraph
│   │   ├── nodes
│   │   │   ├── executor_node.py
│   │   │   ├── finalize_node.py
│   │   │   ├── optimizer_node.py
│   │   │   ├── planner_node.py
│   │   │   └── validator_node.py
│   │   ├── graph.py
│   │   ├── routers.py
│   │   └── state.py
│   ├── llm
│   │   ├── chains.py
│   │   ├── prompts.py
│   │   └── provider.py
│   ├── ml
│   │   ├── data
│   │   │   ├── generate_data.py
│   │   │   └── leads_dataset.csv
│   │   ├── model
│   │   │   ├── lead_model.py
│   │   │   ├── lead_model_v1.pkl
│   │   │   └── provider.py
│   │   ├── services
│   │   │   └── scoring_service.py
│   │   └── __init__.py
│   ├── orchestrator
│   │   ├── orchestrator.py
│   │   ├── state.py
│   │   └── __init__.py
│   ├── schemas
│   │   ├── analytics.py
│   │   ├── campaign.py
│   │   ├── lead.py
│   │   └── __init__.py
│   └── tools
│       ├── email_tool.py
│       ├── langchain_tools.py
│       └── __init__.py
├── tests
│   └── test_scoring_pipeline.py
├── .dockerignore
├── .env
├── .gitignore
├── compose.yaml
├── Dockerfile
├── LICENSE
├── main.py
├── README.Docker.md
├── README.md
└── requirements.txt
```

# ⚡ API Endpoints

## POST `/api/score-leads`

Scores and ranks leads.

## POST `/api/run-outreach`

Runs the complete campaign pipeline.

## GET `/api/campaign-status/{campaign_id}`

Returns campaign progress and logs.

## GET `/api/campaign-analytics/{campaign_id}`

Returns campaign metrics and analytics.

## GET `/health`

Checks API, database, and Redis health.

---

# 📥 Sample Request

```json
{
  "leads": [
    {
      "user_id": 1,
      "name": "Kiran",
      "email": "user@example.com",
      "role": "Engineer",
      "years_experience": 3,
      "company": "Tesla",
      "company_size": 100,
      "activity_score": 5
    }
  ]
}
```

---

# 📤 Sample Response

```json
{
  "campaign_id": "0daa0c9a-cabb-4ce4-b966-d43221963008",
  "status": "completed",
  "selected": 1,
  "processed": 1,
  "top_score": 0.473,
  "results": [
    {
      "user_id": 1,
      "status": "success",
      "attempts": 1,
      "quality_score": 1.0
    }
  ]
}
```

---

# 🧪 Running Locally

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentic-revenue-intelligence-platform.git
cd agentic-revenue-intelligence-platform
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/ai_gatewayAPP_ENV=dev
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/arip
REDIS_URL=redis://localhost:6379/0
LLM_PROVIDER=groq
GROQ_API_KEY=PUT YOUR AI API KEY
GROQ_MODEL=llama-3.3-70b-versatile
```

## 5. Start PostgreSQL and Redis

If using Docker:

```bash
docker run --name arip-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=arip -p 5432:5432 -d postgres:16

docker run --name arip-redis -p 6379:6379 -d redis:7
```

## 6. Run the Backend

```bash
uvicorn main:app --reload
```

## 7. Open API Docs

```text
http://127.0.0.1:8000/docs
```

## 8. Run the Frontend

```bash
streamlit run frontend/app.py
```
---

## 7. Open API Docs

```text
http://localhost:8501 
```
---

# 🐳 Docker Support

Build:

```bash
docker build -t arip .
```

Run:

```bash
docker run -p 8000:8000 arip
```

---

# 📈 Analytics and Observability

ARIP tracks:

* Agent decisions
* Tool executions
* Validation failures
* Retry attempts
* Campaign duration
* Success rate
* Average attempts

Example metrics:

```json
{
  "total_processed": 100,
  "sent": 92,
  "failed": 8,
  "success_rate": 0.92,
  "avg_attempts": 1.14,
  "duration_seconds": 12.5
}
```

---

# 🔒 Business Constraints

ARIP supports real-world rules such as:

* Maximum outreach per day
* Spam-risk thresholds
* Quality thresholds
* Retry limits

Example:

```text
maximize(conversion)
subject to:
  daily_limit <= 60
  spam_risk <= threshold
```

---

# 🏅 Engineering Highlights

This project demonstrates:

* Production-grade FastAPI backend design
* Machine learning integration
* Multi-agent system architecture
* Workflow orchestration
* Redis-based state management
* PostgreSQL persistence
* Structured observability
* Cloud deployment readiness

---

# 🚀 Future Enhancements

## AI Enhancements

* RAG-based personalization
* A/B testing of prompts

## Product Enhancements

* Authentication and RBAC
* Integrating CRM & Mail tools (MCP)
* Webhook support

## Infrastructure

* CI/CD with GitHub Actions
* Kubernetes deployment

---

# ☁️ Deployment Roadmap (Upcoming)

### Backend

* Railway
* Render
* Fly.io
* AWS ECS

### Frontend Dashboard

* Streamlit

### Database

* PostgreSQL

### Cache

* Upstash Redis

---

# 📸 Demo Flow

1. Upload 1000+ leads.
2. Score and rank all leads.
3. Select top 60.
4. Generate personalized outreach.
5. Validate quality.
6. Execute outreach.
7. View logs and analytics.

---

# 📄 License

MIT License

---

# 👤 Author

**Kiran Biju**

Aspiring AI Engineer  | Backend AI Systems Builder

---

# ⭐ Final Verdict

ARIP is a top-tier portfolio project that combines:

* Real business impact
* Advanced AI architecture
* Production backend engineering
* Deployment readiness
