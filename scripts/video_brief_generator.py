# video_brief_generator.py
# This script generates structured video production briefs
# for FemFit.fit Instagram Reels and TikTok content.
# Each brief covers hook, script, visuals, text overlays, and closing CTA.

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


# ── Video brief generator ────────────────────────────────────────────────────

def generate_video_brief(brief):
    """
    Generates a complete video production brief for a single video brief.

    Parameters:
        brief (dict): A video content brief (Reels or TikTok).

    Returns:
        str: The complete video production brief.
    """

    # Determine platform type and get relevant specs.
    if "tiktok" in brief["platform"]:
        platform_name = "TikTok"
        platform_specs = PLATFORM_SPECS["tiktok"]
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("tiktok", "")
    else:
        platform_name = "Instagram Reels"
        platform_specs = PLATFORM_SPECS["instagram_reels"]
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("instagram", "")

    # Format key messages.
    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )

    # Extract video length from format field.
    # The format field contains text like "Reel — 60 seconds".
    # We extract the number for the brief.
    video_length = "45-60 seconds"
    for word in brief["format"].split():
        if word.isdigit():
            video_length = f"{word} seconds"
            break

    user_prompt = f"""
    Create a complete video production brief for FemFit.fit.

    CONTENT BRIEF:
    Day: {brief['day']}
    Platform: {platform_name}
    Pillar: {brief['pillar']}
    Format: {brief['format']}
    Concept: {brief['title']}
    Target length: {video_length}

    OBJECTIVE:
    {brief['objective']}

    KEY MESSAGES:
    {key_messages_text}

    CALL TO ACTION:
    {brief['cta']}

    TONE:
    {brief['tone_note']}

    PLATFORM SPECS:
    Video length: {platform_specs.get('video_length', video_length)}
    Hook requirement: {platform_specs.get('hook_length', 'Strong opening')}
    CTA style: {platform_specs.get('cta_style', 'Direct and clear')}

    HASHTAGS:
    {hashtags}

    PRODUCE A COMPLETE VIDEO PRODUCTION BRIEF WITH THESE SECTIONS:

    VIDEO OVERVIEW:
    One paragraph summarising what this video is, who it is for,
    and what it needs to achieve. The creator reads this first.

    HOOK (First 3 seconds):
    What happens in the first 3 seconds — this is non-negotiable.
    Specify:
    - What is on screen
    - What is said (if anything)
    - What text overlay appears
    The hook must make the viewer stop scrolling immediately.

    SCRIPT / TALKING POINTS:
    The full talking points in order. Not word-for-word unless
    the content requires it — give the creator the key points
    and let them speak naturally.
    Format as numbered talking points.

    SHOT LIST:
    Specific shots needed to produce this video.
    Format as a numbered list. Be specific about angles,
    subjects, and what each shot shows.

    TEXT OVERLAYS:
    Any text that appears on screen during the video.
    Specify timing where relevant (e.g. "appears at 0:05").

    AUDIO DIRECTION:
    Music style or sound direction. Voiceover or talking head?
    Any specific audio notes.

    CAPTION:
    Full platform-optimised caption including hook line,
    body, CTA, and hashtags — ready to copy and paste.

    PRODUCTION NOTES:
    Any specific notes for the editor or creator.
    Keep to 2-3 bullet points maximum.

    Write the complete brief now.
    Make it specific enough that a creator can shoot this
    video without asking a single follow-up question.
    Every section should be specific to {brief['title']}.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Filter video briefs ──────────────────────────────────────────────────────

def get_video_briefs(briefs):
    """
    Filters content briefs to only video briefs — Reels and TikTok.

    Parameters:
        briefs (list): Full list of content briefs.

    Returns:
        list: Filtered list of video briefs only.
    """

    video_platforms = ["instagram_reels", "tiktok"]
    return [b for b in briefs if b["platform"] in video_platforms]


# ── Save video briefs ────────────────────────────────────────────────────────

def save_video_briefs(all_briefs):
    """
    Saves all video production briefs to the outputs folder.

    Parameters:
        all_briefs (list): List of video brief result dictionaries.
    """

    os.makedirs("outputs", exist_ok=True)

    # Save JSON for pipeline use.
    json_filepath = "outputs/video_briefs.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_briefs, f, indent=2, ensure_ascii=False)

    # Save readable text file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filepath = f"outputs/video_briefs_{timestamp}.txt"

    with open(text_filepath, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("FEMFIT.FIT — VIDEO PRODUCTION BRIEFS\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Video briefs generated: {len(all_briefs)}\n")
        f.write("=" * 60 + "\n")

        for item in all_briefs:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"BRIEF: {item['brief_id']}\n")
            f.write(f"Day: {item['day']}\n")
            f.write(f"Platform: {item['platform'].replace('_', ' ').title()}\n")
            f.write(f"Pillar: {item['pillar']}\n")
            f.write(f"Concept: {item['title']}\n")
            f.write(f"{'─' * 60}\n\n")
            f.write(item["video_brief"])
            f.write(f"\n{'─' * 60}\n")

    print(f"✓ JSON saved: {json_filepath}")
    print(f"✓ Text file saved: {text_filepath}")

    return text_filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("FEMFIT.FIT — VIDEO BRIEF GENERATOR")
    print("=" * 60)

    # Filter to video briefs only.
    video_briefs = get_video_briefs(CONTENT_BRIEFS)

    print(f"\nGenerating briefs for {len(video_briefs)} video(s)...")
    print("Each brief takes 15-20 seconds...\n")

    all_video_briefs = []

    for i, brief in enumerate(video_briefs, start=1):

        platform_label = "TikTok" if "tiktok" in brief["platform"] else "Reels"
        print(f"  {i} of {len(video_briefs)}: {brief['day']} — {platform_label}")
        print(f"    Concept: {brief['title'][:50]}...")

        video_brief = generate_video_brief(brief)

        all_video_briefs.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "video_brief": video_brief
        })

        print(f"    ✓ Video brief complete.")

    # Save all video briefs.
    print("\nSaving video briefs...")
    text_filepath = save_video_briefs(all_video_briefs)

    print("\n" + "=" * 60)
    print("VIDEO BRIEF GENERATION COMPLETE")
    print(f"  {len(all_video_briefs)} video brief(s) generated")
    print("  Run run_content_engine.py next.")
    print("=" * 60)