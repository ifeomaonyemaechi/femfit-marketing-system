# run_audit_pipeline.py
# Master runner for the FemFit.fit Marketing Audit and Strategy Report system.
# Runs the complete audit pipeline in one command:
# Stage 1: Channel audits — score and analyse each marketing channel
# Stage 2: Competitive analysis — analyse 3 competitors and synthesise
# Stage 3: Strategy report — produce prioritised recommendations
# Stage 4: Package final client deliverable

import anthropic
import os
import json
from datetime import datetime
from audit_inputs import (
    BRAND_SNAPSHOT,
    CHANNEL_DATA,
    COMPETITOR_DATA,
    AUDIT_FRAMEWORK,
    PRIORITY_LEVELS
)

client = anthropic.Anthropic()


# ── Pipeline status printer ──────────────────────────────────────────────────

def print_stage(stage_number, total_stages, stage_name):
    print(f"\n{'=' * 60}")
    print(f"STAGE {stage_number} OF {total_stages}: {stage_name.upper()}")
    print(f"{'=' * 60}")


# ── Stage 1: Channel audit functions ────────────────────────────────────────

def audit_channel(channel_name, channel_data, brand_snapshot):
    """Audits a single marketing channel against benchmarks."""

    channel_text = "\n".join(
        f"  {k.replace('_', ' ').title()}: {v}"
        for k, v in channel_data.items()
        if k != "notes"
    )
    notes = channel_data.get("notes", "No additional notes.")

    scoring_criteria = []
    for area in AUDIT_FRAMEWORK["scoring_areas"]:
        if channel_name.lower() in area["area"].lower():
            scoring_criteria = area["criteria"]
            break

    criteria_text = "\n".join(
        f"  - {criterion}" for criterion in scoring_criteria
    ) if scoring_criteria else "  - General marketing effectiveness"

    user_prompt = f"""
    You are a senior marketing consultant auditing the {channel_name} channel
    for {brand_snapshot['brand_name']} — a {brand_snapshot['niche']} brand.

    Brand context:
    - Target customer: {brand_snapshot['target_customer']}
    - Team size: {brand_snapshot['team_size']}
    - Monthly revenue: {brand_snapshot['monthly_revenue_range']}

    CHANNEL DATA:
    {channel_text}

    ANALYST NOTES:
    {notes}

    SCORING CRITERIA:
    {criteria_text}

    PRODUCE A CHANNEL AUDIT:

    CHANNEL SCORE: [X/10]
    One sentence justifying the score.

    PERFORMANCE SUMMARY:
    Two sentences on current performance vs benchmarks with specific numbers.

    TOP 3 ISSUES:
    Three critical problems ranked by impact. Name, explain, quantify.

    QUICK WINS (this week):
    Two specific immediate actions.

    STRATEGIC RECOMMENDATIONS (this quarter):
    Three recommendations with expected outcomes.

    BENCHMARK COMPARISON:
    Metric | FemFit.fit | Benchmark | Gap

    Under 400 words. Specific to {brand_snapshot['brand_name']}.
    Use real numbers from the data.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system="You are a senior marketing consultant producing specific, data-driven channel audits. Every recommendation is actionable and brand-specific.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    audit_text = response.content[0].text

    score = None
    for line in audit_text.split("\n"):
        if "CHANNEL SCORE:" in line or "/10" in line:
            for word in line.split():
                if "/10" in word:
                    try:
                        score = float(word.replace("/10", "").strip())
                    except ValueError:
                        pass
            if score:
                break

    return {"channel": channel_name, "score": score, "audit": audit_text}


# ── Stage 2: Competitor analysis functions ───────────────────────────────────

def analyse_competitor(competitor, brand_snapshot, channel_data):
    """Analyses a single competitor vs FemFit.fit."""

    femfit_metrics = f"""
    Instagram followers: {channel_data['instagram']['followers']:,}
    Email list: {channel_data['email']['list_size']:,}
    Email open rate: {channel_data['email']['average_open_rate']}%
    Engagement rate: {channel_data['instagram']['average_engagement_rate']}%
    Active flows: 2 of 5
    Paid ads: Not active
    """

    user_prompt = f"""
    Competitive analysis for {brand_snapshot['brand_name']} vs {competitor['name']}.

    FEMFIT.FIT:
    {femfit_metrics}

    COMPETITOR: {competitor['name']}
    Type: {competitor['type']}
    Instagram: {competitor['instagram_followers']:,} followers
    Email strategy: {competitor['email_strategy']}
    Content strategy: {competitor['content_strategy']}
    Strengths: {competitor['strengths']}
    Weaknesses: {competitor['weaknesses']}
    Relevance: {competitor['relevance']}

    PRODUCE:

    COMPETITIVE POSITION VS {competitor['name'].upper()}:
    One paragraph — honest assessment of where FemFit.fit stands.

    WHAT FEMFIT.FIT CAN LEARN:
    Two specific tactics to adopt or adapt.

    WHERE FEMFIT.FIT CAN WIN:
    Two specific competitive advantages not currently being exploited.

    THREAT LEVEL: [Low / Medium / High]
    One sentence justification.

    Under 300 words. Specific to FemFit.fit.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        system="You are a senior marketing strategist producing competitive intelligence. Be honest, specific, and actionable.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


def generate_competitive_summary(competitor_analyses, brand_snapshot):
    """Synthesises all competitor analyses into strategic recommendations."""

    combined = "\n\n".join([
        f"VS {a['competitor']}:\n{a['analysis']}"
        for a in competitor_analyses
    ])

    user_prompt = f"""
    Synthesise these three competitor analyses for {brand_snapshot['brand_name']}:

    {combined}

    PRODUCE:

    COMPETITIVE LANDSCAPE OVERVIEW:
    Two to three sentences on overall competitive position.

    TOP 3 COMPETITIVE OPPORTUNITIES:
    Three specific actionable opportunities to gain market share.

    TOP 2 COMPETITIVE THREATS:
    Two pressing threats and what happens if not addressed.

    POSITIONING RECOMMENDATION:
    One clear sentence on the most important positioning move.

    COMPETITIVE PRIORITY ACTIONS:
    Three specific actions for the next 30 days.

    Under 350 words. Specific to {brand_snapshot['brand_name']}.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=900,
        system="You are a senior marketing strategist synthesising competitive intelligence into clear strategic recommendations.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 3: Strategy report functions ───────────────────────────────────────

def calculate_overall_score(channel_audits):
    """Calculates weighted overall marketing score."""

    weight_map = {
        "email": 25, "instagram": 10, "tiktok": 10,
        "website": 25, "sms": 5, "brand": 20, "growth": 5
    }

    total_weighted = 0
    total_weight = 0

    for audit in channel_audits:
        if audit["score"] is None:
            continue
        channel_lower = audit["channel"].lower()
        weight = 5
        for key, w in weight_map.items():
            if key in channel_lower:
                weight = w
                break
        total_weighted += audit["score"] * weight
        total_weight += weight

    overall = round(total_weighted / total_weight, 1) if total_weight > 0 else 0
    return overall


def generate_strategy_report(
    brand_snapshot, channel_audits,
    competitive_summary, overall_score
):
    """Generates the complete strategy report."""

    score_summary = "\n".join([
        f"  {a['channel']}: {a['score']}/10"
        if a['score'] else f"  {a['channel']}: Not active"
        for a in channel_audits
    ])

    audit_excerpts = "\n\n".join([
        f"{a['channel'].upper()} ({a['score']}/10):\n{a['audit'][:500]}..."
        for a in channel_audits
    ])

    priority_text = "\n".join([
        f"  {k}: {v}" for k, v in PRIORITY_LEVELS.items()
    ])

    user_prompt = f"""
    You are a senior marketing consultant delivering a complete audit report
    for {brand_snapshot['brand_name']}.

    BRAND: {brand_snapshot['brand_name']}
    Niche: {brand_snapshot['niche']}
    Team: {brand_snapshot['team_size']}
    Revenue: {brand_snapshot['monthly_revenue_range']}
    Audit date: {brand_snapshot['audit_date']}

    OVERALL SCORE: {overall_score}/10

    CHANNEL SCORES:
    {score_summary}

    CHANNEL AUDIT EXCERPTS:
    {audit_excerpts}

    COMPETITIVE SUMMARY:
    {competitive_summary}

    PRIORITY FRAMEWORK:
    {priority_text}

    PRODUCE A COMPLETE MARKETING STRATEGY REPORT:

    1. EXECUTIVE SUMMARY
    Three paragraphs:
    - Overall marketing health assessment
    - Single biggest opportunity across all channels
    - What the brand can achieve in 90 days with right focus

    2. MARKETING SCORECARD
    Overall score: {overall_score}/10
    Channel scores with one sentence verdict each.

    3. CRITICAL FINDINGS
    Five most important findings ranked by revenue impact.
    For each: finding name, data evidence, revenue impact,
    cost of inaction.

    4. 90-DAY ACTION PLAN
    P1 — THIS WEEK: 3 specific actions with exact instructions
    P2 — THIS MONTH: 3 actions with expected outcomes
    P3 — THIS QUARTER: 3 initiatives with success metrics

    5. REVENUE IMPACT PROJECTIONS
    For each major recommendation:
    Current state | Projected state | Revenue impact
    Base on monthly revenue of {brand_snapshot['monthly_revenue_range']}.

    6. COMPETITIVE POSITIONING STRATEGY
    Clear 90-day positioning strategy based on competitive analysis.

    7. TOP 10 ACTIONS — QUICK REFERENCE
    Ten most important actions in priority order.
    One line each. The founder's wall list.

    Specific throughout. Real numbers. No generic advice.
    Every recommendation specific to {brand_snapshot['brand_name']}.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system="You are a senior marketing consultant delivering a high-value audit report. Specific, data-driven, immediately actionable. No generic advice.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 4: Package final deliverable ───────────────────────────────────────

def package_deliverable(
    brand_snapshot, channel_audits,
    competitor_analyses, competitive_summary,
    strategy_report, overall_score, duration
):
    """
    Assembles all audit outputs into one complete client deliverable.

    Parameters:
        brand_snapshot (dict): Brand context.
        channel_audits (list): All channel audit results.
        competitor_analyses (list): Individual competitor analyses.
        competitive_summary (str): Overall competitive summary.
        strategy_report (str): The full strategy report.
        overall_score (float): Overall marketing score.
        duration (int): Pipeline duration in seconds.

    Returns:
        str: Path to the saved deliverable file.
    """

    today = datetime.now().strftime("%d %B %Y")

    sections = [
        "=" * 60,
        "FEMFIT.FIT",
        "MARKETING AUDIT AND STRATEGY REPORT",
        f"Audit Date: {brand_snapshot['audit_date']}",
        f"Prepared: {today}",
        f"Overall Marketing Score: {overall_score}/10",
        "Powered by Claude AI | Delivered by Ifeoma Onyemaechi",
        "=" * 60,
        "",
        "DOCUMENT CONTENTS",
        "─" * 40,
        "Section 1: Marketing Strategy Report",
        "Section 2: Channel Audit Details",
        "Section 3: Competitive Analysis",
        "Section 4: Audit Methodology",
        "",
        "=" * 60,
        "",
        "SECTION 1: MARKETING STRATEGY REPORT",
        "─" * 40,
        "",
        strategy_report,
        "",
        "=" * 60,
        "",
        "SECTION 2: CHANNEL AUDIT DETAILS",
        "─" * 40,
        ""
    ]

    # Add individual channel audits.
    for audit in channel_audits:
        score_display = f"{audit['score']}/10" if audit['score'] else "N/A"
        sections.append(f"\n{'─' * 40}")
        sections.append(f"CHANNEL: {audit['channel'].upper()} — {score_display}")
        sections.append(f"{'─' * 40}")
        sections.append(audit["audit"])

    sections += [
        "",
        "=" * 60,
        "",
        "SECTION 3: COMPETITIVE ANALYSIS",
        "─" * 40,
        ""
    ]

    # Add individual competitor analyses.
    for analysis in competitor_analyses:
        sections.append(f"\n{'─' * 40}")
        sections.append(f"VS {analysis['competitor'].upper()}")
        sections.append(f"{'─' * 40}")
        sections.append(analysis["analysis"])

    sections += [
        "",
        "OVERALL COMPETITIVE SUMMARY",
        "─" * 40,
        "",
        competitive_summary,
        "",
        "=" * 60,
        "",
        "SECTION 4: AUDIT METHODOLOGY",
        "─" * 40,
        "",
        "CHANNELS AUDITED:",
        "  Email (Klaviyo), Instagram, TikTok, Website, SMS",
        "",
        "COMPETITORS ANALYSED:",
        "  Gymshark (enterprise benchmark)",
        "  Tala (direct competitor)",
        "  Adapt Clothing (emerging competitor)",
        "",
        "SCORING FRAMEWORK:",
        "  Email Marketing: 25% weight",
        "  Website and Conversion: 25% weight",
        "  Social Media: 20% weight",
        "  Brand and Content: 20% weight",
        "  Growth and Acquisition: 10% weight",
        "",
        "BENCHMARK SOURCES:",
    ]

    for source in AUDIT_FRAMEWORK["benchmark_sources"]:
        sections.append(f"  - {source}")

    sections += [
        "",
        "=" * 60,
        f"Audit completed: {today}",
        f"Pipeline duration: {duration} seconds",
        "Generated using Claude AI by Ifeoma Onyemaechi",
        "Claude AI Co-Worker Specialist | Marketing Automation",
        "=" * 60
    ]

    document = "\n".join(sections)

    # Save the complete deliverable.
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/FEMFIT_MARKETING_AUDIT_COMPLETE_{timestamp}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(document)

    return filepath


# ── Main pipeline ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)
    pipeline_start = datetime.now()

    print("\n" + "=" * 60)
    print("FEMFIT.FIT — MARKETING AUDIT PIPELINE")
    print("Running complete audit and strategy report system.")
    print(f"Started: {pipeline_start.strftime('%d %B %Y, %H:%M:%S')}")
    print("=" * 60)

    # ── Stage 1: Channel audits ──────────────────────────────────────
    print_stage(1, 4, "Auditing marketing channels")

    channels_to_audit = [
        ("Email", CHANNEL_DATA["email"]),
        ("Instagram", CHANNEL_DATA["instagram"]),
        ("TikTok", CHANNEL_DATA["tiktok"]),
        ("Website and Conversion", CHANNEL_DATA["website"]),
        ("SMS", CHANNEL_DATA["sms"])
    ]

    channel_audits = []
    for i, (channel_name, channel_data) in enumerate(channels_to_audit, start=1):
        print(f"  Auditing {i} of {len(channels_to_audit)}: {channel_name}...")
        result = audit_channel(channel_name, channel_data, BRAND_SNAPSHOT)
        channel_audits.append(result)
        score_display = f"{result['score']}/10" if result['score'] else "scored"
        print(f"  ✓ {channel_name} — {score_display}")

    # Save channel audits.
    with open("outputs/channel_audits.json", "w", encoding="utf-8") as f:
        json.dump(channel_audits, f, indent=2, ensure_ascii=False)
    print(f"\n✓ {len(channel_audits)} channel audits saved.")

    # ── Stage 2: Competitive analysis ───────────────────────────────
    print_stage(2, 4, "Analysing competitors")

    competitor_analyses = []
    for i, competitor in enumerate(COMPETITOR_DATA, start=1):
        print(f"  Analysing {i} of {len(COMPETITOR_DATA)}: {competitor['name']}...")
        analysis = analyse_competitor(competitor, BRAND_SNAPSHOT, CHANNEL_DATA)
        competitor_analyses.append({
            "competitor": competitor["name"],
            "type": competitor["type"],
            "analysis": analysis
        })
        print(f"  ✓ {competitor['name']} complete.")

    print("\n  Generating competitive summary...")
    competitive_summary = generate_competitive_summary(
        competitor_analyses, BRAND_SNAPSHOT
    )
    print("  ✓ Competitive summary complete.")

    # Save competitive analysis.
    with open("outputs/competitive_analysis.json", "w", encoding="utf-8") as f:
        json.dump({
            "competitor_analyses": competitor_analyses,
            "competitive_summary": competitive_summary
        }, f, indent=2, ensure_ascii=False)
    print(f"✓ Competitive analysis saved.")

    # ── Stage 3: Strategy report ─────────────────────────────────────
    print_stage(3, 4, "Generating strategy report")

    overall_score = calculate_overall_score(channel_audits)
    print(f"  Overall marketing score: {overall_score}/10")
    print("  Generating report — this may take 40-60 seconds...")

    strategy_report = generate_strategy_report(
        BRAND_SNAPSHOT,
        channel_audits,
        competitive_summary,
        overall_score
    )
    print("  ✓ Strategy report complete.")

    # ── Stage 4: Package deliverable ────────────────────────────────
    print_stage(4, 4, "Packaging complete client deliverable")

    pipeline_end = datetime.now()
    duration = (pipeline_end - pipeline_start).seconds

    filepath = package_deliverable(
        BRAND_SNAPSHOT,
        channel_audits,
        competitor_analyses,
        competitive_summary,
        strategy_report,
        overall_score,
        duration
    )

    print(f"✓ Complete audit package saved.")
    print(f"  File: {os.path.basename(filepath)}")

    # ── Pipeline summary ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("AUDIT PIPELINE COMPLETE")
    print("─" * 40)
    print(f"Channels audited:        {len(channel_audits)}")
    print(f"Competitors analysed:    {len(competitor_analyses)}")
    print(f"Overall score:           {overall_score}/10")
    print(f"Pipeline duration:       {duration} seconds")
    print(f"Output file:             {os.path.basename(filepath)}")
    print("=" * 60)
    print("\nProject 4 complete. Your audit report is ready.")