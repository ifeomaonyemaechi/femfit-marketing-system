# subject_line_generator.py
# This tool takes an email brief and generates 3 subject line variants
# for A/B testing. Each variant uses a different psychological approach.
# Run this on any campaign type to get testable subject line options.

import anthropic
import os
from brand_voice import FEMFIT_BRAND_VOICE

client = anthropic.Anthropic()

# ── Subject line test briefs ─────────────────────────────────────────────────
# Each dictionary represents one email we want subject line variants for.
# We are generating variants for one email from each campaign type
# to demonstrate the tool across different contexts.

subject_line_briefs = [
    {
        "campaign": "Welcome Series — Email 1",
        "email_objective": "First email to a new subscriber. Introduce the brand and offer 15% off first order.",
        "current_subject": "You're in the right place",
        "offer": "15% off first order — code FEMFIT15"
    },
    {
        "campaign": "Flash Sale",
        "email_objective": "24-hour sitewide sale. 25% off everything. Ends midnight.",
        "current_subject": "25% off everything. 24 hours. That's it.",
        "offer": "25% off — code FEMFIT25 — ends midnight"
    },
    {
        "campaign": "Re-engagement — Email 3",
        "email_objective": "Final email to inactive subscriber. Honest last chance before removal from list.",
        "current_subject": "This is our last email",
        "offer": "15% off if they choose to stay — code STAYWITHUS15"
    },
    {
        "campaign": "Post-Purchase — Email 4",
        "email_objective": "Second purchase nudge sent 21 days after first order. Loyalty reward discount.",
        "current_subject": "Three weeks in — what comes next",
        "offer": "12% off next order — code FEMFITNEXT12"
    }
]


# ── Subject line generation function ────────────────────────────────────────

def generate_subject_variants(brief):
    """
    Generates 3 subject line variants for a given email brief.
    Each variant uses a different psychological approach.

    Parameters:
        brief (dict): Email context and current subject line.

    Returns:
        str: Three subject line variants with labels and preview text.
    """

    user_prompt = f"""
    Generate 3 subject line variants for the following FemFit.fit email.
    Each variant must use a DIFFERENT psychological approach.
    All variants must match the FemFit.fit brand voice — no hype, no filler words.

    CAMPAIGN: {brief['campaign']}
    EMAIL OBJECTIVE: {brief['email_objective']}
    CURRENT SUBJECT LINE: {brief['current_subject']}
    OFFER (if any): {brief['offer']}

    THE THREE PSYCHOLOGICAL APPROACHES TO USE:
    
    Variant A — CURIOSITY: Make the reader want to open to find out more.
    Do not reveal the full offer. Create a genuine information gap.
    
    Variant B — DIRECT BENEFIT: State the clearest benefit or offer plainly.
    No cleverness. Just the most useful thing the reader needs to know.
    
    Variant C — PATTERN INTERRUPT: Say something unexpected for a fitness brand email.
    Subvert the reader's expectation of what this email will say.

    OUTPUT FORMAT — use exactly this structure for each variant:

    VARIANT A — CURIOSITY:
    Subject: [subject line]
    Preview: [preview text that complements the subject]
    Why it works: [one sentence explanation of the psychological mechanism]

    VARIANT B — DIRECT BENEFIT:
    Subject: [subject line]
    Preview: [preview text that complements the subject]
    Why it works: [one sentence explanation of the psychological mechanism]

    VARIANT C — PATTERN INTERRUPT:
    Subject: [subject line]
    Preview: [preview text that complements the subject]
    Why it works: [one sentence explanation of the psychological mechanism]

    Keep every subject line under 50 characters.
    Keep every preview text under 90 characters.
    Do not add any commentary before or after the variants.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        system=FEMFIT_BRAND_VOICE,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content[0].text


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/subject_line_variants.txt", "w", encoding="utf-8") as f:

        header = (
            "=" * 60 + "\n"
            "FEMFIT.FIT — SUBJECT LINE A/B VARIANT GENERATOR\n"
            "3 variants per email — Curiosity / Direct Benefit / Pattern Interrupt\n"
            + "=" * 60
        )
        print(header)
        f.write(header + "\n")

        for brief in subject_line_briefs:

            campaign_header = (
                f"\n{'=' * 60}\n"
                f"CAMPAIGN: {brief['campaign'].upper()}\n"
                f"Current subject: {brief['current_subject']}\n"
                f"{'=' * 60}\n"
            )

            print(campaign_header)
            f.write(campaign_header)

            variants = generate_subject_variants(brief)

            print(variants)
            f.write(variants + "\n")

            divider = f"\n{'─' * 60}\n"
            print(divider)
            f.write(divider)

    print("\n✓ Subject line variants saved to outputs/subject_line_variants.txt")