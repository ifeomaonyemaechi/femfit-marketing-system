# strategy_report.py
# This script reads the channel audits and competitive analysis outputs,
# combines them with the audit framework, and produces a complete
# marketing strategy report for FemFit.fit.
# This is the main client deliverable for Project 4.

import anthropic
import os
import json
from datetime import datetime
from audit_inputs import BRAND_SNAPSHOT, AUDIT_FRAMEWORK, PRIORITY_LEVELS, CHANNEL_DATA

client = anthropic.Anthropic()


# ── Load audit outputs ───────────────────────────────────────────────────────

def load_audit_outputs():
    """
    Loads the channel audits and competitive analysis from the outputs folder.

    Returns:
        tuple: (channel_audits list, competitive_analysis dict)
    """

    # Load channel audits.
    channel_path = "outputs/channel_audits.json"
    if not os.path.exists(channel_path):
        print("ERROR: channel_audits.json not found.")
        print("Run channel_auditor.py first.")
        exit()

    with open(channel_path, "r", encoding="utf-8") as f:
        channel_audits = json.load(f)

    # Load competitive analysis.
    competitive_path = "outputs/competitive_analysis.json"
    if not os.path.exists(competitive_path):
        print("ERROR: competitive_analysis.json not found.")
        print("Run competitor_analyser.py first.")
        exit()

    with open(competitive_path, "r", encoding="utf-8") as f:
        competitive_analysis = json.load(f)

    print(f"✓ Loaded {len(channel_audits)} channel audits.")
    print(f"✓ Loaded competitive analysis for {len(competitive_analysis['competitor_analyses'])} competitors.")

    return channel_audits, competitive_analysis


# ── Format audit data for report prompt ──────────────────────────────────────

def format_audit_data(channel_audits, competitive_analysis):
    """
    Formats the channel audits and competitive analysis into a
    clean text block for the strategy report prompt.

    Parameters:
        channel_audits (list): List of channel audit results.
        competitive_analysis (dict): Competitive analysis results.

    Returns:
        str: Formatted text block containing all audit findings.
    """

    sections = []

    # Format channel audit scores and key findings.
    sections.append("CHANNEL AUDIT RESULTS:")
    sections.append("─" * 40)

    for audit in channel_audits:
        score = f"{audit['score']}/10" if audit['score'] else "unscored"
        sections.append(f"\n{audit['channel'].upper()} — Score: {score}")

        # Include first 600 characters of each audit
        # to give Claude the key findings without overwhelming the prompt.
        audit_excerpt = audit["audit"][:600]
        sections.append(audit_excerpt)
        sections.append("...")

    # Format competitive summary.
    sections.append("\n" + "─" * 40)
    sections.append("COMPETITIVE ANALYSIS SUMMARY:")
    sections.append("─" * 40)
    sections.append(competitive_analysis["competitive_summary"])

    return "\n".join(sections)


# ── Overall score calculator ─────────────────────────────────────────────────

def calculate_overall_score(channel_audits):
    """
    Calculates a weighted overall marketing score from channel scores.
    Uses the weights defined in AUDIT_FRAMEWORK.

    Parameters:
        channel_audits (list): List of channel audit results with scores.

    Returns:
        tuple: (overall_score float, score_breakdown dict)
    """

    # Map channel names to their framework weights.
    # We match channel names to scoring areas by checking for keywords.
    weight_map = {
        "email": 25,
        "instagram": 10,
        "tiktok": 10,
        "website": 25,
        "sms": 5,
        "brand": 20,
        "growth": 5
    }

    total_weighted_score = 0
    total_weight = 0
    score_breakdown = {}

    for audit in channel_audits:
        if audit["score"] is None:
            continue

        channel_lower = audit["channel"].lower()

        # Find the matching weight by checking if any weight key
        # appears in the channel name.
        weight = 5  # Default weight for unmatched channels.
        for key, w in weight_map.items():
            if key in channel_lower:
                weight = w
                break

        weighted = audit["score"] * weight
        total_weighted_score += weighted
        total_weight += weight

        score_breakdown[audit["channel"]] = {
            "raw_score": audit["score"],
            "weight": weight,
            "weighted_score": round(weighted / weight_map.get("email", 25) * 10, 1)
        }

    # Calculate overall score out of 10.
    if total_weight > 0:
        overall = round((total_weighted_score / total_weight), 1)
    else:
        overall = 0

    return overall, score_breakdown


# ── Strategy report generator ────────────────────────────────────────────────

def generate_strategy_report(
    brand_snapshot,
    channel_audits,
    competitive_analysis,
    overall_score,
    formatted_audit_data
):
    """
    Sends all audit findings to Claude and returns a complete
    marketing strategy report.

    Parameters:
        brand_snapshot (dict): Brand context.
        channel_audits (list): Channel audit results.
        competitive_analysis (dict): Competitive analysis results.
        overall_score (float): Calculated overall marketing score.
        formatted_audit_data (str): Formatted text of all audit findings.

    Returns:
        str: The complete strategy report text.
    """

    # Build a channel score summary string.
    score_summary = "\n".join([
        f"  {a['channel']}: {a['score']}/10" if a['score']
        else f"  {a['channel']}: Not scored"
        for a in channel_audits
    ])

    # Format priority levels for the prompt.
    priority_text = "\n".join([
        f"  {k}: {v}" for k, v in PRIORITY_LEVELS.items()
    ])

    user_prompt = f"""
    You are a senior marketing consultant delivering a complete marketing
    audit and strategy report for {brand_snapshot['brand_name']}.

    BRAND CONTEXT:
    Brand: {brand_snapshot['brand_name']}
    Niche: {brand_snapshot['niche']}
    Platform: {brand_snapshot['platform']}
    Target customer: {brand_snapshot['target_customer']}
    Team size: {brand_snapshot['team_size']}
    Monthly revenue range: {brand_snapshot['monthly_revenue_range']}
    Audit date: {brand_snapshot['audit_date']}

    OVERALL MARKETING SCORE: {overall_score}/10

    CHANNEL SCORES:
    {score_summary}

    AUDIT FINDINGS:
    {formatted_audit_data}

    PRIORITY FRAMEWORK:
    {priority_text}

    PRODUCE A COMPLETE MARKETING STRATEGY REPORT WITH THESE EXACT SECTIONS:

    1. EXECUTIVE SUMMARY
    Three paragraphs:
    - Overall assessment of FemFit.fit's marketing health
    - The single biggest opportunity identified across all channels
    - What the brand could achieve in 90 days with the right focus

    2. MARKETING SCORECARD
    A formatted scorecard showing:
    - Overall score: {overall_score}/10
    - Individual channel scores
    - One sentence verdict per channel

    3. CRITICAL FINDINGS
    The five most important findings from the audit ranked by impact.
    For each finding:
    - Finding name
    - What the data shows
    - Why it matters for revenue
    - The cost of not addressing it

    4. 90-DAY ACTION PLAN
    A prioritised action plan using the priority framework:

    P1 — DO THIS WEEK (high impact, low effort):
    List 3 specific actions with exact instructions.

    P2 — DO THIS MONTH (high impact, moderate effort):
    List 3 specific actions with expected outcomes.

    P3 — DO THIS QUARTER (high impact, higher effort):
    List 3 strategic initiatives with success metrics.

    5. REVENUE IMPACT PROJECTIONS
    Conservative estimates of revenue impact if recommendations
    are implemented. For each major recommendation estimate:
    - Current state
    - Projected state after 90 days
    - Estimated revenue impact
    Base projections on the monthly revenue range of {brand_snapshot['monthly_revenue_range']}.

    6. COMPETITIVE POSITIONING STRATEGY
    Based on the competitive analysis, write a clear positioning
    strategy for the next 90 days. Where should FemFit.fit focus
    to build competitive advantage?

    7. QUICK REFERENCE — TOP 10 ACTIONS
    A numbered list of the 10 most important actions from the entire
    report in priority order. One line each. This is the one-page
    summary the founder pins to their wall.

    Be specific throughout. Use real numbers from the audit data.
    Do not give generic marketing advice.
    Every recommendation must be specific to FemFit.fit.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system="You are a senior marketing consultant delivering a high-value audit report. Your reports are specific, data-driven, and immediately actionable. You never give generic advice. Every finding references actual data from the audit.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Save strategy report ─────────────────────────────────────────────────────

def save_strategy_report(report, overall_score, brand_snapshot):
    """
    Saves the strategy report to the outputs folder.

    Parameters:
        report (str): The strategy report text.
        overall_score (float): The calculated overall score.
        brand_snapshot (dict): Brand context for the file header.

    Returns:
        str: Path to the saved file.
    """

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/FemFitfit_Marketing_Audit_Report_{timestamp}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("MARKETING AUDIT AND STRATEGY REPORT\n")
        f.write(f"Brand: {brand_snapshot['brand_name']}\n")
        f.write(f"Audit Date: {brand_snapshot['audit_date']}\n")
        f.write(f"Overall Score: {overall_score}/10\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write("Powered by Claude AI\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)

    return filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — STRATEGY REPORT GENERATOR")
    print("=" * 60)

    # Load audit outputs from Steps 2 and 3.
    print("\nLoading audit outputs...")
    channel_audits, competitive_analysis = load_audit_outputs()

    # Calculate overall marketing score.
    print("\nCalculating overall marketing score...")
    overall_score, score_breakdown = calculate_overall_score(channel_audits)
    print(f"✓ Overall marketing score: {overall_score}/10")

    # Format audit data for the report prompt.
    print("\nFormatting audit data...")
    formatted_audit_data = format_audit_data(
        channel_audits, competitive_analysis
    )
    print("✓ Audit data formatted.")

    # Generate the strategy report.
    print("\nGenerating strategy report...")
    print("This may take 40-60 seconds...\n")

    report = generate_strategy_report(
        BRAND_SNAPSHOT,
        channel_audits,
        competitive_analysis,
        overall_score,
        formatted_audit_data
    )

    # Save the report.
    print("Saving strategy report...")
    filepath = save_strategy_report(report, overall_score, BRAND_SNAPSHOT)

    # Print the report to terminal.
    print(report)

    print("\n" + "=" * 60)
    print("STRATEGY REPORT COMPLETE")
    print(f"✓ Overall score: {overall_score}/10")
    print(f"✓ Saved to: {os.path.basename(filepath)}")
    print("Run run_audit_pipeline.py next.")
    print("=" * 60)