# run_content_engine.py
# Master runner for the FemFit.fit Social Media Content Engine.
# Produces a complete week of content in one command:
# Stage 1: Generate captions for feed posts, Reels, and TikTok
# Stage 2: Generate carousel scripts slide by slide
# Stage 3: Generate video production briefs
# Stage 4: Package complete weekly content pack

import anthropic
import os
import json
from datetime import datetime
from content_inputs import (
    BRAND_VOICE,
    CONTENT_BRIEFS,
    CONTENT_PILLARS,
    PLATFORM_SPECS,
    HASHTAG_SETS
)

client = anthropic.Anthropic()


# ── Pipeline status printer ──────────────────────────────────────────────────

def print_stage(stage_number, total_stages, stage_name):
    print(f"\n{'=' * 60}")
    print(f"STAGE {stage_number} OF {total_stages}: {stage_name.upper()}")
    print(f"{'=' * 60}")


# ── Stage 1: Caption generation ──────────────────────────────────────────────

def generate_caption(brief, platform_specs, hashtags):
    """Generates a platform-optimised caption for a content brief."""

    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )
    specs_text = "\n".join(
        f"  {k.replace('_', ' ').title()}: {v}"
        for k, v in platform_specs.items()
    )

    user_prompt = f"""
    Write a {brief['platform'].replace('_', ' ')} caption for FemFit.fit.

    BRIEF:
    Day: {brief['day']}
    Platform: {brief['platform'].replace('_', ' ').title()}
    Pillar: {brief['pillar']}
    Concept: {brief['title']}

    OBJECTIVE: {brief['objective']}

    KEY MESSAGES:
    {key_messages_text}

    CTA: {brief['cta']}
    TONE: {brief['tone_note']}

    PLATFORM SPECS:
    {specs_text}

    HASHTAGS: {hashtags}

    WRITE WITH THIS STRUCTURE:

    HOOK:
    [First line — under 10 words — must stop the scroll]

    CAPTION:
    [Full body — platform-appropriate length]

    CTA:
    [In FemFit.fit voice]

    HASHTAGS:
    [Append provided hashtags]

    FULL CAPTION (ready to copy):
    [Complete caption as one block]
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 2: Carousel generation ────────────────────────────────────────────

def generate_carousel(brief):
    """Generates a complete slide-by-slide carousel script."""

    carousel_specs = PLATFORM_SPECS["instagram_carousel"]
    hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("instagram", "")
    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )

    user_prompt = f"""
    Create a complete Instagram carousel script for FemFit.fit.

    BRIEF:
    Day: {brief['day']}
    Pillar: {brief['pillar']}
    Concept: {brief['title']}

    OBJECTIVE: {brief['objective']}

    KEY MESSAGES:
    {key_messages_text}

    CTA: {brief['cta']}
    TONE: {brief['tone_note']}

    SPECS:
    Slides: {carousel_specs['slide_count']}
    Slide 1: {carousel_specs['slide_1']}
    Middle slides: {carousel_specs['slide_2_to_last']}
    Last slide: {carousel_specs['last_slide']}

    HASHTAGS: {hashtags}

    FOR EACH SLIDE WRITE:
    SLIDE [number]:
    HEADLINE: [Under 8 words]
    BODY COPY: [1-3 sentences]
    VISUAL DIRECTION: [One sentence for designer]

    THEN WRITE:
    CAPTION: [Full Instagram caption with hook, body, CTA, hashtags]
    DESIGN NOTES: [2-3 sentences on overall look and feel]
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 3: Video brief generation ─────────────────────────────────────────

def generate_video_brief(brief):
    """Generates a complete video production brief."""

    if "tiktok" in brief["platform"]:
        platform_name = "TikTok"
        platform_specs = PLATFORM_SPECS["tiktok"]
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("tiktok", "")
    else:
        platform_name = "Instagram Reels"
        platform_specs = PLATFORM_SPECS["instagram_reels"]
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get("instagram", "")

    key_messages_text = "\n".join(
        f"  - {msg}" for msg in brief["key_messages"]
    )

    video_length = "45-60 seconds"
    for word in brief["format"].split():
        if word.isdigit():
            video_length = f"{word} seconds"
            break

    user_prompt = f"""
    Create a complete video production brief for FemFit.fit.

    BRIEF:
    Day: {brief['day']}
    Platform: {platform_name}
    Pillar: {brief['pillar']}
    Concept: {brief['title']}
    Length: {video_length}

    OBJECTIVE: {brief['objective']}

    KEY MESSAGES:
    {key_messages_text}

    CTA: {brief['cta']}
    TONE: {brief['tone_note']}

    PLATFORM:
    Hook: {platform_specs.get('hook_length', 'Strong opening')}
    CTA style: {platform_specs.get('cta_style', 'Direct')}

    HASHTAGS: {hashtags}

    PRODUCE:

    VIDEO OVERVIEW:
    One paragraph — what this video is and what it needs to achieve.

    HOOK (First 3 seconds):
    What is on screen, what is said, what text overlay appears.

    SCRIPT / TALKING POINTS:
    Numbered talking points in order.

    SHOT LIST:
    Numbered list of specific shots needed.

    TEXT OVERLAYS:
    On-screen text with timing notes.

    AUDIO DIRECTION:
    Music style, voiceover or talking head, audio notes.

    CAPTION:
    Full platform caption with hook, body, CTA, hashtags.

    PRODUCTION NOTES:
    2-3 bullet points for editor or creator.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system=BRAND_VOICE,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 4: Package content pack ───────────────────────────────────────────

def package_content_pack(
    all_captions, all_carousels,
    all_video_briefs, duration
):
    """
    Assembles all content into one complete weekly content pack.

    Parameters:
        all_captions (list): Generated captions.
        all_carousels (list): Generated carousel scripts.
        all_video_briefs (list): Generated video briefs.
        duration (int): Pipeline duration in seconds.

    Returns:
        str: Path to the saved content pack file.
    """

    today = datetime.now().strftime("%d %B %Y")

    # Count total pieces by type.
    total_pieces = len(all_captions) + len(all_carousels) + len(all_video_briefs)

    sections = [
        "=" * 60,
        "FEMFIT.FIT",
        "WEEKLY SOCIAL MEDIA CONTENT PACK",
        f"Week of: {today}",
        "Powered by Claude AI | Delivered by Ifeoma Onyemaechi",
        "=" * 60,
        "",
        "CONTENT SUMMARY",
        "─" * 40,
        f"Total pieces:      {total_pieces}",
        f"Captions:          {len(all_captions)} (Instagram feed, Reels, TikTok)",
        f"Carousel scripts:  {len(all_carousels)} (Instagram carousel)",
        f"Video briefs:      {len(all_video_briefs)} (Reels and TikTok)",
        f"Generated in:      {duration} seconds",
        "",
        "WEEKLY SCHEDULE",
        "─" * 40,
    ]

    # Build the weekly schedule from all briefs.
    all_content = []
    for c in all_captions:
        all_content.append({
            "day": c["day"],
            "platform": c["platform"],
            "title": c["title"],
            "type": "Caption"
        })
    for c in all_carousels:
        all_content.append({
            "day": c["day"],
            "platform": c["platform"],
            "title": c["title"],
            "type": "Carousel Script"
        })
    for v in all_video_briefs:
        all_content.append({
            "day": v["day"],
            "platform": v["platform"],
            "title": v["title"],
            "type": "Video Brief"
        })

    # Sort by day of week.
    day_order = {
        "Monday": 1, "Tuesday": 2, "Wednesday": 3,
        "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7
    }
    all_content.sort(key=lambda x: day_order.get(x["day"], 8))

    for item in all_content:
        platform_label = item["platform"].replace("_", " ").title()
        sections.append(
            f"  {item['day']:<12} {platform_label:<25} {item['type']}"
        )

    sections += [
        "",
        "=" * 60,
        "",
        "SECTION 1: CAPTIONS",
        "─" * 40,
        ""
    ]

    for item in all_captions:
        sections.append(f"\n{'─' * 40}")
        sections.append(
            f"{item['day'].upper()} — "
            f"{item['platform'].replace('_', ' ').title()}"
        )
        sections.append(f"Concept: {item['title']}")
        sections.append(f"Pillar: {item['pillar']}")
        sections.append(f"{'─' * 40}\n")
        sections.append(item["caption"])

    sections += [
        "",
        "=" * 60,
        "",
        "SECTION 2: CAROUSEL SCRIPTS",
        "─" * 40,
        ""
    ]

    for item in all_carousels:
        sections.append(f"\n{'─' * 40}")
        sections.append(f"{item['day'].upper()} — INSTAGRAM CAROUSEL")
        sections.append(f"Concept: {item['title']}")
        sections.append(f"Pillar: {item['pillar']}")
        sections.append(f"{'─' * 40}\n")
        sections.append(item["carousel_script"])

    sections += [
        "",
        "=" * 60,
        "",
        "SECTION 3: VIDEO PRODUCTION BRIEFS",
        "─" * 40,
        ""
    ]

    for item in all_video_briefs:
        platform_label = item["platform"].replace("_", " ").title()
        sections.append(f"\n{'─' * 40}")
        sections.append(f"{item['day'].upper()} — {platform_label.upper()}")
        sections.append(f"Concept: {item['title']}")
        sections.append(f"Pillar: {item['pillar']}")
        sections.append(f"{'─' * 40}\n")
        sections.append(item["video_brief"])

    sections += [
        "",
        "=" * 60,
        "CONTENT PACK COMPLETE",
        f"Generated: {today}",
        f"Pipeline duration: {duration} seconds",
        "Generated using Claude AI by Ifeoma Onyemaechi",
        "Claude AI Co-Worker Specialist | Marketing Automation",
        "=" * 60
    ]

    document = "\n".join(sections)

    # Save the content pack.
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/FEMFIT_WEEKLY_CONTENT_PACK_{timestamp}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(document)

    return filepath


# ── Main pipeline ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)
    pipeline_start = datetime.now()

    print("\n" + "=" * 60)
    print("FEMFIT.FIT — SOCIAL MEDIA CONTENT ENGINE")
    print("Generating one complete week of content.")
    print(f"Started: {pipeline_start.strftime('%d %B %Y, %H:%M:%S')}")
    print("=" * 60)

    # ── Stage 1: Captions ────────────────────────────────────────────
    print_stage(1, 4, "Generating captions")

    caption_platforms = ["instagram_feed", "instagram_reels", "tiktok"]
    caption_briefs = [
        b for b in CONTENT_BRIEFS
        if b["platform"] in caption_platforms
    ]

    all_captions = []
    for i, brief in enumerate(caption_briefs, start=1):
        platform_label = brief["platform"].replace("_", " ").title()
        print(f"  {i} of {len(caption_briefs)}: {brief['day']} — {platform_label}")

        platform_specs = PLATFORM_SPECS.get(
            brief["platform"], PLATFORM_SPECS["instagram_feed"]
        )
        platform_type = "tiktok" if "tiktok" in brief["platform"] else "instagram"
        hashtags = HASHTAG_SETS.get(brief["pillar"], {}).get(platform_type, "")

        caption = generate_caption(brief, platform_specs, hashtags)
        all_captions.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "caption": caption
        })
        print(f"  ✓ Done.")

    print(f"\n✓ {len(all_captions)} captions generated.")

    # ── Stage 2: Carousels ───────────────────────────────────────────
    print_stage(2, 4, "Generating carousel scripts")

    carousel_briefs = [
        b for b in CONTENT_BRIEFS
        if b["platform"] == "instagram_carousel"
    ]

    all_carousels = []
    for i, brief in enumerate(carousel_briefs, start=1):
        print(f"  {i} of {len(carousel_briefs)}: {brief['day']} — {brief['title'][:40]}...")
        carousel_script = generate_carousel(brief)
        all_carousels.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "carousel_script": carousel_script
        })
        print(f"  ✓ Done.")

    print(f"\n✓ {len(all_carousels)} carousel script(s) generated.")

    # ── Stage 3: Video briefs ────────────────────────────────────────
    print_stage(3, 4, "Generating video production briefs")

    video_platforms = ["instagram_reels", "tiktok"]
    video_brief_list = [
        b for b in CONTENT_BRIEFS
        if b["platform"] in video_platforms
    ]

    all_video_briefs = []
    for i, brief in enumerate(video_brief_list, start=1):
        platform_label = "TikTok" if "tiktok" in brief["platform"] else "Reels"
        print(f"  {i} of {len(video_brief_list)}: {brief['day']} — {platform_label}")
        video_brief = generate_video_brief(brief)
        all_video_briefs.append({
            "brief_id": brief["brief_id"],
            "day": brief["day"],
            "platform": brief["platform"],
            "pillar": brief["pillar"],
            "title": brief["title"],
            "video_brief": video_brief
        })
        print(f"  ✓ Done.")

    print(f"\n✓ {len(all_video_briefs)} video brief(s) generated.")

    # ── Stage 4: Package content pack ───────────────────────────────
    print_stage(4, 4, "Packaging weekly content pack")

    pipeline_end = datetime.now()
    duration = (pipeline_end - pipeline_start).seconds

    filepath = package_content_pack(
        all_captions,
        all_carousels,
        all_video_briefs,
        duration
    )

    print(f"✓ Content pack saved: {os.path.basename(filepath)}")

    # ── Pipeline summary ─────────────────────────────────────────────
    total_pieces = (
        len(all_captions) + len(all_carousels) + len(all_video_briefs)
    )

    print("\n" + "=" * 60)
    print("CONTENT ENGINE COMPLETE")
    print("─" * 40)
    print(f"Captions generated:      {len(all_captions)}")
    print(f"Carousel scripts:        {len(all_carousels)}")
    print(f"Video briefs:            {len(all_video_briefs)}")
    print(f"Total pieces:            {total_pieces}")
    print(f"Pipeline duration:       {duration} seconds")
    print(f"Output file:             {os.path.basename(filepath)}")
    print("=" * 60)
    print("\nProject 5 complete. Your weekly content pack is ready.")