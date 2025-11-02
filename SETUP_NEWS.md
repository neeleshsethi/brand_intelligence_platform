# News Intelligence Setup Guide

## ✅ Completed Steps

1. ✅ Database tables created in Supabase (`news_articles`, `brand_news_relevance`)
2. ✅ Tavily integration code complete
3. ✅ News service built (multi-tier search)
4. ✅ API endpoints created (`GET /api/news/{brand_id}`)
5. ✅ Tavily package installed
6. ✅ Analyzer agent enhanced with news context
7. ✅ Frontend news API client added
8. ✅ "Recent Market Intelligence" section added to CompetitiveIntel page
9. ✅ News indicators added to Dashboard (badges showing article count and high-priority alerts)
10. ✅ Loading steps updated to show "Fetching latest market intelligence..."

## 🔑 Required: Get Tavily API Key

### Step 1: Sign up for Tavily (2 minutes)
1. Go to https://tavily.com
2. Click "Get API Key" or "Sign Up"
3. Free tier includes **1,000 searches/month** (plenty for demo)
4. Copy your API key

### Step 2: Add to Backend .env
Open `backend/.env` and add:
```
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Restart Backend
```bash
docker-compose restart backend
```

## 🧪 Test the News API

Once API key is added, test it:

```bash
# Get brand ID for Eliquis
curl http://localhost:8000/api/brands | jq '.[] | select(.name=="Eliquis") | .id'

# Fetch news for that brand (replace with actual ID)
curl "http://localhost:8000/api/news/4fea864b-a447-43ce-989f-98343dee7213?refresh=true"
```

Expected response:
```json
{
  "brand_id": "...",
  "articles": [
    {
      "title": "Pfizer's Eliquis revenue jumps...",
      "source": "FiercePharma",
      "published_at": "2024-11-01...",
      "sentiment": "positive",
      "priority": "high"
    }
  ],
  "total_count": 15,
  "high_priority_count": 5
}
```

## 🎯 What's Now Working

Once you add the Tavily API key, you'll have:

1. **Real-time Market Intelligence** - Fetches news from pharmaceutical sources
2. **AI Analysis with Context** - Analyzer agent now uses recent news to ground insights
3. **Dashboard News Badges** - See high-priority alerts and total article counts per brand
4. **Recent News Section** - Browse latest articles on CompetitiveIntel page with priority/sentiment tags
5. **News Citations** - AI insights reference specific market events and news sources

## 🎯 Optional Future Enhancements

- Add news filtering by sentiment/priority/date range
- Create dedicated News tab for deep-dive analysis
- Add email alerts for high-priority news
- Export news reports to PDF
- Track competitor mentions over time

## 🐛 Troubleshooting

**"TAVILY_API_KEY not set"**
- Check backend/.env has the key
- Restart Docker container

**"No articles returned"**
- Check Tavily API key is valid
- Brand name might not have recent news (try "Eliquis" or "Paxlovid")

**"Database error"**
- Verify Supabase migration ran successfully
- Check tables exist in brand_planning schema

## 📊 Demo Flow

For tomorrow's demo:
1. Show dashboard (news count badges appear)
2. Click "Analyze Brand"
3. Before analysis, show "Recent Market Intelligence" section
4. Run analysis - insights now cite news sources
5. Show "This article from FiercePharma on Nov 1..."
