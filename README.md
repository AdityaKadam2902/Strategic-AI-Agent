# Strategic Debate Engine 🚀
 
An AI-powered multi-agent system for strategic business decision analysis. Six specialized AI agents debate decisions from multiple perspectives and deliver comprehensive analysis in 20 seconds.
 
![Strategic Debate Engine](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
 
## 🎯 Overview
 
The Strategic Debate Engine simulates an expert panel debate for business decisions. Instead of spending weeks consulting multiple experts, executives get comprehensive multi-perspective analysis instantly.
 
**Key Features:**
- 🤖 **6 Specialized AI Agents** - Pro, Con, Financial, Market, Judge, Confidence Scorer
- ⚡ **20-Second Analysis** - Parallel execution for maximum speed
- 📊 **Structured Outputs** - Confidence scores, ROI projections, risk assessments
- 🎨 **Beautiful UI** - Interactive React interface with real-time progress
- 🔒 **Type-Safe** - Pydantic models ensure data validation
 
## 🏗️ Architecture
 
```
User Input
    ↓
4 Specialist Agents (Parallel)
├─ Pro Agent (Arguments FOR)
├─ Con Agent (Arguments AGAINST)
├─ Financial Agent (ROI, Costs, Breakeven)
└─ Market Agent (Competition, Regulations)
    ↓
Judge Agent (Synthesis)
    ↓
Confidence Scorer (0-100)
    ↓
Final Decision + Analysis
```
 
### Multi-Agent System
 
Each agent has a specialized role:
 
1. **Pro Agent**: Identifies opportunities, strategic benefits, success factors
2. **Con Agent**: Highlights risks, challenges, alternative approaches
3. **Financial Agent**: Analyzes investment, ROI, breakeven, uncertainty
4. **Market Agent**: Assesses competition, regulations, market trends
5. **Judge Agent**: Synthesizes all inputs into final recommendation
6. **Confidence Scorer**: Calculates decision confidence (0-100)
 
Agents run in **parallel** using `asyncio.gather()` for 4x faster execution.
 
## 🛠️ Tech Stack
 
**Backend:**
- Python 3.10+
- FastAPI - Async web framework
- LangGraph - Multi-agent orchestration
- LangChain - LLM framework
- Groq AI - Ultra-fast inference (500+ tokens/sec)
- Pydantic - Data validation
 
**Frontend:**
- React 18
- Vanilla CSS (no build required)
- Responsive design
 
## 🚀 Quick Start
 
### Prerequisites
 
- Python 3.10 or higher
- Groq API key ([Get one here](https://console.groq.com/keys))
 
### Installation
 
1. **Clone the repository**
```bash
git clone https://github.com/yourusername/strategic-debate-engine.git
cd strategic-debate-engine
```
 
2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
 
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
 
4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```
 
5. **Run the server**
```bash
uvicorn app.main:app --reload
```
 
6. **Open the UI**
```bash
# Open frontend/index.html in your browser
# Or visit http://localhost:8000/docs for API documentation
```
 
## 📖 Usage
 
### Web Interface
 
1. Open `frontend/index.html` in your browser
2. Enter a strategic decision (or click an example)
3. Click "Start Debate 🚀"
4. Watch agents analyze in real-time
5. Review comprehensive results
 
### API Usage
 
**Endpoint:** `POST /debate`
 
**Request:**
```json
{
  "decision": "Should we invest $500K in AI-powered features?"
}
```
 
**Response:**
```json
{
  "decision": "Proceed with conditions",
  "confidence_score": 62,
  "opportunities": [
    "Launch AI-driven analytics dashboard",
    "AI-powered workflow automation",
    "Generative AI for reports"
  ],
  "risks": [
    "Financial exposure and cash flow strain",
    "Data privacy and compliance",
    "Integration complexity"
  ],
  "financial_summary": {
    "investment": "Approximately $500,000 total...",
    "roi_projection": "Target ROI of 150% over 3 years",
    "breakeven": "Approximately 20 months",
    "uncertainty": "medium"
  },
  "reasoning_summary": "The projected ROI and market signals justify..."
}
```
 
### API Documentation
 
Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
 
## 🎓 Example Decisions
 
Try these example questions:
 
1. **Market Expansion**: "Should we expand to Southeast Asian markets?"
2. **Product Strategy**: "Should we pivot from B2B to B2C?"
3. **M&A**: "Should we acquire our main competitor for $10M?"
4. **Technology**: "Should we migrate to microservices architecture?"
5. **Investment**: "Should we invest $500K in AI features?"
 
## 🧪 How It Works
 
### 1. Parallel Agent Execution
 
```python
# app/graph.py
results = await asyncio.gather(
    run_pro_agent(state),
    run_con_agent(state),
    run_financial_agent(state),
    run_market_agent(state),
    return_exceptions=True
)
```
 
Four agents analyze simultaneously, reducing latency by 75%.
 
### 2. LangGraph Orchestration
 
```python
workflow = StateGraph(DebateState)
workflow.add_node("specialist_agents", run_all_specialist_agents)
workflow.add_node("judge_agent", run_judge_agent)
workflow.add_node("confidence_scorer", run_confidence_scorer)
workflow.add_edge("specialist_agents", "judge_agent")
workflow.add_edge("judge_agent", "confidence_scorer")
```
 
LangGraph manages state flow and execution order.
 
### 3. Structured Outputs
 
```python
# app/models.py
class DebateResponse(BaseModel):
    decision: str
    confidence_score: int = Field(ge=0, le=100)
    opportunities: List[str]
    risks: List[str]
    financial_summary: Dict[str, str]
    reasoning_summary: str
```
 
Pydantic ensures type-safe, validated responses.
 
## 📁 Project Structure
 
```
strategic-debate-engine/
├── app/
│   ├── agents/           # AI agent implementations
│   │   ├── pro_agent.py
│   │   ├── con_agent.py
│   │   ├── financial_agent.py
│   │   ├── market_agent.py
│   │   ├── judge_agent.py
│   │   └── confidence.py
│   ├── utils/            # Utility functions
│   │   └── llm.py
│   ├── main.py           # FastAPI app
│   ├── graph.py          # LangGraph workflow
│   ├── state.py          # State definitions
│   ├── models.py         # Pydantic models
│   └── config.py         # Configuration
├── frontend/
│   └── index.html        # React UI
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore
└── README.md
```
 
## 🔧 Configuration
 
Edit `.env` to customize:
 
```bash
# Model Selection
MODEL_NAME=openai/gpt-oss-120b  # or llama-3.3-70b-versatile
 
# Model Parameters
TEMPERATURE=0.7   # Creativity (0.0-1.0)
MAX_TOKENS=2048   # Response length
 
# Server
HOST=0.0.0.0
PORT=8000
```
 
## 🤝 Contributing
 
Contributions are welcome! Please:
 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 
 
## 🙏 Acknowledgments
 
- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration
- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
 
## 📧 Contact
 
**Aditya Kadam** - [LinkedIn](https://www.linkedin.com/in/aditya-kadam-268304252?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
 
Project Link: (https://github.com/AdityaKadam2902/Strategic-AI-Agent)
 
## 🌟 Star History
 
If you find this project useful, please give it a star! ⭐
 
---
 
**Built with Python, FastAPI, LangGraph, and React**
 
 
