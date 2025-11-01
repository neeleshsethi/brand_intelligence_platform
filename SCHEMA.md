# Database Schema Documentation

## Schema: `brand_planning`

All tables are organized under the `brand_planning` schema in Supabase PostgreSQL.

---

## Tables

### 1. `brand_planning.brands`

Stores pharmaceutical brands being tracked and analyzed.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `name` | VARCHAR(255) | NOT NULL | Brand name (e.g., "Paxlovid", "Eliquis") |
| `company` | VARCHAR(255) | NOT NULL | Pharmaceutical company (e.g., "Pfizer") |
| `therapeutic_area` | VARCHAR(255) | NOT NULL | Medical category (e.g., "COVID-19 Antiviral") |
| `market_share` | DECIMAL(5,2) | CHECK (0-100) | Market share percentage |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`

**Triggers:**
- `update_brands_updated_at`: Automatically updates `updated_at` on row modification

**Example Data:**
```json
{
  "id": "uuid-here",
  "name": "Paxlovid",
  "company": "Pfizer",
  "therapeutic_area": "COVID-19 Antiviral",
  "market_share": 65.4,
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

---

### 2. `brand_planning.insights`

Stores AI-generated insights about brands with confidence scoring and human validation.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `brand_id` | UUID | NOT NULL, FK → brands(id), ON DELETE CASCADE | Associated brand |
| `type` | VARCHAR(100) | NOT NULL | Insight type (see types below) |
| `content` | TEXT | NOT NULL | Main insight content |
| `confidence_score` | DECIMAL(3,2) | CHECK (0-1) | AI confidence (0.0-1.0) |
| `ai_reasoning` | TEXT | NULL | Explanation of AI's analysis |
| `human_validated` | BOOLEAN | DEFAULT FALSE | Whether reviewed by human |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last update timestamp |

**Insight Types:**
- `market_research`
- `competitor_analysis`
- `target_audience`
- `messaging_strategy`
- `channel_planning`
- `budget_optimization`

**Indexes:**
- Primary key on `id`
- `idx_insights_brand_id` on `brand_id`
- `idx_insights_type` on `type`
- `idx_insights_created_at` on `created_at DESC`

**Foreign Keys:**
- `brand_id` → `brand_planning.brands(id)` ON DELETE CASCADE

**Triggers:**
- `update_insights_updated_at`: Automatically updates `updated_at` on row modification

**Example Data:**
```json
{
  "id": "uuid-here",
  "brand_id": "brand-uuid",
  "type": "competitor_analysis",
  "content": "Paxlovid maintains significant market lead over Lagevrio...",
  "confidence_score": 0.92,
  "ai_reasoning": "Analysis of IQVIA prescription data, clinical trial efficacy comparisons...",
  "human_validated": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

### 3. `brand_planning.brand_plans`

Stores complete brand planning strategies as JSON with versioning support.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `brand_id` | UUID | NOT NULL, FK → brands(id), ON DELETE CASCADE | Associated brand |
| `plan_json` | JSONB | NOT NULL | Complete plan structure (see schema below) |
| `version` | INTEGER | NOT NULL, DEFAULT 1 | Plan version number |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last update timestamp |

**Constraints:**
- UNIQUE(`brand_id`, `version`) - One version per brand

**Indexes:**
- Primary key on `id`
- `idx_brand_plans_brand_id` on `brand_id`
- `idx_brand_plans_version` on `version DESC`

**Foreign Keys:**
- `brand_id` → `brand_planning.brands(id)` ON DELETE CASCADE

**Triggers:**
- `update_brand_plans_updated_at`: Automatically updates `updated_at` on row modification

**Plan JSON Schema:**
```json
{
  "executive_summary": "string",
  "time_period": "string",
  "objectives": ["string", "..."],
  "target_audiences": [
    {
      "segment": "string",
      "size": "string",
      "priority": "string",
      "key_message": "string"
    }
  ],
  "strategies": {
    "market_access": "string",
    "medical_education": "string",
    "patient_engagement": "string",
    "competitive": "string (optional)"
  },
  "channels": [
    {
      "name": "string",
      "budget_pct": number,
      "focus": "string"
    }
  ],
  "budget": {
    "total": number,
    "currency": "string",
    "breakdown": {
      "channel_name": number
    }
  },
  "kpis": [
    {
      "metric": "string",
      "target": "string",
      "current": "string"
    }
  ],
  "risks": ["string", "..."]
}
```

**Example Data:**
```json
{
  "id": "uuid-here",
  "brand_id": "brand-uuid",
  "version": 1,
  "plan_json": {
    "executive_summary": "Paxlovid transition strategy from pandemic to endemic",
    "time_period": "2025 Q1-Q4",
    "objectives": [
      "Maintain market leadership position (>60% share)",
      "Expand to long-COVID prevention indication"
    ],
    "budget": {
      "total": 45000000,
      "currency": "USD"
    }
  },
  "created_at": "2025-01-15T11:00:00Z",
  "updated_at": "2025-01-15T11:00:00Z"
}
```

---

## Relationships

```
brands (1) ──< insights (many)
brands (1) ──< brand_plans (many)
```

- One brand can have many insights
- One brand can have many plan versions
- All relationships use CASCADE DELETE

---

## Schema Access

### Python (Supabase Client)

```python
from db import get_table

# Query brands
brands = get_table("brands").select("*").execute()

# Query insights for a specific brand
insights = get_table("insights").select("*").eq("brand_id", brand_id).execute()

# Get latest plan version
latest_plan = (
    get_table("brand_plans")
    .select("*")
    .eq("brand_id", brand_id)
    .order("version", desc=True)
    .limit(1)
    .execute()
)
```

### SQL Direct Access

```sql
-- Set schema search path
SET search_path TO brand_planning, public;

-- Query with schema prefix
SELECT * FROM brand_planning.brands;
SELECT * FROM brand_planning.insights WHERE type = 'market_research';
SELECT * FROM brand_planning.brand_plans WHERE version = 1;
```

---

## Migration File

Location: `backend/db/migrations/001_initial_schema.sql`

Run this file in Supabase SQL Editor to create the complete schema.

---

## Seed Data

Location: `backend/db/seeds/seed_data.py`

Run: `cd backend && python -m db.seeds.seed_data`

Includes:
- 4 pharmaceutical brands (Paxlovid, Lagevrio, Eliquis, Xarelto)
- 10 realistic AI insights across all types
- 2 complete brand plans with full strategic details
