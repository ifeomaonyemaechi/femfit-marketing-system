# outreach_generator.py
# This script reads qualified leads with research briefs and generates
# three personalised outreach messages per lead:
# 1. Cold email
# 2. Instagram DM
# 3. LinkedIn message
# All outputs are saved to the outputs folder.

import anthropic
import os
import json
from datetime import datetime

client = anthropic.Anthropic()


# ── Load qualified leads ─────────────────────────────────────────────────────

def load_qualified_leads(filepath):
    """
    Loads the qualified leads with research briefs from JSON.

    Parameters:
        filepath (str): Path to the qualified leads JSON file.

    Returns:
        list: List of qualified lead dictionaries with research briefs.
    """

    if not os.path.exists(filepath):
        print("ERROR: qualified_leads_with_briefs.json not found.")
        print("Run lead_researcher.py first.")
        exit()

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Outreach generator ───────────────────────────────────────────────────────

def generate_outreach_messages(lead):
    """
    Generates three outreach messages for a single lead.
    Cold email, Instagram DM, and LinkedIn message.

    Parameters:
        lead (dict): A qualified lead with research brief attached.

    Returns:
        dict: A dictionary containing all three outreach messages.
    """

    # Format pain points for the prompt.
    pain_points_text = "\n".join(
        f"- {point}" for point in lead["pain_points_observed"]
    )

    user_prompt = f"""
    You are writing outreach messages for AIMarketer.co — a Claude AI
    Co-Worker Specialist agency helping Shopify DTC brands automate
    their marketing workflows using AI.

    The person sending these messages is Ifeoma — the founder of
    AIMarketer.co. She has a background in DevOps and Klaviyo email
    marketing and now specialises in building AI-powered marketing
    systems for eCommerce brands.

    LEAD INFORMATION:
    Brand: {lead['brand_name']}
    Founder: {lead['founder_name']} ({lead['role']})
    Industry: {lead['industry']}
    Products: {lead['product_focus']}
    Instagram: {lead['instagram_handle']} ({lead['instagram_followers']:,} followers)
    Email platform: {lead['email_platform']}

    OBSERVED PAIN POINTS:
    {pain_points_text}

    RECENT ACTIVITY TO REFERENCE:
    {lead['recent_activity']}

    RESEARCH BRIEF:
    {lead['research_brief']}

    WRITE THREE OUTREACH MESSAGES:

    ─────────────────────────────────────────
    MESSAGE 1: COLD EMAIL
    ─────────────────────────────────────────
    Rules:
    - Subject line that references something specific about their brand
    - Opening line that proves you have actually looked at their brand
    - One specific observation about their marketing gap — not generic
    - A clear, low-pressure CTA — offer a free audit or 15-minute call
    - Signed from Ifeoma, AIMarketer.co
    - Maximum 150 words in the body
    - No buzzwords — no "synergy", "leverage", "game-changing"
    - Do not start with "I hope this email finds you well"
    - Do not use passive voice

    Format output as:
    SUBJECT:
    BODY:

    ─────────────────────────────────────────
    MESSAGE 2: INSTAGRAM DM
    ─────────────────────────────────────────
    Rules:
    - Under 80 words total
    - Conversational and direct — not salesy
    - Reference one specific thing about their content or recent post
    - End with one simple question — not a pitch
    - No links in the first message
    - Sound like a real person, not a template

    Format output as:
    DM:

    ─────────────────────────────────────────
    MESSAGE 3: LINKEDIN MESSAGE
    ─────────────────────────────────────────
    Rules:
    - Professional but warm — founder to founder tone
    - Reference their industry and growth stage specifically
    - Position Ifeoma's background as relevant to their situation
    - Soft CTA — invite a conversation not a sale
    - Maximum 120 words
    - No buzzwords

    Format output as:
    LINKEDIN:

    Write all three messages now. Use the lead data and research brief
    to make each message specific to {lead['brand_name']}.
    Do not write generic outreach that could apply to any brand.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1200,
        system="You are an expert at writing personalised cold outreach that converts. Your messages are specific, human, and never sound like templates.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Save outreach ────────────────────────────────────────────────────────────

def save_outreach_results(all_outreach):
    """
    Saves all outreach messages to the outputs folder.
    Saves both a JSON file (for the pipeline) and a readable text file.

    Parameters:
        all_outreach (list): List of dicts containing lead info and messages.
    """

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON for pipeline use.
    json_filepath = "outputs/outreach_messages.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_outreach, f, indent=2, ensure_ascii=False)

    # Save readable text file for human review.
    text_filepath = f"outputs/outreach_messages_{timestamp}.txt"
    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("AIMARKETER.CO — OUTREACH MESSAGES\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Total leads: {len(all_outreach)}\n")
        f.write("Messages per lead: 3 (Email, Instagram DM, LinkedIn)\n")
        f.write("=" * 60 + "\n")

        for item in all_outreach:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"LEAD: {item['brand_name']}\n")
            f.write(f"Contact: {item['founder_name']} — {item['role']}\n")
            f.write(f"Industry: {item['industry']}\n")
            f.write(f"Qualification score: {item['qualification_score']}/100\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(item["outreach_messages"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("AIMARKETER.CO — OUTREACH GENERATOR")
    print("=" * 60)

    # Load qualified leads with research briefs.
    qualified_leads = load_qualified_leads(
        "outputs/qualified_leads_with_briefs.json"
    )

    print(f"\nLoaded {len(qualified_leads)} qualified leads.")
    print("Generating 3 outreach messages per lead...\n")

    all_outreach = []

    for i, lead in enumerate(qualified_leads, start=1):

        print(f"  Lead {i} of {len(qualified_leads)}: {lead['brand_name']}...")

        messages = generate_outreach_messages(lead)

        # Build the outreach record — lead info plus the messages.
        outreach_record = {
            "id": lead["id"],
            "brand_name": lead["brand_name"],
            "founder_name": lead["founder_name"],
            "role": lead["role"],
            "industry": lead["industry"],
            "qualification_score": lead["qualification_score"],
            "outreach_messages": messages
        }

        all_outreach.append(outreach_record)
        print(f"  ✓ {lead['brand_name']} outreach complete.")

    # Save all results.
    print("\nSaving outreach messages...")
    text_filepath = save_outreach_results(all_outreach)

    print("\n" + "=" * 60)
    print("OUTREACH GENERATION COMPLETE")
    print(f"  {len(all_outreach)} leads processed")
    print(f"  {len(all_outreach) * 3} total messages generated")
    print("  Run follow_up_generator.py next.")
    print("=" * 60)