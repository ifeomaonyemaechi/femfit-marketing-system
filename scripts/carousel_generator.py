# carousel_generator.py
# This script generates complete slide-by-slide carousel scripts
# for FemFit.fit Instagram carousel posts.
# Each carousel includes slide copy, visual direction, and full caption.

import anthropic
import os
import json
from datetime import datetime
from content_inputs import (
    BRAND_VOICE,
    CONTENT_BRIEFS,
    PLATFORM_SPECS,
    HASHTAG_SETS
)

client = anthropic.Anthropic()


# ── Carousel script generator ────────────────────────────────────────────────

def generate_carousel(brief):
    """
    Generates a complete carousel script for a single carousel brief.
    Includes slide-by-slide copy, visual direction, and full caption.

    Parameters:
        brief (dict): A carousel content brief.

    Returns:
        str: The complete carousel script.
    """

    # Get carousel platform specs.
    carousel_specs = PLATFORM_SPECS["instagram_carousel"]

    # Get hashtags for this pillar.
    hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("instagram", "")

    # Format key messages.
    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )

    user_prompt = f"""
    Create a complete Instagram carousel script for FemFit.fit.

    CONTENT BRIEF:
    Day: {brief['day']}
    Pillar: {brief['pillar']}
    Format: {brief['format']}
    Title/Concept: {brief['title']}

    OBJECTIVE:
    {brief['objective']}

    KEY MESSAGES:
    {key_messages_text}

    CALL TO ACTION:
    {brief['cta']}

    TONE GUIDANCE:
    {brief['tone_note']}

    CAROUSEL SPECIFICATIONS:
    - Slides: {carousel_specs['slide_count']}
    - Slide 1: {carousel_specs['slide_1']}
    - Slides 2 to last: {carousel_specs['slide_2_to_last']}
    - Last slide: {carousel_specs['last_slide']}
    - Caption length: {carousel_specs['caption_length']}

    HASHTAGS:
    {hashtags}

    PRODUCE A COMPLETE CAROUSEL SCRIPT:

    For each slide write:

    SLIDE [number]:
    HEADLINE: [Bold text that appears on the slide — under 8 words]
    BODY COPY: [Supporting text on the slide — 1-3 sentences max]
    VISUAL DIRECTION: [One sentence describing what the designer or
    photographer should show on this slide]

    Then after all slides write:

    CAPTION:
    [Full Instagram caption for this carousel post —
    hook line, brief context, CTA, hashtags]

    DESIGN NOTES:
    [Two to three sentences of overall design guidance —
    colour, typography feel, image style]

    SPECIFIC REQUIREMENTS FOR THIS CAROUSEL:
    - Slide 1 must make someone stop scrolling and want to swipe
    - Each slide must deliver one clear point — no cramming
    - The test steps (if applicable) must be specific and actionable
    - Last slide must give them a reason to save the post
    - Write in FemFit.fit's voice throughout — direct, specific, no hype

    Write the complete carousel script now.
    Make it specific to the brief — not a generic template.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Filter carousel briefs ───────────────────────────────────────────────────

def get_carousel_briefs(briefs):
    """
    Filters content briefs to only carousel briefs.

    Parameters:
        briefs (list): Full list of content briefs.

    Returns:
        list: Filtered list of carousel briefs only.
    """

    return [b for b in briefs if b["platform"] == "instagram_carousel"]


# ── Save carousel scripts ────────────────────────────────────────────────────

def save_carousel_scripts(all_carousels):
    """
    Saves all carousel scripts to the outputs folder.

    Parameters:
        all_carousels (list): List of carousel script dictionaries.
    """

    os.makedirs("outputs", exist_ok=True)

    # Save JSON for pipeline use.
    json_filepath = "outputs/carousels.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_carousels, f, indent=2, ensure_ascii=False)

    # Save readable text file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filepath = f"outputs/carousels_{timestamp}.txt"

    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("FEMFIT.FIT — CAROUSEL SCRIPTS\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Carousels generated: {len(all_carousels)}\n")
        f.write("=" * 60 + "\n")

        for item in all_carousels:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"BRIEF: {item['brief_id']}\n")
            f.write(f"Day: {item['day']}\n")
            f.write(f"Pillar: {item['pillar']}\n")
            f.write(f"Concept: {item['title']}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(item["carousel_script"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — CAROUSEL GENERATOR")
    print("=" * 60)

    # Filter to carousel briefs only.
    carousel_briefs = get_carousel_briefs(CONTENT_BRIEFS)

    print(f"\nGenerating scripts for {len(carousel_briefs)} carousel(s)...")
    print("Each carousel takes 20-30 seconds...\n")

    all_carousels = []

    for i, brief in enumerate(carousel_briefs, start=1):

        print(f"  {i} of {len(carousel_briefs)}: {brief['day']} — {brief['title'][:50]}...")

        carousel_script = generate_carousel(brief)

        all_carousels.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "carousel_script": carousel_script
        })

        print(f"  ✓ Carousel script complete.")

    # Save all carousel scripts.
    print("\nSaving carousel scripts...")
    text_filepath = save_carousel_scripts(all_carousels)

    print("\n" + "=" * 60)
    print("CAROUSEL GENERATION COMPLETE")
    print(f"  {len(all_carousels)} carousel script(s) generated")
    print("  Run video_brief_generator.py next.")
    print("=" * 60)