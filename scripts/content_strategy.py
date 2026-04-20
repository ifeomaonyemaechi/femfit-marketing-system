# content_strategy.py
# This script reads the generated brand voice document and produces
# a full 30-day content strategy for FemFit.fit across three channels:
# Email, Instagram, and Twitter/X.
# Output is saved as a structured content calendar.

import anthropic
import os
from datetime import datetime

client = anthropic.Anthropic()


# ── Load brand voice document ────────────────────────────────────────────────

def load_brand_voice_document(outputs_folder):
    """
    Finds and loads the most recently generated brand voice document
    from the outputs folder.

    Parameters:
        outputs_folder (str): Path to the outputs folder.

    Returns:
        str: The full text of the brand voice document.
    """

    # Get a list of all files in the outputs folder.
    all_files = os.listdir(outputs_folder)

    # Filter to only files that contain "Brand_Voice_Document" in the name.
    # This makes the script find the right file automatically without
    # needing to hardcode the exact filename including the timestamp.
    brand_voice_files = [
        f for f in all_files
        if "Brand_Voice_Document" in f and f.endswith(".txt")
    ]

    # If no brand voice document is found, stop and explain why.
    if not brand_voice_files:
        print("ERROR: No brand voice document found in outputs folder.")
        print("Run brand_analyser.py first to generate the brand voice document.")
        exit()

    # Sort by filename — since filenames include timestamps,
    # sorting alphabetically gives us the most recent file last.
    # We take the last one with [-1].
    latest_file = sorted(brand_voice_files)[-1]
    filepath = os.path.join(outputs_folder, latest_file)

    print(f"✓ Loaded brand voice document: {latest_file}")

    # Open and return the full text content of the file.
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# ── Content strategy generation function ─────────────────────────────────────

def generate_content_strategy(brand_voice_text):
    """
    Sends the brand voice document to Claude and returns
    a full 30-day content strategy.

    Parameters:
        brand_voice_text (str): The full brand voice document text.

    Returns:
        str: The complete 30-day content strategy.
    """

    system_prompt = """
    You are a senior content strategist specialising in DTC eCommerce brands.
    You build content strategies that are realistic, channel-appropriate,
    and directly tied to brand voice and business goals.

    Your strategies are known for being specific and executable — not vague
    editorial calendars full of generic topic suggestions. Every content idea
    you produce could be briefed to a creator or AI system and executed immediately.

    You understand that small DTC brands need to be selective about channels
    and consistent about cadence. You never recommend doing everything —
    you recommend doing fewer things exceptionally well.
    """

    user_prompt = f"""
    Using the brand voice document below, create a complete 30-day content
    strategy for FemFit.fit.

    BRAND VOICE DOCUMENT:
    {brand_voice_text}

    PRODUCE THE FOLLOWING CONTENT STRATEGY — use these exact section headers:

    1. CHANNEL STRATEGY
    Recommend exactly 3 channels for FemFit.fit to focus on for the next
    30 days. For each channel explain:
    - Why this channel fits the brand and audience
    - What content format works best on this channel
    - Realistic posting frequency for a small DTC brand
    - One metric to track to measure success

    2. CONTENT PILLARS MAPPED TO CHANNELS
    Take the 4 content pillars from the brand voice document and map each
    one to the 3 channels. For each pillar show which channel it fits best
    and why. This gives the brand a clear system for deciding where each
    piece of content belongs.

    3. 30-DAY CONTENT CALENDAR
    Produce a week-by-week content plan for 30 days.
    Structure it as 4 weeks with 5 content pieces per week — 20 total.
    For each piece include:
    - Day and channel
    - Content pillar it belongs to
    - Format (e.g. carousel, reel, email, tweet thread)
    - Specific title or hook — not a topic, an actual headline or opening line
    - Brief notes on what the content covers

    4. CONTENT CREATION SYSTEM
    Write a simple repeatable system the brand can follow each week to
    plan, create, and publish content without burning out. Include:
    - A weekly content planning rhythm (what to do on which day)
    - A batching strategy for creating multiple pieces efficiently
    - A repurposing framework — how one piece of content becomes three

    5. FIRST WEEK EXECUTION BRIEF
    Write a detailed brief for Week 1 only — as if briefing a content
    creator or AI system to execute it. For each of the 5 Week 1 pieces,
    include the full context, key messages, tone notes, and any specific
    details needed to create the content without further clarification.

    Be specific to FemFit.fit throughout. Use the brand voice, vocabulary,
    and content pillars from the document above. Do not produce generic
    content strategy advice.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content[0].text


# ── Save function ────────────────────────────────────────────────────────────

def save_content_strategy(content):
    """
    Saves the content strategy to the outputs folder.

    Parameters:
        content (str): The content strategy text.

    Returns:
        str: The path to the saved file.
    """

    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/FemFitfit_Content_Strategy_30Day_{timestamp}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("30-DAY CONTENT STRATEGY\n")
        f.write("Brand: FemFit.fit\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write("Powered by Claude AI\n")
        f.write("=" * 60 + "\n\n")
        f.write(content)

    return filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    outputs_folder = "outputs"

    print("=" * 60)
    print("FEMFIT.FIT — CONTENT STRATEGY GENERATOR")
    print("Reading brand voice document...")
    print("=" * 60 + "\n")

    # Load the brand voice document from the outputs folder.
    brand_voice_text = load_brand_voice_document(outputs_folder)

    print("\nSending to Claude for content strategy generation...")
    print("This may take 30-40 seconds...\n")

    # Generate the content strategy.
    strategy = generate_content_strategy(brand_voice_text)

    # Save to file.
    filepath = save_content_strategy(strategy)

    # Print to terminal.
    print(strategy)

    print("\n" + "=" * 60)
    print("✓ Content strategy complete.")
    print(f"✓ Saved to: {filepath}")
    print("Run brand_voice_builder.py next to build the final client package.")
    print("=" * 60)