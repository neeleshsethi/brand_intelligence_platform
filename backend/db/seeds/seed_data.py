"""
Seed data for Pfizer AI Brand Planning prototype.
Includes realistic pharmaceutical brand data and AI-generated insights.
"""

from typing import List, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db.supabase_client import get_table


# Pharmaceutical brands data
BRANDS_DATA = [
    {
        "name": "Paxlovid",
        "company": "Pfizer",
        "therapeutic_area": "COVID-19 Antiviral",
        "market_share": 65.4,
    },
    {
        "name": "Lagevrio",
        "company": "Merck",
        "therapeutic_area": "COVID-19 Antiviral",
        "market_share": 34.6,
    },
    {
        "name": "Eliquis",
        "company": "Pfizer/Bristol Myers Squibb",
        "therapeutic_area": "Anticoagulant (Blood Thinner)",
        "market_share": 42.3,
    },
    {
        "name": "Xarelto",
        "company": "Johnson & Johnson/Bayer",
        "therapeutic_area": "Anticoagulant (Blood Thinner)",
        "market_share": 38.7,
    },
]


def get_insights_data(brand_ids: Dict[str, str]) -> List[Dict]:
    """Generate insights data with brand IDs."""
    return [
        # Paxlovid insights
        {
            "brand_id": brand_ids["Paxlovid"],
            "type": "market_research",
            "content": "COVID-19 antiviral market shows declining demand as pandemic transitions to endemic phase. Projected 35% YoY decline in prescriptions, but increased focus on high-risk populations maintains strategic value.",
            "confidence_score": 0.87,
            "ai_reasoning": "Based on CDC surveillance data, prescription trends from Q4 2024, and epidemiological modeling. High confidence due to consistent data sources across multiple regions.",
            "human_validated": True,
        },
        {
            "brand_id": brand_ids["Paxlovid"],
            "type": "competitor_analysis",
            "content": "Paxlovid maintains significant market lead over Lagevrio (65% vs 35% market share) due to stronger efficacy data and physician preference. However, Merck's pricing strategy and oral convenience factor remain competitive advantages.",
            "confidence_score": 0.92,
            "ai_reasoning": "Analysis of IQVIA prescription data, clinical trial efficacy comparisons (89% vs 30% hospitalization reduction), and physician survey data from 1,200+ respondents.",
            "human_validated": True,
        },
        {
            "brand_id": brand_ids["Paxlovid"],
            "type": "target_audience",
            "content": "Primary target: Adults 65+ with 2+ comorbidities (diabetes, cardiovascular disease). Secondary: Immunocompromised patients 18-64. Key messaging: early treatment within 5 days of symptom onset.",
            "confidence_score": 0.89,
            "ai_reasoning": "CDC high-risk population guidelines, real-world evidence studies, and current prescribing patterns indicate this segmentation optimizes treatment outcomes.",
            "human_validated": False,
        },
        # Lagevrio insights
        {
            "brand_id": brand_ids["Lagevrio"],
            "type": "market_research",
            "content": "Lagevrio faces headwinds from superior competitor efficacy but maintains niche in patients with drug-drug interaction concerns with nirmatrelvir/ritonavir combination.",
            "confidence_score": 0.84,
            "ai_reasoning": "EHR analysis of prescription patterns shows 40% of Lagevrio prescriptions driven by CYP3A4 interaction concerns, particularly in patients on immunosuppressants.",
            "human_validated": False,
        },
        # Eliquis insights
        {
            "brand_id": brand_ids["Eliquis"],
            "type": "market_research",
            "content": "Non-vitamin K oral anticoagulant (NOAC) market growing at 8.2% CAGR. Eliquis leads with 42.3% share, driven by strong atrial fibrillation indication and favorable bleeding profile vs warfarin.",
            "confidence_score": 0.91,
            "ai_reasoning": "Multi-source analysis: IQVIA market data, ARISTOTLE trial long-term follow-up, real-world comparative effectiveness studies across 4M+ patients.",
            "human_validated": True,
        },
        {
            "brand_id": brand_ids["Eliquis"],
            "type": "competitor_analysis",
            "content": "Eliquis vs Xarelto: Eliquis advantages include BID dosing flexibility and perceived safety profile. Xarelto counters with QD convenience and VTE treatment indication strength. Market share gap narrowing 0.3% per quarter.",
            "confidence_score": 0.88,
            "ai_reasoning": "Trend analysis of 18-month prescription data, physician preference surveys, and head-to-head trial meta-analyses. Market dynamics suggest continued competition.",
            "human_validated": True,
        },
        {
            "brand_id": brand_ids["Eliquis"],
            "type": "messaging_strategy",
            "content": "Lead with 'Proven Stroke Prevention + Lower Bleeding Risk' message to cardiologists. Emphasize reversibility with Andexxa for emergency departments. Focus digital outreach on patient education regarding adherence.",
            "confidence_score": 0.82,
            "ai_reasoning": "Message testing across 3 physician focus groups and 500-patient digital survey. Safety messaging resonates strongest with prescribers, adherence with patients.",
            "human_validated": False,
        },
        # Xarelto insights
        {
            "brand_id": brand_ids["Xarelto"],
            "type": "competitor_analysis",
            "content": "Xarelto's once-daily dosing remains key differentiator vs Eliquis BID. Strong in VTE treatment/prevention (DVT/PE) where QD dosing improves adherence. Afib market more competitive.",
            "confidence_score": 0.86,
            "ai_reasoning": "Adherence studies show 12% better compliance with QD vs BID regimens. EINSTEIN trial data supports VTE leadership positioning.",
            "human_validated": False,
        },
        {
            "brand_id": brand_ids["Xarelto"],
            "type": "channel_planning",
            "content": "Optimize rep deployment toward high-volume VTE centers and orthopedic surgeons for post-operative prophylaxis. Reduce detail frequency in primary care where Eliquis has strong presence.",
            "confidence_score": 0.79,
            "ai_reasoning": "Territory analysis of 12,000+ HCPs shows 60% higher ROI in specialist vs PCP segments for Xarelto. Statistical modeling of sales-to-detail ratios.",
            "human_validated": False,
        },
        {
            "brand_id": brand_ids["Xarelto"],
            "type": "budget_optimization",
            "content": "Shift 25% of DTC budget from broad TV to targeted digital (afib patients, post-surgery populations). Increase medical education spend by 15% focusing on VTE guidelines and real-world evidence.",
            "confidence_score": 0.75,
            "ai_reasoning": "Attribution modeling shows digital channels have 3.2x higher conversion rate. HCP engagement data indicates evidence-based content drives switching behavior.",
            "human_validated": False,
        },
    ]


def get_brand_plans_data(brand_ids: Dict[str, str]) -> List[Dict]:
    """Generate brand plan data with brand IDs."""
    return [
        {
            "brand_id": brand_ids["Paxlovid"],
            "version": 1,
            "plan_json": {
                "executive_summary": "Paxlovid transition strategy from pandemic emergency to endemic standard of care for high-risk COVID-19 patients",
                "time_period": "2025 Q1-Q4",
                "objectives": [
                    "Maintain market leadership position (>60% share)",
                    "Expand to long-COVID prevention indication",
                    "Educate 50,000+ PCPs on early treatment protocols",
                ],
                "target_audiences": [
                    {
                        "segment": "Primary Care Physicians",
                        "size": "120,000 HCPs",
                        "priority": "High",
                        "key_message": "Early treatment within 5 days reduces hospitalization by 89%",
                    },
                    {
                        "segment": "High-risk patients 65+",
                        "size": "8.5M patients",
                        "priority": "High",
                        "key_message": "Proven protection when you need it most",
                    },
                ],
                "strategies": {
                    "market_access": "Secure long-term government stockpiling contracts, expand Medicare coverage",
                    "medical_education": "CME programs on antiviral stewardship, real-world evidence campaigns",
                    "patient_engagement": "Digital symptom checker tools, pharmacy partnerships for rapid access",
                },
                "channels": [
                    {"name": "Sales Force", "budget_pct": 35, "focus": "PCP education and practice integration"},
                    {"name": "Digital/HCP", "budget_pct": 25, "focus": "Medical education and treatment guidelines"},
                    {"name": "DTC Digital", "budget_pct": 20, "focus": "High-risk patient awareness"},
                    {"name": "Medical Affairs", "budget_pct": 20, "focus": "KOL engagement and evidence generation"},
                ],
                "budget": {
                    "total": 45000000,
                    "currency": "USD",
                    "breakdown": {
                        "sales_force": 15750000,
                        "digital_hcp": 11250000,
                        "dtc": 9000000,
                        "medical_affairs": 9000000,
                    },
                },
                "kpis": [
                    {"metric": "Market Share", "target": "62%", "current": "65.4%"},
                    {"metric": "NRx Growth", "target": "-30% (vs -35% market)", "current": "baseline"},
                    {"metric": "HCP Awareness", "target": "75%", "current": "68%"},
                    {"metric": "Time to Treatment", "target": "<3 days avg", "current": "3.8 days"},
                ],
                "risks": [
                    "Declining COVID incidence reduces prescriptions faster than projected",
                    "Competitor pipeline: new antivirals in Phase 3 with improved resistance profiles",
                    "Payer coverage restrictions to generic alternatives if authorized",
                ],
            },
        },
        {
            "brand_id": brand_ids["Eliquis"],
            "version": 1,
            "plan_json": {
                "executive_summary": "Eliquis growth strategy focused on maintaining atrial fibrillation market leadership and expanding share in VTE prevention",
                "time_period": "2025 Full Year",
                "objectives": [
                    "Defend 42% market share in atrial fibrillation",
                    "Grow VTE prevention market by 8%",
                    "Launch post-MI indication expansion",
                ],
                "target_audiences": [
                    {
                        "segment": "Cardiologists",
                        "size": "25,000 HCPs",
                        "priority": "Critical",
                        "key_message": "Superior stroke prevention with lower major bleeding vs warfarin and competitors",
                    },
                    {
                        "segment": "Afib patients 65+",
                        "size": "6.1M patients",
                        "priority": "High",
                        "key_message": "Take your stroke risk off the table with proven protection",
                    },
                    {
                        "segment": "Primary Care Physicians",
                        "size": "180,000 HCPs",
                        "priority": "Medium",
                        "key_message": "Simple, effective anticoagulation for your afib patients",
                    },
                ],
                "strategies": {
                    "market_access": "Maintain preferred formulary status, expand Medicare Advantage coverage",
                    "medical_education": "Real-world evidence campaigns, bleeding risk calculators, reversal agent training",
                    "patient_engagement": "Adherence programs, afib education apps, stroke risk awareness",
                    "competitive": "Direct comparison messaging vs Xarelto on bleeding outcomes",
                },
                "channels": [
                    {"name": "Cardiology Sales Force", "budget_pct": 30, "focus": "KOL engagement, trial education"},
                    {"name": "PCP Sales Force", "budget_pct": 25, "focus": "Afib detection and treatment initiation"},
                    {"name": "DTC (TV + Digital)", "budget_pct": 25, "focus": "Patient awareness and adherence"},
                    {"name": "Medical Affairs", "budget_pct": 15, "focus": "RWE generation, guidelines"},
                    {"name": "Digital HCP", "budget_pct": 5, "focus": "Clinical tools and resources"},
                ],
                "budget": {
                    "total": 180000000,
                    "currency": "USD",
                    "breakdown": {
                        "cardiology_sf": 54000000,
                        "pcp_sf": 45000000,
                        "dtc": 45000000,
                        "medical_affairs": 27000000,
                        "digital_hcp": 9000000,
                    },
                },
                "kpis": [
                    {"metric": "Afib Market Share", "target": "42.5%", "current": "42.3%"},
                    {"metric": "VTE Market Share", "target": "28%", "current": "25.7%"},
                    {"metric": "NRx Growth", "target": "+6% YoY", "current": "baseline"},
                    {"metric": "Patient Adherence (PDC 80%)", "target": "68%", "current": "64%"},
                    {"metric": "Cardiologist Preference", "target": "1st choice 55%", "current": "52%"},
                ],
                "risks": [
                    "Xarelto competitive pressure with QD dosing message",
                    "Generic entrants in NOAC class (Pradaxa patent expiry)",
                    "Payer step-edit policies favoring lower-cost alternatives",
                    "Safety signal monitoring for all NOACs increases scrutiny",
                ],
            },
        },
    ]


def seed_database():
    """Seed the database with pharmaceutical demo data."""
    print("Starting database seeding...")

    # Clear existing data (in reverse order of dependencies)
    print("\nClearing existing data...")
    try:
        get_table("brand_plans").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        get_table("insights").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        get_table("brands").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Existing data cleared successfully")
    except Exception as e:
        print(f"Note: {e}")

    # Insert brands
    print("\nInserting brands...")
    brand_ids = {}
    for brand_data in BRANDS_DATA:
        response = get_table("brands").insert(brand_data).execute()
        brand_id = response.data[0]["id"]
        brand_name = response.data[0]["name"]
        brand_ids[brand_name] = brand_id
        print(f"  ✓ {brand_name} (ID: {brand_id})")

    # Insert insights
    print("\nInserting insights...")
    insights_data = get_insights_data(brand_ids)
    for insight in insights_data:
        response = get_table("insights").insert(insight).execute()
        print(f"  ✓ {insight['type']} for {[k for k, v in brand_ids.items() if v == insight['brand_id']][0]}")

    # Insert brand plans
    print("\nInserting brand plans...")
    plans_data = get_brand_plans_data(brand_ids)
    for plan in plans_data:
        response = get_table("brand_plans").insert(plan).execute()
        brand_name = [k for k, v in brand_ids.items() if v == plan['brand_id']][0]
        print(f"  ✓ Plan v{plan['version']} for {brand_name}")

    print("\n" + "="*60)
    print("Database seeding completed successfully!")
    print("="*60)
    print(f"\nSummary:")
    print(f"  • {len(BRANDS_DATA)} brands inserted")
    print(f"  • {len(insights_data)} insights inserted")
    print(f"  • {len(plans_data)} brand plans inserted")
    print("\nBrand IDs for reference:")
    for brand, bid in brand_ids.items():
        print(f"  • {brand}: {bid}")


if __name__ == "__main__":
    seed_database()
