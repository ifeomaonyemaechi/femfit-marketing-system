# run_outreach_pipeline.py
# Master runner for the AIMarketer.co lead generation and outreach system.
# Runs the complete pipeline in one command:
# Stage 1: Score and qualify leads
# Stage 2: Generate research briefs for qualified leads
# Stage 3: Generate outreach messages (email, DM, LinkedIn)
# Stage 4: Generate 3-touch follow-up sequences
# Stage 5: Build complete campaign summary document

import anthropic
import os
import json
from datetime import datetime
from lead_profiles import LEADS, IDEAL_CLIENT_PROFILE, SCORING_CRITERIA, QUALIFICATION_THRESHOLD

client = anthropic.Anthropic()


# ── Pipeline status printer ──────────────────────────────────────────────────

def print_stage(stage_number, total_stages, stage_name):
    print(f"\n{'=' * 60}")
    print(f"STAGE {stage_number} OF {total_stages}: {stage_name.upper()}")
    print(f"{'=' * 60}")


# ── Stage 1: Lead scoring ────────────────────────────────────────────────────

def score_lead(lead):
    """
    Scores a single lead against qualification criteria.
    Returns the lead with score and qualification status added.
    """

    score = 0
    score_breakdown = {}

    if lead.get("shopify", False):
        score += SCORING_CRITERIA["uses_shopify"]
        score_breakdown["uses_shopify"] = SCORING_CRITERIA["uses_shopify"]
    else:
        score_breakdown["uses_shopify"] = 0

    if lead.get("email_platform"):
        score += SCORING_CRITERIA["has_email_platform"]
        score_breakdown["has_email_platform"] = SCORING_CRITERIA["has_email_platform"]
    else:
        score_breakdown["has_email_platform"] = 0

    followers = lead.get("instagram_followers", 0)
    if 1000 <= followers <= 50000:
        score += SCORING_CRITERIA["follower_range_1k_to_50k"]
        score_breakdown["follower_range_1k_to_50k"] = SCORING_CRITERIA["follower_range_1k_to_50k"]
    else:
        score_breakdown["follower_range_1k_to_50k"] = 0

    frequency = lead.get("posting_frequency", "")
    posts_regularly = any(
        str(n) in frequency for n in range(3, 10)
    ) or "daily" in frequency.lower()

    if posts_regularly:
        score += SCORING_CRITERIA["posts_regularly"]
        score_breakdown["posts_regularly"] = SCORING_CRITERIA["posts_regularly"]
    else:
        score_breakdown["posts_regularly"] = 0

    pain_points = lead.get("pain_points_observed", [])
    if len(pain_points) >= 2:
        score += SCORING_CRITERIA["has_pain_points"]
        score_breakdown["has_pain_points"] = SCORING_CRITERIA["has_pain_points"]
    else:
        score_breakdown["has_pain_points"] = 0

    if lead.get("recent_activity"):
        score += SCORING_CRITERIA["recent_activity_detected"]
        score_breakdown["recent_activity_detected"] = SCORING_CRITERIA["recent_activity_detected"]
    else:
        score_breakdown["recent_activity_detected"] = 0

    scored_lead = lead.copy()
    scored_lead["qualification_score"] = score
    scored_lead["score_breakdown"] = score_breakdown
    scored_lead["qualified"] = score >= QUALIFICATION_THRESHOLD

    return scored_lead


# ── Stage 2: Research brief ──────────────────────────────────────────────────

def generate_research_brief(lead):
    """
    Sends a qualified lead to Claude and returns a research brief.
    """

    pain_points_text = "\n".join(
        f"- {point}" for point in lead["pain_points_observed"]
    )

    user_prompt = f"""
    You are a business development researcher for AIMarketer.co — a Claude AI
    Co-Worker Specialist agency helping Shopify DTC brands automate their
    marketing workflows using AI.

    Analyse the following lead and produce a research brief.

    LEAD INFORMATION:
    Brand: {lead['brand_name']}
    Founder: {lead['founder_name']} ({lead['role']})
    Industry: {lead['industry']}
    Products: {lead['product_focus']}
    Instagram followers: {lead['instagram_followers']:,}
    Email platform: {lead['email_platform']}
    Posting frequency: {lead['posting_frequency']}
    Qualification score: {lead['qualification_score']}/100

    OBSERVED PAIN POINTS:
    {pain_points_text}

    RECENT ACTIVITY:
    {lead['recent_activity']}

    CURRENT CONTENT TONE:
    {lead['tone_of_current_content']}

    PRODUCE A RESEARCH BRIEF WITH THESE SECTIONS:

    SITUATION SUMMARY:
    Two to three sentences on where this brand is right now.

    PRIMARY PAIN POINT:
    The single most pressing marketing problem this brand has.

    OUTREACH ANGLE:
    The strongest hook for reaching out to this specific brand.

    SERVICE FIT:
    Which AIMarketer.co service fits this lead best and why.

    PERSONALISATION HOOKS:
    Three specific details that can be referenced naturally in outreach.

    Keep the entire brief under 300 words. Be specific and direct.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        system="You are a precise business development researcher. Your briefs are specific, actionable, and free of generic sales language.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 3: Outreach messages ───────────────────────────────────────────────

def generate_outreach_messages(lead):
    """
    Generates cold email, Instagram DM, and LinkedIn message for a lead.
    """

    pain_points_text = "\n".join(
        f"- {point}" for point in lead["pain_points_observed"]
    )

    user_prompt = f"""
    You are writing outreach messages for AIMarketer.co.
    The sender is Ifeoma — founder of AIMarketer.co, a Claude AI Co-Worker
    Specialist with a background in DevOps and Klaviyo email marketing.

    LEAD INFORMATION:
    Brand: {lead['brand_name']}
    Founder: {lead['founder_name']} ({lead['role']})
    Industry: {lead['industry']}
    Products: {lead['product_focus']}
    Instagram: {lead['instagram_handle']} ({lead['instagram_followers']:,} followers)
    Email platform: {lead['email_platform']}

    OBSERVED PAIN POINTS:
    {pain_points_text}

    RECENT ACTIVITY:
    {lead['recent_activity']}

    RESEARCH BRIEF:
    {lead['research_brief']}

    WRITE THREE OUTREACH MESSAGES:

    MESSAGE 1 — COLD EMAIL:
    - Subject line referencing something specific about their brand
    - Opening line proving you have looked at their brand
    - One specific observation about their marketing gap
    - Low-pressure CTA — free audit or 15-minute call
    - Signed from Ifeoma, AIMarketer.co
    - Maximum 150 words in the body
    - No buzzwords. No "I hope this email finds you well."

    Format as:
    SUBJECT:
    BODY:

    MESSAGE 2 — INSTAGRAM DM:
    - Under 80 words
    - Reference one specific thing about their content
    - End with one simple question
    - No links. Sound like a real person.

    Format as:
    DM:

    MESSAGE 3 — LINKEDIN MESSAGE:
    - Founder to founder tone
    - Reference their industry and growth stage
    - Soft CTA — invite a conversation
    - Maximum 120 words. No buzzwords.

    Format as:
    LINKEDIN:
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1200,
        system="You are an expert at writing personalised cold outreach that converts. Your messages are specific, human, and never sound like templates.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 4: Follow-up sequence ─────────────────────────────────────────────

def generate_followup_sequence(outreach_record):
    """
    Generates a 3-touch follow-up email sequence for a lead.
    """

    user_prompt = f"""
    You are writing follow-up emails for AIMarketer.co.
    The sender is Ifeoma, founder of AIMarketer.co.
    She sent initial outreach to this lead with no response.

    LEAD:
    Brand: {outreach_record['brand_name']}
    Contact: {outreach_record['founder_name']} — {outreach_record['role']}
    Industry: {outreach_record['industry']}

    INITIAL OUTREACH SENT:
    {outreach_record['outreach_messages'][:800]}

    WRITE A 3-TOUCH FOLLOW-UP EMAIL SEQUENCE:

    TOUCH 1 — Day 4 — VALUE ADD:
    Give something useful. A specific insight about their brand or industry.
    Do not repeat the pitch. Lead with value.
    Under 100 words. New subject line.

    TOUCH 2 — Day 8 — TIMELY RELEVANCE:
    Reference something current — a season, trend, or business moment.
    Make the timing feel relevant right now.
    Under 100 words. New subject line.

    TOUCH 3 — Day 14 — CLEAN CLOSE:
    Tell them this is the last email. No hard feelings.
    Leave one final specific reason to respond.
    Under 80 words. New subject line.

    RULES FOR ALL THREE:
    - Never say "just checking in" or "circling back"
    - Do not apologise for following up
    - Each message must feel different from the previous
    - Reference {outreach_record['brand_name']} specifically in each message
    - Sign each from Ifeoma, AIMarketer.co

    FORMAT EACH AS:
    TOUCH [number]: [strategy]
    SUBJECT:
    BODY:
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system="You are an expert at writing follow-up sequences that feel human, respectful, and specific.",
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text


# ── Stage 5: Campaign summary ────────────────────────────────────────────────

def build_campaign_summary(scored_leads, all_outreach, all_followups, duration):
    """
    Builds a complete campaign summary document.

    Parameters:
        scored_leads (list): All leads with scores.
        all_outreach (list): All outreach records with messages.
        all_followups (list): All follow-up records with sequences.
        duration (int): Pipeline duration in seconds.

    Returns:
        str: The complete campaign summary as formatted text.
    """

    qualified = [l for l in scored_leads if l["qualified"]]
    today = datetime.now().strftime("%d %B %Y")

    sections = [
        "=" * 60,
        "AIMARKETER.CO",
        "LEAD GENERATION AND OUTREACH CAMPAIGN",
        f"Generated: {today}",
        f"Pipeline duration: {duration} seconds",
        "=" * 60,
        "",
        "CAMPAIGN OVERVIEW",
        "─" * 40,
        f"Total leads processed:     {len(scored_leads)}",
        f"Leads qualified:           {len(qualified)}",
        f"Qualification rate:        {int(len(qualified)/len(scored_leads)*100)}%",
        f"Outreach messages sent:    {len(all_outreach) * 3} (email, DM, LinkedIn per lead)",
        f"Follow-up emails queued:   {len(all_followups) * 3} (3 touches per lead)",
        f"Total touchpoints:         {len(all_outreach) * 3 + len(all_followups) * 3}",
        "",
        "=" * 60,
        "",
        "QUALIFIED LEADS SUMMARY",
        "─" * 40,
        ""
    ]

    for lead in qualified:
        sections.append(f"Brand:    {lead['brand_name']}")
        sections.append(f"Contact:  {lead['founder_name']} — {lead['role']}")
        sections.append(f"Industry: {lead['industry']}")
        sections.append(f"Score:    {lead['qualification_score']}/100")
        sections.append("")

    sections += [
        "=" * 60,
        "",
        "OUTREACH AND FOLLOW-UP LOG",
        "─" * 40,
        ""
    ]

    for i, record in enumerate(all_outreach):
        sections.append(f"{'─' * 40}")
        sections.append(f"LEAD {i+1}: {record['brand_name']}")
        sections.append(f"{'─' * 40}")
        sections.append("INITIAL OUTREACH:")
        sections.append(record["outreach_messages"])
        sections.append("")

        matching_followup = next(
            (f for f in all_followups if f["id"] == record["id"]), None
        )

        if matching_followup:
            sections.append("FOLLOW-UP SEQUENCE:")
            sections.append(matching_followup["followup_sequence"])

        sections.append("")

    sections += [
        "=" * 60,
        "CAMPAIGN COMPLETE",
        f"Generated by Ifeoma Onyemaechi — AIMarketer.co",
        "Claude AI Co-Worker Specialist | Marketing Automation",
        "=" * 60
    ]

    return "\n".join(sections)


# ── Main pipeline ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)
    pipeline_start = datetime.now()

    print("\n" + "=" * 60)
    print("AIMARKETER.CO — OUTREACH PIPELINE")
    print("Running complete lead generation and outreach system.")
    print(f"Started: {pipeline_start.strftime('%d %B %Y, %H:%M:%S')}")
    print("=" * 60)

    # ── Stage 1: Score all leads ─────────────────────────────────────
    print_stage(1, 5, "Scoring and qualifying leads")

    scored_leads = []
    for lead in LEADS:
        scored = score_lead(lead)
        scored_leads.append(scored)
        status = "✓ QUALIFIED" if scored["qualified"] else "✗ DISQUALIFIED"
        print(f"  {scored['brand_name']}: {scored['qualification_score']}/100 — {status}")

    qualified_leads = [l for l in scored_leads if l["qualified"]]
    print(f"\n✓ {len(qualified_leads)} of {len(scored_leads)} leads qualified.")

    # ── Stage 2: Research briefs ─────────────────────────────────────
    print_stage(2, 5, "Generating research briefs")

    qualified_with_briefs = []
    for i, lead in enumerate(qualified_leads, start=1):
        print(f"  Researching {i} of {len(qualified_leads)}: {lead['brand_name']}...")
        brief = generate_research_brief(lead)
        lead_with_brief = lead.copy()
        lead_with_brief["research_brief"] = brief
        qualified_with_briefs.append(lead_with_brief)
        print(f"  ✓ Done.")

    # ── Stage 3: Outreach messages ───────────────────────────────────
    print_stage(3, 5, "Generating outreach messages")

    all_outreach = []
    for i, lead in enumerate(qualified_with_briefs, start=1):
        print(f"  Writing outreach {i} of {len(qualified_with_briefs)}: {lead['brand_name']}...")
        messages = generate_outreach_messages(lead)
        all_outreach.append({
            "id": lead["id"],
            "brand_name": lead["brand_name"],
            "founder_name": lead["founder_name"],
            "role": lead["role"],
            "industry": lead["industry"],
            "qualification_score": lead["qualification_score"],
            "outreach_messages": messages
        })
        print(f"  ✓ Done.")

    # ── Stage 4: Follow-up sequences ────────────────────────────────
    print_stage(4, 5, "Generating follow-up sequences")

    all_followups = []
    for i, record in enumerate(all_outreach, start=1):
        print(f"  Follow-up {i} of {len(all_outreach)}: {record['brand_name']}...")
        followup = generate_followup_sequence(record)
        all_followups.append({
            "id": record["id"],
            "brand_name": record["brand_name"],
            "founder_name": record["founder_name"],
            "role": record["role"],
            "industry": record["industry"],
            "qualification_score": record["qualification_score"],
            "followup_sequence": followup
        })
        print(f"  ✓ Done.")

    # ── Stage 5: Campaign summary ────────────────────────────────────
    print_stage(5, 5, "Building campaign summary document")

    pipeline_end = datetime.now()
    duration = (pipeline_end - pipeline_start).seconds

    summary = build_campaign_summary(
        scored_leads, all_outreach, all_followups, duration
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filepath = f"outputs/AIMARKETER_CAMPAIGN_{timestamp}.txt"

    with open(summary_filepath, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✓ Campaign summary saved: {os.path.basename(summary_filepath)}")

    # ── Pipeline summary ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("─" * 40)
    print(f"Leads scored:          {len(scored_leads)}")
    print(f"Leads qualified:       {len(qualified_leads)}")
    print(f"Research briefs:       {len(qualified_with_briefs)}")
    print(f"Outreach messages:     {len(all_outreach) * 3}")
    print(f"Follow-up emails:      {len(all_followups) * 3}")
    print(f"Total touchpoints:     {len(all_outreach) * 3 + len(all_followups) * 3}")
    print(f"Pipeline duration:     {duration} seconds")
    print(f"Output file:           {os.path.basename(summary_filepath)}")
    print("=" * 60)
    print("\nProject 3 complete. Your campaign is ready.")