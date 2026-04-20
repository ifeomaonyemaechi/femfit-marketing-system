# follow_up_generator.py
# This script reads the outreach messages JSON and generates
# a 3-touch follow-up sequence for each lead.
# Each touch uses a different psychological strategy.
# Output is saved to the outputs folder.

import anthropic
import os
import json
from datetime import datetime

client = anthropic.Anthropic()


# ── Load outreach data ───────────────────────────────────────────────────────

def load_outreach_data(filepath):
    """
    Loads the outreach messages from the JSON file saved in Step 3.

    Parameters:
        filepath (str): Path to the outreach messages JSON file.

    Returns:
        list: List of outreach records with lead info and messages.
    """

    if not os.path.exists(filepath):
        print("ERROR: outreach_messages.json not found.")
        print("Run outreach_generator.py first.")
        exit()

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Follow-up sequence definitions ──────────────────────────────────────────
# Three follow-up touches with different strategies.
# These are passed to Claude as context for each message.

FOLLOWUP_SEQUENCE = [
    {
        "touch_number": 1,
        "timing": "Day 4 after initial outreach — no response received",
        "strategy": "Value add",
        "objective": "Re-open the conversation by giving something useful — a specific insight, observation, or idea relevant to their brand. Do not repeat the pitch. Lead with value, mention the service only briefly at the end.",
        "tone": "Helpful and generous. Like a peer sharing something useful, not a salesperson following up.",
        "length": "Under 100 words for email. Under 60 words for DM."
    },
    {
        "touch_number": 2,
        "timing": "Day 8 after initial outreach — still no response",
        "strategy": "Timely relevance",
        "objective": "Reference something current — a season, a trend in their industry, or a business moment that makes the timing feel relevant right now. Create soft urgency without pressure. Make them feel like now is a natural moment to have this conversation.",
        "tone": "Informed and timely. Shows you are paying attention to their industry and their brand specifically.",
        "length": "Under 100 words for email. Under 60 words for DM."
    },
    {
        "touch_number": 3,
        "timing": "Day 14 after initial outreach — final follow-up",
        "strategy": "Clean close",
        "objective": "Give them an easy out while leaving the door open. Be honest that this is the last follow-up. Make it clear there are no hard feelings if it is not the right time. Leave them with one final specific reason to respond. The goal is to close the loop cleanly — not to pressure.",
        "tone": "Calm, direct, and respectful. Confident enough to walk away. This email should feel like the opposite of desperation.",
        "length": "Under 80 words for email. Under 50 words for DM."
    }
]


# ── Follow-up generator ──────────────────────────────────────────────────────

def generate_followup_sequence(outreach_record):
    """
    Generates a 3-touch follow-up sequence for a single lead.

    Parameters:
        outreach_record (dict): A lead's outreach record including
                                their info and initial messages.

    Returns:
        str: The full 3-touch follow-up sequence as formatted text.
    """

    # Format the follow-up sequence instructions for the prompt.
    sequence_text = ""
    for touch in FOLLOWUP_SEQUENCE:
        sequence_text += f"""
    TOUCH {touch['touch_number']}: {touch['strategy'].upper()}
    Timing: {touch['timing']}
    Objective: {touch['objective']}
    Tone: {touch['tone']}
    Length: {touch['length']}
    """

    user_prompt = f"""
    You are writing follow-up messages for AIMarketer.co — a Claude AI
    Co-Worker Specialist agency helping Shopify DTC brands automate
    their marketing workflows using AI.

    The sender is Ifeoma, founder of AIMarketer.co.
    She sent initial outreach to this lead and received no response.
    She is now sending a 3-touch follow-up sequence via email.

    LEAD INFORMATION:
    Brand: {outreach_record['brand_name']}
    Contact: {outreach_record['founder_name']} — {outreach_record['role']}
    Industry: {outreach_record['industry']}
    Qualification score: {outreach_record['qualification_score']}/100

    INITIAL OUTREACH SENT:
    {outreach_record['outreach_messages'][:800]}

    WRITE A 3-TOUCH FOLLOW-UP EMAIL SEQUENCE:
    {sequence_text}

    RULES FOR ALL THREE MESSAGES:
    - Each message must feel different from the previous one
    - Never repeat the same hook or opening line
    - Reference the brand specifically in each message
    - Do not apologise for following up
    - Do not say "just checking in" or "circling back"
    - Do not use passive voice
    - Each email needs a subject line and body
    - Sign each email from Ifeoma, AIMarketer.co

    FORMAT EACH TOUCH EXACTLY LIKE THIS:

    ══════════════════════════════════════
    FOLLOW-UP TOUCH [number]: [strategy name]
    Timing: [when to send]
    ══════════════════════════════════════
    SUBJECT: [subject line]
    BODY:
    [email body]
    ──────────────────────────────────────

    Write all three follow-up touches now.
    Make each one specific to {outreach_record['brand_name']}.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system="You are an expert at writing follow-up sequences that feel human, respectful, and specific. Your follow-ups never sound like templates.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Save follow-up results ───────────────────────────────────────────────────

def save_followup_results(all_followups):
    """
    Saves all follow-up sequences to the outputs folder.

    Parameters:
        all_followups (list): List of dicts with lead info and follow-up sequences.
    """

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON for pipeline use.
    json_filepath = "outputs/followup_sequences.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_followups, f, indent=2, ensure_ascii=False)

    # Save readable text file for human review.
    text_filepath = f"outputs/followup_sequences_{timestamp}.txt"
    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("AIMARKETER.CO — FOLLOW-UP SEQUENCES\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Total leads: {len(all_followups)}\n")
        f.write("Touches per lead: 3\n")
        f.write(f"Total emails: {len(all_followups) * 3}\n")
        f.write("=" * 60 + "\n")

        for item in all_followups:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"LEAD: {item['brand_name']}\n")
            f.write(f"Contact: {item['founder_name']} — {item['role']}\n")
            f.write(f"Industry: {item['industry']}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(item["followup_sequence"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("AIMARKETER.CO — FOLLOW-UP GENERATOR")
    print("=" * 60)

    # Load outreach data from Step 3.
    outreach_data = load_outreach_data("outputs/outreach_messages.json")

    print(f"\nLoaded {len(outreach_data)} leads.")
    print("Generating 3-touch follow-up sequence per lead...")
    print("Each sequence takes 15-20 seconds...\n")

    all_followups = []

    for i, record in enumerate(outreach_data, start=1):

        print(f"  Lead {i} of {len(outreach_data)}: {record['brand_name']}...")

        followup = generate_followup_sequence(record)

        followup_record = {
            "id": record["id"],
            "brand_name": record["brand_name"],
            "founder_name": record["founder_name"],
            "role": record["role"],
            "industry": record["industry"],
            "qualification_score": record["qualification_score"],
            "followup_sequence": followup
        }

        all_followups.append(followup_record)
        print(f"  ✓ {record['brand_name']} follow-up sequence complete.")

    # Save all results.
    print("\nSaving follow-up sequences...")
    text_filepath = save_followup_results(all_followups)

    print("\n" + "=" * 60)
    print("FOLLOW-UP GENERATION COMPLETE")
    print(f"  {len(all_followups)} leads processed")
    print(f"  {len(all_followups) * 3} follow-up emails generated")
    print("  Run run_outreach_pipeline.py next.")
    print("=" * 60)