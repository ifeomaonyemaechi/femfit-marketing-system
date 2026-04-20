# competitor_analyser.py
# This script analyses FemFit.fit's competitive position against
# three competitors at different scales.
# Output is a competitive intelligence report saved to outputs folder.

import anthropic
import os
import json
from datetime import datetime
from audit_inputs import BRAND_SNAPSHOT, CHANNEL_DATA, COMPETITOR_DATA

client = anthropic.Anthropic()


# ── Individual competitor analysis ───────────────────────────────────────────

def analyse_competitor(competitor, brand_snapshot, channel_data):
    """
    Sends a single competitor to Claude for comparative analysis.

    Parameters:
        competitor (dict): Competitor data from COMPETITOR_DATA.
        brand_snapshot (dict): FemFit.fit brand context.
        channel_data (dict): FemFit.fit's current channel performance.

    Returns:
        str: Competitive analysis text for this competitor.
    """

    # Format FemFit.fit's key metrics for comparison.
    femfit_metrics = f"""
    Instagram followers: {channel_data['instagram']['followers']:,}
    Email list size: {channel_data['email']['list_size']:,}
    Email open rate: {channel_data['email']['average_open_rate']}%
    Instagram engagement rate: {channel_data['instagram']['average_engagement_rate']}%
    Active email flows: 2 of 5 core flows
    Paid ads: Not active
    """

    user_prompt = f"""
    You are a senior marketing strategist conducting a competitive analysis
    for {brand_snapshot['brand_name']} — a {brand_snapshot['niche']} brand.

    FEMFIT.FIT CURRENT POSITION:
    {femfit_metrics}

    COMPETITOR BEING ANALYSED:
    Name: {competitor['name']}
    Type: {competitor['type']}
    Instagram followers: {competitor['instagram_followers']:,}
    Email strategy: {competitor['email_strategy']}
    Content strategy: {competitor['content_strategy']}
    Strengths: {competitor['strengths']}
    Weaknesses: {competitor['weaknesses']}
    Strategic relevance: {competitor['relevance']}

    PRODUCE A COMPETITIVE ANALYSIS WITH THESE SECTIONS:

    COMPETITIVE POSITION VS {competitor['name'].upper()}:
    One paragraph on where FemFit.fit stands relative to this competitor.
    Be honest — where are they behind, where do they have an advantage?

    WHAT FEMFIT.FIT CAN LEARN:
    Two specific tactics or strategies this competitor uses that
    FemFit.fit should adopt or adapt. Be specific — not "post more"
    but "adopt their content ratio of 60% lifestyle to 40% product."

    WHERE FEMFIT.FIT CAN WIN:
    Two specific areas where FemFit.fit has a genuine competitive
    advantage over this competitor that they are not currently exploiting.

    THREAT LEVEL: [Low / Medium / High]
    One sentence justifying the threat level.

    Keep the entire analysis under 300 words.
    Be specific to FemFit.fit throughout.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        system="You are a senior marketing strategist producing competitive intelligence. Your analysis is honest, specific, and actionable. You never produce generic competitive analysis.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Overall competitive summary ───────────────────────────────────────────────

def generate_competitive_summary(competitor_analyses, brand_snapshot):
    """
    Generates an overall competitive summary synthesising all three
    individual competitor analyses into strategic recommendations.

    Parameters:
        competitor_analyses (list): List of individual analysis results.
        brand_snapshot (dict): FemFit.fit brand context.

    Returns:
        str: Overall competitive summary and strategic recommendations.
    """

    # Combine all three analyses into one text block for synthesis.
    combined_analyses = "\n\n".join([
        f"VS {a['competitor']}:\n{a['analysis']}"
        for a in competitor_analyses
    ])

    user_prompt = f"""
    You have just completed competitive analyses of three competitors
    for {brand_snapshot['brand_name']}.

    Here are the three individual analyses:

    {combined_analyses}

    Now produce an OVERALL COMPETITIVE SUMMARY with these sections:

    COMPETITIVE LANDSCAPE OVERVIEW:
    Two to three sentences summarising FemFit.fit's overall competitive
    position across the three competitors analysed.

    TOP 3 COMPETITIVE OPPORTUNITIES:
    The three biggest opportunities FemFit.fit has to differentiate
    from competitors and gain market share. Each opportunity should
    be specific and actionable — not generic positioning advice.

    TOP 2 COMPETITIVE THREATS:
    The two most pressing competitive threats FemFit.fit needs to
    address in the next 90 days. Be direct about what happens if
    they do not address these threats.

    POSITIONING RECOMMENDATION:
    One clear sentence stating the single most important positioning
    move FemFit.fit should make to strengthen their competitive position.

    COMPETITIVE PRIORITY ACTIONS:
    Three specific actions ranked by priority that FemFit.fit should
    take in the next 30 days based on the competitive analysis.

    Keep the entire summary under 350 words.
    Be specific to FemFit.fit throughout.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=900,
        system="You are a senior marketing strategist synthesising competitive intelligence into clear strategic recommendations. Be direct and specific.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Save competitive analysis ─────────────────────────────────────────────────

def save_competitive_analysis(competitor_analyses, competitive_summary):
    """
    Saves the full competitive analysis to the outputs folder.

    Parameters:
        competitor_analyses (list): Individual competitor analysis results.
        competitive_summary (str): Overall competitive summary text.
    """

    os.makedirs("outputs", exist_ok=True)

    # Save JSON for pipeline use.
    json_data = {
        "competitor_analyses": competitor_analyses,
        "competitive_summary": competitive_summary
    }

    json_filepath = "outputs/competitive_analysis.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # Save readable text file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filepath = f"outputs/competitive_analysis_{timestamp}.txt"

    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("FEMFIT.FIT — COMPETITIVE ANALYSIS\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Competitors analysed: {len(competitor_analyses)}\n")
        f.write("=" * 60 + "\n")

        # Write individual competitor analyses.
        for analysis in competitor_analyses:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"COMPETITOR: {analysis['competitor'].upper()}\n")
            f.write(f"Type: {analysis['type']}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(analysis["analysis"])
            f.write(f"\n{'─' * 60}\n")

        # Write overall summary.
        f.write(f"\n{'=' * 60}\n")
        f.write("OVERALL COMPETITIVE SUMMARY\n")
        f.write(f"{'─' * 60}\n\n")
        f.write(competitive_summary)
        f.write(f"\n{'=' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — COMPETITOR ANALYSER")
    print("=" * 60)

    print(f"\nAnalysing {len(COMPETITOR_DATA)} competitors...")
    print("Each analysis takes 15-20 seconds...\n")

    competitor_analyses = []

    # Analyse each competitor individually.
    for i, competitor in enumerate(COMPETITOR_DATA, start=1):

        print(f"  Analysing competitor {i} of {len(COMPETITOR_DATA)}: {competitor['name']}...")

        analysis_text = analyse_competitor(
            competitor,
            BRAND_SNAPSHOT,
            CHANNEL_DATA
        )

        competitor_analyses.append({
            "competitor": competitor["name"],
            "type": competitor["type"],
            "instagram_followers": competitor["instagram_followers"],
            "analysis": analysis_text
        })

        print(f"  ✓ {competitor['name']} analysis complete.")

    # Generate overall competitive summary.
    print("\n  Generating overall competitive summary...")
    competitive_summary = generate_competitive_summary(
        competitor_analyses,
        BRAND_SNAPSHOT
    )
    print("  ✓ Competitive summary complete.")

    # Save all results.
    print("\nSaving competitive analysis...")
    text_filepath = save_competitive_analysis(
        competitor_analyses,
        competitive_summary
    )

    print("\n" + "=" * 60)
    print("COMPETITIVE ANALYSIS COMPLETE")
    print("─" * 40)
    print("Competitors analysed:")
    for analysis in competitor_analyses:
        print(f"  {analysis['competitor']:<25} {analysis['instagram_followers']:>10,} followers")
    print("─" * 40)
    print("Run strategy_report.py next.")
    print("=" * 60)