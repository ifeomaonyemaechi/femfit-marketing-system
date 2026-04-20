# caption_generator.py
# This script generates platform-optimised captions for FemFit.fit
# social media content across Instagram feed, Instagram Reels, and TikTok.
# Each caption includes hook, body, CTA, and hashtags.

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


# ── Caption generator ────────────────────────────────────────────────────────

def generate_caption(brief, platform_specs, hashtags):
    """
    Generates a platform-optimised caption for a single content brief.

    Parameters:
        brief (dict): Content brief with title, objective, key messages etc.
        platform_specs (dict): Technical requirements for this platform.
        hashtags (str): Pre-researched hashtag set for this pillar.

    Returns:
        str: The complete caption including hook, body, CTA, and hashtags.
    """

    # Format key messages as a readable list.
    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )

    # Format platform specs for the prompt.
    specs_text = "\n".join(
        f"  {k.replace('_', ' ').title()}: {v}"
        for k, v in platform_specs.items()
    )

    user_prompt = f"""
    Write a {brief['platform'].replace('_', ' ')} caption for FemFit.fit.

    CONTENT BRIEF:
    Day: {brief['day']}
    Platform: {brief['platform'].replace('_', ' ').title()}
    Content Pillar: {brief['pillar']}
    Format: {brief['format']}
    Title/Concept: {brief['title']}

    OBJECTIVE:
    {brief['objective']}

    KEY MESSAGES TO INCLUDE:
    {key_messages_text}

    CALL TO ACTION:
    {brief['cta']}

    TONE GUIDANCE:
    {brief['tone_note']}

    PLATFORM SPECIFICATIONS:
    {specs_text}

    HASHTAGS TO APPEND:
    {hashtags}

    WRITE THE CAPTION WITH THIS EXACT STRUCTURE:

    HOOK:
    [The first line — must stop the scroll. Under 10 words.
    This is the most important line. Make it earn the tap.]

    CAPTION:
    [Full caption body following the platform specs.
    Start directly after the hook with no repetition.
    Use line breaks to create breathing room.
    Build to the CTA naturally — do not force it.]

    CTA:
    [{brief['cta']} — written in FemFit.fit's voice]

    HASHTAGS:
    [Append the provided hashtag set here]

    FULL CAPTION (hook + body + cta + hashtags combined and ready to copy):
    [The complete ready-to-publish caption as one block]

    Write the caption now. Be specific to the brief.
    Do not use generic fitness captions.
    Every line should feel like it could only have been written for FemFit.fit.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Filter briefs by platform ────────────────────────────────────────────────

def get_caption_briefs(briefs):
    """
    Filters content briefs to only those that need captions.
    Carousels and video briefs are handled by separate generators.
    This generator handles feed posts, reels, and TikTok captions.

    Parameters:
        briefs (list): Full list of content briefs.

    Returns:
        list: Filtered list of briefs needing caption generation.
    """

    # We generate captions for all platforms except carousels —
    # those get their own slide-by-slide treatment in Step 3.
    caption_platforms = [
        "instagram_feed",
        "instagram_reels",
        "tiktok"
    ]

    return [b for b in briefs if b["platform"] in caption_platforms]


# ── Save captions ────────────────────────────────────────────────────────────

def save_captions(all_captions):
    """
    Saves all generated captions to the outputs folder.

    Parameters:
        all_captions (list): List of caption result dictionaries.
    """

    os.makedirs("outputs", exist_ok=True)

    # Save JSON for pipeline use.
    json_filepath = "outputs/captions.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_captions, f, indent=2, ensure_ascii=False)

    # Save readable text file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filepath = f"outputs/captions_{timestamp}.txt"

    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("FEMFIT.FIT — SOCIAL MEDIA CAPTIONS\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Captions generated: {len(all_captions)}\n")
        f.write("=" * 60 + "\n")

        for item in all_captions:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"BRIEF: {item['brief_id']}\n")
            f.write(f"Day: {item['day']}\n")
            f.write(f"Platform: {item['platform'].replace('_', ' ').title()}\n")
            f.write(f"Pillar: {item['pillar']}\n")
            f.write(f"Concept: {item['title']}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(item["caption"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — CAPTION GENERATOR")
    print("=" * 60)

    # Filter to caption-only briefs.
    caption_briefs = get_caption_briefs(CONTENT_BRIEFS)

    print(f"\nGenerating captions for {len(caption_briefs)} pieces...")
    print("Each caption takes 10-15 seconds...\n")

    all_captions = []

    for i, brief in enumerate(caption_briefs, start=1):

        print(f"  {i} of {len(caption_briefs)}: {brief['day']} — {brief['platform'].replace('_', ' ').title()}")
        print(f"    Concept: {brief['title'][:50]}...")

        # Get platform specs for this brief.
        # Use instagram_feed specs as default if platform not found.
        platform_specs = PLATFORM_SPECS.get(
            brief["platform"],
            PLATFORM_SPECS["instagram_feed"]
        )

        # Get hashtags for this pillar and platform.
        # Determine platform type for hashtag selection.
        platform_type = "tiktok" if "tiktok" in brief["platform"] else "instagram"
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get(platform_type, "")

        # Generate the caption.
        caption = generate_caption(brief, platform_specs, hashtags)

        all_captions.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "caption": caption
        })

        print(f"    ✓ Caption complete.")

    # Save all captions.
    print("\nSaving captions...")
    text_filepath = save_captions(all_captions)

    print("\n" + "=" * 60)
    print("CAPTION GENERATION COMPLETE")
    print(f"  {len(all_captions)} captions generated")
    print("  Run carousel_generator.py next.")
    print("=" * 60)