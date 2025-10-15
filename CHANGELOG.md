# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-10-15

### ✨ Added
- **Rejection Reason Display**: Now prominently shows why Q&A pairs were rejected
  - Red banner with AlertTriangle icon
  - Clear explanation of which criteria failed hard minimums
  - Example: "Failed hard minimum on: CITATION_ACCURACY, LEGAL_REASONING"

### 🎯 Features

#### Rejection Reason UI
```
┌───────────────────────────────────────────────┐
│ ❌ QUESTION_2                    SCORE: 20    │
├───────────────────────────────────────────────┤
│ ⚠️  REJECTION_REASON:                         │
│     Failed hard minimum on:                   │
│     CITATION_ACCURACY, LEGAL_REASONING        │
├───────────────────────────────────────────────┤
│ CITATION_ACCURACY:  20/100 ✗                  │
│ LEGAL_REASONING:    20/100 ✗                  │
└───────────────────────────────────────────────┘
```

## [1.1.0] - 2025-10-15

### ✨ Added
- **OpenAI O1 Reasoning Models**: Added support for o1 and o1-mini models
  - O1: 98% accuracy, deep thinking, best for complex analysis
  - O1-Mini: 94% accuracy, fast reasoning, optimized for STEM
  - Special handling for reasoning models (no system messages, no temperature)
  - 🧠 REASONING badges in UI
  
- **TXT File Support**: Parse and evaluate plain text files alongside PDFs
  - UTF-8 and Latin-1 encoding support
  - Same Q&A format as PDF files
  - File input now accepts `.pdf,.txt,text/plain`

### 📚 Documentation
- Added `docs/REASONING_MODELS.md` with comprehensive guide
  - Model comparison and selection guide
  - Cost analysis and performance insights
  - API usage examples
  - When to use reasoning vs regular models

### 🔧 Technical Changes
- Updated `schemas.py`: Added o1 models to Literal type
- Modified `llm_judge.py`: Special API handling for reasoning models
- Enhanced `evaluate.py`: Added o1 model metadata and validation
- Frontend: New model cards with reasoning indicators

### 💰 Cost Structure
| Model | Accuracy | Cost/Eval | Best For |
|-------|----------|-----------|----------|
| O1 | 98% | $0.15 | Complex legal analysis |
| O1-Mini | 94% | $0.03 | STEM & code tasks |
| Claude Sonnet 4 | 95% | $0.03 | Balanced performance |
| GPT-4o | 92% | $0.025 | General purpose |
| GPT-4o-Mini | 85% | $0.002 | High volume |

## [1.0.0] - 2025-10-14

### 🚀 Initial Release
- FastAPI backend with async support
- Multi-criterion evaluation system
- PDF parsing with PyMuPDF4LLM
- Support for GPT-4o, GPT-4o-mini, Claude Sonnet 4
- React frontend with brutalist design
- Railway deployment configuration
- Comprehensive evaluation metrics
- Hard minimum threshold enforcement
- Weighted scoring system
- Domain-specific criteria (legal, medical, finance)

### 📦 Deployment
- Backend: Railway (https://web-production-446a5.up.railway.app)
- Frontend: Vercel
- GitHub: AryanMarwah7781/llm-judge

### 🎨 UI Features
- Hero landing page
- Domain selection
- Criteria customization
- Model selection with specs
- Real-time evaluation progress
- Detailed results with pass/fail verdicts
- Debug panel with API request logs

### 🔐 Security
- Environment-based API key management
- CORS configuration
- Input validation with Pydantic

### 📝 Documentation
- `README.md`: Quick start guide
- `docs/DEPLOYMENT.md`: Deployment instructions
- `docs/QUICK_DEPLOY.md`: Fast deployment guide
- `docs/RAILWAY_DEPLOY.md`: Railway-specific guide
- `docs/STRUCTURE.md`: Project architecture
- `docs/DESIGN.md`: Design decisions
- `docs/CUSTOM_DOMAIN.md`: Domain setup guide

### 🧪 Testing
- 12 law-based test files
- Various scenarios (perfect, incorrect, incomplete)
- Advanced legal topics
- Example usage scripts

## Future Roadmap

### 🎯 Planned Features
- [ ] Batch evaluation API endpoint
- [ ] PDF report generation
- [ ] Webhook support for async evaluations
- [ ] Custom criteria templates
- [ ] Evaluation history dashboard
- [ ] Multi-file uploads
- [ ] Team collaboration features
- [ ] Cost tracking and analytics

### 🔮 Under Consideration
- [ ] Support for more LLM providers (Google, Cohere)
- [ ] Fine-tuned models for specific domains
- [ ] Integration with LangSmith/LangChain
- [ ] Desktop app (Electron)
- [ ] Mobile app
- [ ] Browser extension
- [ ] Slack/Discord bots

---

**Version Format**: [Major].[Minor].[Patch]
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes and minor improvements
