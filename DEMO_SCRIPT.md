# Pfizer AI Brand Planning Platform - Demo Script

## 🎯 Overview
A 2-minute walkthrough showcasing AI-powered competitive intelligence and brand planning for pharmaceutical brands.

**Target Audience:** Pharmaceutical executives, brand managers, strategic planning teams
**Demo Duration:** 2-3 minutes
**Key Message:** AI agents can accelerate strategic planning from weeks to minutes

---

## 🚀 Pre-Demo Checklist

### Backend Setup
```bash
cd backend

# Quick start with convenience script (recommended!)
./run_demo.sh

# OR manually with environment variables:
# export DEMO_MODE=true
# export MOCK_MODE=true
# uv run uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Verify Demo Data
- Ensure Supabase is running with seed data
- Brands available: Paxlovid, Lagevrio, Eliquis, Xarelto
- Navigate to `http://localhost:5173`

---

## 📋 2-Minute Demo Script

### **[0:00-0:20] Opening - Dashboard Overview**

**Say:**
> "Welcome to our AI Brand Planning Platform. We've built this to help pharmaceutical teams accelerate strategic planning from weeks to minutes using specialized AI agents."

**Do:**
- Show the clean dashboard
- Point out the 4 pharmaceutical brands
- Highlight the two main features: Competitive Intelligence and Brand Planning

**Key Points:**
- ✅ Real pharmaceutical data (COVID antivirals, anticoagulants)
- ✅ Market share, therapeutic areas visible
- ✅ Two core workflows: Analyze and Plan

---

### **[0:20-1:20] Feature #1 - Competitive Intelligence Analysis**

**Say:**
> "Let's analyze Paxlovid's competitive position. I'll click 'Analyze Brand' and our AI agents go to work."

**Do:**
1. Click "Analyze Brand" on Paxlovid
2. Watch the multi-step loading animation
   - "Gathering brand data..."
   - "Analyzing competitive landscape..."
   - "Evaluating market position..."
   - "Generating strategic insights..."

**When results appear:**

**Say:**
> "In seconds, we get a complete competitive analysis with three powerful views:"

**Show (spend 10 seconds each):**
1. **Positioning Matrix** (2x2 chart)
   - "Here's Paxlovid vs Lagevrio on price and efficacy"
   - Paxlovid is highlighted in Pfizer blue

2. **SWOT Analysis** (4 quadrants)
   - "Color-coded SWOT with strengths, weaknesses, opportunities, threats"
   - Point to 1-2 specific items

3. **AI-Generated Insights** (3 cards with confidence scores)
   - "Watch these confidence scores animate - our AI is transparent about certainty"
   - Click "View AI Reasoning" on one card
   - "Every recommendation shows the AI's reasoning"
   - Click "Validate" on an insight → Success toast appears

**Key Points:**
- ✅ Multi-step AI processing visible
- ✅ **WOW MOMENT #1:** Animated confidence scores counting up
- ✅ **WOW MOMENT #2:** Expandable AI reasoning
- ✅ Interactive validation/rejection
- ✅ Complete in ~5 seconds with DEMO_MODE

---

### **[1:20-2:00] Feature #2 - Brand Plan Generator**

**Say:**
> "Now let's generate a complete 12-month brand plan. Normally this takes weeks of work."

**Do:**
1. Click "Back to Dashboard"
2. Click "Create Plan" on Eliquis
3. Show the form:
   - Brand: Eliquis (already selected)
   - Market: US (default)
4. Click "Generate AI-Powered Plan"

**Watch the loading:**
- "Researching market..."
- "Formulating strategy..."
- "Creating projections..."
- "Finalizing plan..."

**When complete:**

**Say:**
> "And here's our comprehensive strategic plan!"

**Show (quickly scroll through):**
1. **Market Share Projection Chart**
   - "12-month growth projection with beautiful visualization"
   - Point to the gradient area chart

2. **Expandable Plan Sections** (show 2-3)
   - "Every section is AI-generated - see the badges?"
   - Click to expand "Strategic Objectives"
   - Click to expand "Budget Allocation" ($5M breakdown)

3. **Export Feature**
   - Click "Export to PDF" → Success toast + **CONFETTI! 🎉**

**Key Points:**
- ✅ **WOW MOMENT #3:** Confetti celebration on plan generation
- ✅ Professional chart visualization
- ✅ 8 comprehensive plan sections
- ✅ Fake but impressive export functionality
- ✅ Complete in ~6 seconds with DEMO_MODE

---

### **[2:00-2:20] Closing - Key Takeaways**

**Say:**
> "In just 2 minutes, we've shown what typically takes weeks:
> - Complete competitive intelligence with AI-powered insights
> - 12-month strategic plan with budget, KPIs, and timeline
> - All transparent, explainable, and validated by your team
>
> This is a 2-day prototype, but imagine scaling this across your entire portfolio."

**Optional Next Steps:**
- Show the 6 specialized AI agents (if technical audience)
- Demonstrate scenario analysis endpoint (if time permits)
- Discuss customization for specific therapeutic areas

---

## 🔥 "Wow" Moments to Emphasize

### 1. **Animated Confidence Scores**
- Watch them count up from 0% to final value
- Shows AI transparency
- Different colors for different confidence levels

### 2. **Expandable AI Reasoning**
- Click "View AI Reasoning" on any insight
- Every recommendation is explainable
- Builds trust in AI outputs

### 3. **Confetti on Plan Generation**
- Celebrates completion
- Makes the demo memorable
- Shows polish and attention to detail

### 4. **Speed**
- With DEMO_MODE: ~2 seconds per operation
- Without DEMO_MODE: ~5-8 seconds (still impressive)
- Traditional process: Weeks

---

## 🛠️ Backup Plan (If Something Breaks)

### If Backend is Down:
1. Switch to MOCK_MODE (already built in)
2. Refresh the frontend
3. Continue demo - all mock responses are pre-loaded

### If Frontend Errors:
1. Check browser console for errors
2. Common fix: Clear browser cache and reload
3. Fallback: Show screenshots from `docs/screenshots/` (create these)

### If Data is Missing:
1. Re-run seed script: `python backend/db/seeds/seed_data.py`
2. Or use the hardcoded brand IDs in the frontend

### If Charts Don't Load:
- Charts are built with Recharts (reliable)
- Check that brand has `market_share` field
- Fallback: Focus on other features

---

## 📊 Technical Details (If Asked)

### Architecture:
- **Backend:** FastAPI + 6 Specialized AI Agents + Supabase
- **Frontend:** React + TypeScript + Tailwind + Recharts
- **AI:** OpenAI GPT-4 with structured outputs (Instructor library)
- **Tracing:** LangSmith for observability

### The 6 AI Agents:
1. **AnalyzerAgent** - Market insights, gaps, opportunities
2. **StrategyAgent** - SWOT, positioning, recommendations
3. **BrandPlanAgent** - Complete strategic plans
4. **ScenarioAgent** - What-if analysis, risk assessment
5. **ValidatorAgent** - Confidence scoring, quality checks
6. **InsightDiscoveryAgent** - Novel market insights

### Demo Mode Features:
- `DEMO_MODE=true` → Cached responses for instant results
- `MOCK_MODE=true` → No API calls, hardcoded responses
- Both can be toggled via environment variables

### Data:
- **Real brands:** Paxlovid, Lagevrio, Eliquis, Xarelto
- **Realistic market shares:** Based on actual market data
- **Complete seed data:** 10 insights, 2 full brand plans

---

## 🎨 Visual Polish to Highlight

1. **Color Scheme**
   - Pfizer Blue (#0093D0) throughout
   - Consistent, professional branding

2. **Animations**
   - Fade-in effects on all content
   - Slide-in for details
   - Count-up for numbers
   - Confetti for celebrations

3. **Loading States**
   - Multi-step progress indicators
   - Clear messaging about what AI is doing
   - No blank screens

4. **Interactive Elements**
   - Hover states on all buttons
   - Expandable sections
   - Toast notifications for feedback

---

## 💡 Questions You Might Get

### "How accurate is the AI?"
> "We show confidence scores on every insight. The AI is transparent about certainty, and your team can validate or reject recommendations. Think of it as AI-assisted, not AI-automated."

### "Can it handle our therapeutic area?"
> "Absolutely. The agents are designed to be therapeutic-area agnostic. We just need to train them on your specific market data and competitive landscape."

### "How long did this take to build?"
> "This is a 2-day rapid prototype. A production version would include: custom agent training, integration with your data sources, advanced analytics, and role-based access control."

### "What about data security?"
> "In production, we'd use your private LLM deployment or on-premise hosting. All data stays within your security perimeter. The AI agents are just the orchestration layer."

### "Can we customize the outputs?"
> "Yes! All prompts are in separate files (backend/agents/prompts/). You can tune the outputs, add your brand voice, and customize for different stakeholders."

---

## 🎬 Demo Tips

### Before You Start:
- ✅ Close unnecessary browser tabs
- ✅ Zoom browser to 100% (not 125% or 150%)
- ✅ Have backend and frontend logs visible (optional, for technical audiences)
- ✅ Test the full flow once before the real demo

### During Demo:
- 🗣️ Talk while things are loading (don't just watch spinners)
- 👆 Use your cursor to guide attention
- 🎯 Focus on business value, not technical details (unless asked)
- ⏱️ Keep it moving - 2 minutes feels short but it's enough

### After Demo:
- 📧 Offer to send technical architecture docs
- 🤝 Ask what therapeutic areas they'd want to prioritize
- 📅 Suggest a follow-up to show scenario analysis or other features

---

## 📝 Success Metrics

**You'll know the demo was successful if:**
1. ✅ They ask "Can we try it with our brands?"
2. ✅ They want to see the technical architecture
3. ✅ They ask about timeline to production
4. ✅ They mention specific use cases or pain points

**Red flags:**
- ❌ They question AI accuracy without seeing confidence scores
- ❌ They think it's just GPT with a nice UI (show the 6 agents!)
- ❌ They don't understand the value prop (re-emphasize weeks → minutes)

---

## 🔗 Quick Links

- **Frontend:** http://localhost:5173
- **Backend API Docs:** http://localhost:8000/docs
- **LangSmith Dashboard:** https://smith.langchain.com (if tracing enabled)
- **GitHub Repo:** [Add your repo link]

---

## 🎯 The One-Sentence Pitch

> "Transform weeks of strategic planning into minutes with AI agents that analyze competitors, generate brand plans, and provide transparent, validated recommendations."

---

**Good luck with your demo! 🚀**
