# run_brand_strategy.py
# Master runner for the FemFit.fit Brand Voice and Content Strategy system.
# This script contains all functions directly — no imports from other scripts.
# Orchestrates the full pipeline in one command:
# Stage 1: Generate brand voice document
# Stage 2: Generate 30-day content strategy
# Stage 3: Generate executive summary and usage guide
# Stage 4: Build and save complete client deliverable

import anthropic
import os
import json
from datetime import datetime

client = anthropic.Anthropic()


# ── Pipeline status printer ──────────────────────────────────────────────────

def print_stage(stage_number, total_stages, stage_name):
    print(f"\n{'=' * 60}")
    print(f"STAGE {stage_number} OF {total_stages}: {stage_name.upper()}")
    print(f"{'=' * 60}")


# ── Intake validator ─────────────────────────────────────────────────────────

def validate_and_load_intake(filepath):
    """
    Checks the intake JSON file exists and contains valid data.
    Stops the pipeline early with a clear message if anything is wrong.
    """

    if not os.path.exists(filepath):
        print(f"\nERROR: Intake file not found at {filepath}")
        print("Run brand_intake.py first to complete the brand interview.")
        exit()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "brand_name" not in data or "categories" not in data:
        print("\nERROR: Intake file is missing required fields.")
        print("Run brand_intake.py again to regenerate the intake file.")
        exit()

    total_answers = sum(
        len(cat["answers"]) for cat in data["categories"]
    )

    if total_answers == 0:
        print("\nERROR: Intake file contains no answers.")
        print("Run brand_intake.py again and answer the questions.")
        exit()

    print(f"✓ Intake file valid — {total_answers} answers found.")
    return data


# ── Format intake answers for Claude ────────────────────────────────────────

def format_answers_for_prompt(intake_data):
    """
    Converts the JSON intake data into a readable text block for Claude.
    """

    formatted = f"BRAND: {intake_data['brand_name']}\n"
    formatted += f"INTERVIEW DATE: {intake_data['interview_date']}\n\n"

    for category in intake_data["categories"]:
        formatted += f"{'─' * 40}\n"
        formatted += f"CATEGORY: {category['category'].upper()}\n"
        formatted += f"{'─' * 40}\n"

        for i, qa in enumerate(category["answers"], start=1):
            formatted += f"Q{i}: {qa['question']}\n"
            formatted += f"A: {qa['answer']}\n\n"

    return formatted


# ── Stage 1: Brand voice analysis ────────────────────────────────────────────

def run_brand_voice_analysis(intake_data):
    """
    Sends intake answers to Claude and returns a brand voice document.
    """

    formatted_answers = format_answers_for_prompt(intake_data)

    system_prompt = """
    You are a senior brand strategist with deep expertise in DTC eCommerce brands.
    You specialise in translating founder interviews into clear, actionable brand
    voice documents that marketing teams and AI systems can use to produce
    consistent, on-brand content.
    Every guideline you write includes a concrete example.
    You write with authority and clarity. No filler. No corporate language.
    """

    user_prompt = f"""
    Below are the answers from a brand discovery interview with {intake_data['brand_name']}.
    Analyse these answers and produce a complete Brand Voice Document.

    INTERVIEW ANSWERS:
    {formatted_answers}

    PRODUCE THE FOLLOWING DOCUMENT STRUCTURE:

    1. BRAND POSITIONING STATEMENT
    A single sharp paragraph capturing who this brand is, who they serve,
    and what makes them different. Max 80 words.

    2. BRAND PERSONALITY
    5 personality traits with a one-sentence description of what each
    trait means for this brand specifically.

    3. TARGET AUDIENCE PROFILE
    Detailed profile including demographics, psychographics, what they
    value, what frustrates them, and what they want to feel.

    4. VOICE AND TONE GUIDELINES
    6 specific writing rules. Each rule must include:
    - The rule stated clearly
    - A DO example
    - A DON'T example

    5. VOCABULARY GUIDE
    10 words or phrases to USE with a note on why each fits.
    10 words or phrases to NEVER USE with a note on why each is wrong.

    6. CONTENT PILLARS
    4 content pillars with pillar name, one sentence description,
    and 3 specific content ideas per pillar.

    7. BRAND VOICE SUMMARY CARD
    A condensed one-page reference a copywriter or AI system can read
    quickly before writing any content for this brand.

    Be specific to {intake_data['brand_name']} throughout.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 2: Content strategy ─────────────────────────────────────────────────

def run_content_strategy(brand_voice_doc):
    """
    Sends the brand voice document to Claude and returns a 30-day content strategy.
    """

    system_prompt = """
    You are a senior content strategist specialising in DTC eCommerce brands.
    You build content strategies that are realistic, channel-appropriate,
    and directly tied to brand voice and business goals.
    Every content idea you produce could be briefed and executed immediately.
    """

    user_prompt = f"""
    Using the brand voice document below, create a complete 30-day content
    strategy for FemFit.fit.

    BRAND VOICE DOCUMENT:
    {brand_voice_doc}

    PRODUCE THE FOLLOWING:

    1. CHANNEL STRATEGY
    Recommend 3 channels. For each explain why it fits the brand,
    what content format works best, realistic posting frequency,
    and one metric to track.

    2. CONTENT PILLARS MAPPED TO CHANNELS
    Map each of the 4 content pillars to the 3 channels.
    Show which channel fits each pillar best and why.

    3. 30-DAY CONTENT CALENDAR
    4 weeks with 5 content pieces per week — 20 total.
    For each piece include:
    - Day and channel
    - Content pillar
    - Format
    - Specific title or hook
    - Brief notes

    4. CONTENT CREATION SYSTEM
    Weekly planning rhythm, batching strategy, and repurposing framework.

    5. FIRST WEEK EXECUTION BRIEF
    Detailed brief for Week 1 only — all 5 pieces with full context,
    key messages, tone notes, and specific details.

    Be specific to FemFit.fit throughout.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 3: Executive summary ────────────────────────────────────────────────

def run_executive_summary(brand_voice_doc, strategy_doc):
    """
    Generates a concise executive summary for the client package.
    """

    user_prompt = f"""
    Write a concise executive summary (200-250 words) introducing this
    complete brand strategy package to the FemFit.fit client.

    The summary should:
    - Open with one sentence capturing what FemFit.fit stands for
    - Explain what this document package contains and how to use it
    - Highlight the 3 most important strategic decisions made
    - Close with one sentence on what consistent application will achieve
    - Address FemFit.fit directly as "you" and "your brand"
    - Be direct and specific — no filler phrases

    BRAND VOICE DOCUMENT EXCERPT:
    {brand_voice_doc[:2000]}

    CONTENT STRATEGY EXCERPT:
    {strategy_doc[:2000]}
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        system="You are a senior brand strategist writing a client-facing document introduction. Be direct, specific, and professional.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 3: Usage guide ──────────────────────────────────────────────────────

def run_usage_guide():
    """
    Generates a practical guide on how to use the brand strategy package.
    """

    user_prompt = """
    Write a practical "How to Use This Document" guide for FemFit.fit.
    For a small DTC eCommerce brand with no dedicated marketing team.

    Include:
    1. Who should read this document and when
    2. How to use the brand voice summary card before writing any content
    3. How to use the content calendar on a weekly basis
    4. How to brief a freelancer, designer, or AI tool using this document
    5. When to revisit and update the strategy

    Under 300 words. Written for a time-poor founder.
    Use numbered steps where appropriate.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        system="You are a senior brand strategist writing practical client guidance. Be concise and actionable.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 4: Assemble and save client document ───────────────────────────────

def assemble_and_save(brand_voice_doc, strategy_doc, executive_summary, usage_guide):
    """
    Assembles all components into one document and saves it.
    """

    today = datetime.now().strftime("%d %B %Y")

    document_sections = [
        "=" * 60,
        "FEMFIT.FIT",
        "BRAND VOICE & CONTENT STRATEGY PACKAGE",
        f"Prepared: {today}",
        "Powered by Claude AI | Delivered by [Your Name]",
        "=" * 60,
        "",
        "DOCUMENT CONTENTS",
        "─" * 40,
        "Section 1: Executive Summary",
        "Section 2: How to Use This Document",
        "Section 3: Brand Voice Document",
        "Section 4: 30-Day Content Strategy",
        "Section 5: Quick Reference Cards",
        "",
        "=" * 60,
        "",
        "SECTION 1: EXECUTIVE SUMMARY",
        "─" * 40,
        "",
        executive_summary,
        "",
        "=" * 60,
        "",
        "SECTION 2: HOW TO USE THIS DOCUMENT",
        "─" * 40,
        "",
        usage_guide,
        "",
        "=" * 60,
        "",
        "SECTION 3: BRAND VOICE DOCUMENT",
        "─" * 40,
        "",
        brand_voice_doc,
        "",
        "=" * 60,
        "",
        "SECTION 4: 30-DAY CONTENT STRATEGY",
        "─" * 40,
        "",
        strategy_doc,
        "",
        "=" * 60,
        "",
        "SECTION 5: QUICK REFERENCE CARDS",
        "─" * 40,
        "",
        "CARD 1 — BEFORE YOU WRITE ANYTHING",
        "─" * 30,
        "Ask yourself these three questions:",
        "1. Would a woman who trains say this to another woman who trains?",
        "2. Am I stating a fact or making a vague claim?",
        "3. Have I used any words from the NEVER USE list?",
        "",
        "CARD 2 — WEEKLY CONTENT CHECKLIST",
        "─" * 30,
        "Sunday:    Plan the week. Confirm 5 pieces.",
        "Monday:    Batch film all video content.",
        "Tuesday:   Edit, write captions, schedule.",
        "Wednesday: Write and schedule email.",
        "Thursday:  Engage. Reshare. Monitor.",
        "Friday:    Post final piece. Review the week.",
        "",
        "CARD 3 — THE FEMFIT.FIT VOICE IN ONE LINE",
        "─" * 30,
        "Confident but not cocky. Direct but warm.",
        "Empowering but never preachy.",
        "Knowledgeable like a friend who trains —",
        "not a brand that sells.",
        "",
        "=" * 60,
        "",
        f"Document prepared for FemFit.fit — {today}",
        "Generated using Claude AI by [Your Name]",
        "Claude AI Co-Worker Specialist | Marketing Automation",
        "=" * 60,
    ]

    document = "\n".join(document_sections)

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/FemFitfit_Brand_Strategy_COMPLETE_{timestamp}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(document)

    return filepath


# ── Main pipeline ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)
    pipeline_start = datetime.now()

    print("\n" + "=" * 60)
    print("FEMFIT.FIT — BRAND STRATEGY PIPELINE")
    print("Running complete brand voice and content strategy system.")
    print(f"Started: {pipeline_start.strftime('%d %B %Y, %H:%M:%S')}")
    print("=" * 60)

    # ── Validate inputs ──────────────────────────────────────────────
    print_stage(0, 4, "Validating inputs")
    intake_data = validate_and_load_intake("outputs/brand_intake_answers.json")
    print(f"✓ Brand: {intake_data['brand_name']}")
    print(f"✓ Interview date: {intake_data['interview_date']}")

    # ── Stage 1: Brand voice ─────────────────────────────────────────
    print_stage(1, 4, "Generating brand voice document")
    print("This may take 30-40 seconds...")
    brand_voice_doc = run_brand_voice_analysis(intake_data)
    print("✓ Brand voice document complete.")

    # ── Stage 2: Content strategy ────────────────────────────────────
    print_stage(2, 4, "Generating 30-day content strategy")
    print("This may take 30-40 seconds...")
    strategy_doc = run_content_strategy(brand_voice_doc)
    print("✓ Content strategy complete.")

    # ── Stage 3: Executive summary and usage guide ───────────────────
    print_stage(3, 4, "Generating executive summary and usage guide")
    executive_summary = run_executive_summary(brand_voice_doc, strategy_doc)
    print("✓ Executive summary complete.")
    usage_guide = run_usage_guide()
    print("✓ Usage guide complete.")

    # ── Stage 4: Assemble and save ───────────────────────────────────
    print_stage(4, 4, "Building complete client deliverable")
    final_filepath = assemble_and_save(
        brand_voice_doc,
        strategy_doc,
        executive_summary,
        usage_guide
    )
    print(f"✓ Complete client package saved.")
    print(f"  File: {os.path.basename(final_filepath)}")

    # ── Pipeline summary ─────────────────────────────────────────────
    pipeline_end = datetime.now()
    duration = (pipeline_end - pipeline_start).seconds

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("─" * 40)
    print(f"Final deliverable: {os.path.basename(final_filepath)}")
    print(f"Total duration: {duration} seconds")
    print(f"Completed: {pipeline_end.strftime('%d %B %Y, %H:%M:%S')}")
    print("=" * 60)
    print("\nProject 2 complete. Your client deliverable is ready.")