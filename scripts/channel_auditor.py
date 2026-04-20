# channel_auditor.py
# This script audits each of FemFit.fit's marketing channels individually.
# Each channel is sent to Claude for analysis against industry benchmarks.
# Output is a scored channel audit saved to the outputs folder.

import anthropic
import os
import json
from datetime import datetime
from audit_inputs import BRAND_SNAPSHOT, CHANNEL_DATA, AUDIT_FRAMEWORK

client = anthropic.Anthropic()


# ── Channel audit function ───────────────────────────────────────────────────

def audit_channel(channel_name, channel_data, brand_snapshot):
    """
    Sends a single channel's data to Claude for audit analysis.

    Parameters:
        channel_name (str): Name of the channel being audited.
        channel_data (dict): Performance data for this channel.
        brand_snapshot (dict): Brand context for benchmarking.

    Returns:
        dict: Audit results including score, findings, and recommendations.
    """

    # Convert the channel data dictionary to readable text for the prompt.
    # We format it as a series of key-value lines.
    channel_text = "\n".join(
        f"  {k.replace('_', ' ').title()}: {v}"
        for k, v in channel_data.items()
        if k != "notes"
    )

    # Get the notes separately so we can position them prominently.
    notes = channel_data.get("notes", "No additional notes.")

    # Get the scoring criteria for this channel from the audit framework.
    # We search for the matching area by name.
    scoring_criteria = []
    for area in AUDIT_FRAMEWORK["scoring_areas"]:
        if channel_name.lower() in area["area"].lower():
            scoring_criteria = area["criteria"]
            break

    criteria_text = "\n".join(
        f"  - {criterion}" for criterion in scoring_criteria
    ) if scoring_criteria else "  - General marketing effectiveness"

    user_prompt = f"""
    You are a senior marketing consultant conducting a channel audit
    for {brand_snapshot['brand_name']} — a {brand_snapshot['niche']} brand
    on {brand_snapshot['platform']}.

    Brand context:
    - Target customer: {brand_snapshot['target_customer']}
    - Team size: {brand_snapshot['team_size']}
    - Monthly revenue range: {brand_snapshot['monthly_revenue_range']}

    CHANNEL BEING AUDITED: {channel_name.upper()}

    CURRENT PERFORMANCE DATA:
    {channel_text}

    ANALYST NOTES:
    {notes}

    SCORING CRITERIA FOR THIS CHANNEL:
    {criteria_text}

    BENCHMARK SOURCES:
    {', '.join(AUDIT_FRAMEWORK['benchmark_sources'])}

    PRODUCE A CHANNEL AUDIT WITH THESE EXACT SECTIONS:

    CHANNEL SCORE: [X/10]
    Provide a score out of 10 with one sentence justifying it.

    PERFORMANCE SUMMARY:
    Two to three sentences on where this channel stands right now
    relative to industry benchmarks. Be specific with numbers.

    TOP 3 ISSUES:
    The three most critical problems with this channel ranked by impact.
    For each issue: name it, explain why it matters, and quantify
    the impact where possible.

    QUICK WINS (implement this week):
    Two specific actions that can be taken immediately with low effort
    and meaningful impact. Be specific — not "improve content" but
    "increase Reels to 60% of feed posts this week."

    STRATEGIC RECOMMENDATIONS (implement this quarter):
    Three recommendations that require more planning but will
    significantly move the needle on this channel.

    BENCHMARK COMPARISON:
    A brief table showing key metrics vs industry benchmark.
    Format as: Metric | FemFit.fit | Benchmark | Gap

    Keep the entire audit under 400 words.
    Be specific to {brand_snapshot['brand_name']} throughout.
    Use real numbers from the data provided.
    Do not give generic marketing advice.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system="You are a senior marketing consultant who produces specific, data-driven channel audits. You never give generic advice. Every recommendation is actionable and specific to the brand being audited.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    audit_text = response.content[0].text

    # Extract the score from the audit text.
    # We look for the pattern "X/10" in the response.
    # This is a simple extraction — in production you would use
    # structured output or JSON mode for reliability.
    score = None
    for line in audit_text.split("\n"):
        if "CHANNEL SCORE:" in line or "/10" in line:
            for word in line.split():
                if "/10" in word:
                    try:
                        # Split on "/" and take the number before it.
                        score = float(word.replace("/10", "").strip())
                    except ValueError:
                        pass
            if score:
                break

    return {
        "channel": channel_name,
        "score": score,
        "audit": audit_text
    }


# ── Save channel audits ──────────────────────────────────────────────────────

def save_channel_audits(channel_audits):
    """
    Saves all channel audit results to the outputs folder.

    Parameters:
        channel_audits (list): List of channel audit result dictionaries.
    """

    os.makedirs("outputs", exist_ok=True)

    # Save JSON for pipeline use in Step 4.
    json_filepath = "outputs/channel_audits.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(channel_audits, f, indent=2, ensure_ascii=False)

    # Save readable text file for human review.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filepath = f"outputs/channel_audits_{timestamp}.txt"

    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write(f"FEMFIT.FIT — CHANNEL AUDIT RESULTS\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Channels audited: {len(channel_audits)}\n")
        f.write("=" * 60 + "\n")

        for audit in channel_audits:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"CHANNEL: {audit['channel'].upper()}\n")
            score_display = f"{audit['score']}/10" if audit['score'] else "See audit"
            f.write(f"SCORE: {score_display}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(audit["audit"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — CHANNEL AUDITOR")
    print("=" * 60)

    # Define which channels to audit and in what order.
    # We audit the most important channels first.
    channels_to_audit = [
        ("Email", CHANNEL_DATA["email"]),
        ("Instagram", CHANNEL_DATA["instagram"]),
        ("TikTok", CHANNEL_DATA["tiktok"]),
        ("Website and Conversion", CHANNEL_DATA["website"]),
        ("SMS", CHANNEL_DATA["sms"])
    ]

    print(f"\nAuditing {len(channels_to_audit)} channels...")
    print("Each channel takes 15-20 seconds...\n")

    channel_audits = []

    for i, (channel_name, channel_data) in enumerate(channels_to_audit, start=1):

        print(f"  Auditing channel {i} of {len(channels_to_audit)}: {channel_name}...")

        audit_result = audit_channel(
            channel_name,
            channel_data,
            BRAND_SNAPSHOT
        )

        channel_audits.append(audit_result)

        score_display = f"{audit_result['score']}/10" if audit_result['score'] else "scored"
        print(f"  ✓ {channel_name} audit complete — {score_display}")

    # Save all results.
    print("\nSaving channel audit results...")
    text_filepath = save_channel_audits(channel_audits)

    # Print overall score summary.
    print("\n" + "=" * 60)
    print("CHANNEL AUDIT COMPLETE")
    print("─" * 40)
    print("SCORES:")
    for audit in channel_audits:
        score_display = f"{audit['score']}/10" if audit['score'] else "N/A"
        print(f"  {audit['channel']:<30} {score_display}")
    print("─" * 40)
    print("Run competitor_analyser.py next.")
    print("=" * 60)