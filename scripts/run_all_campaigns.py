# run_all_campaigns.py
# Master runner for the FemFit.fit email campaign system.
# Runs all four campaign generators in one command and saves
# a single consolidated output file with all 13 emails.

import anthropic
import os
from datetime import datetime

from brand_voice import FEMFIT_BRAND_VOICE
from welcome_series import welcome_briefs, generate_welcome_email
from promo_campaign import promo_campaigns, generate_promo_email
from reengagement import reengagement_briefs, generate_reengagement_email
from post_purchase import post_purchase_briefs, generate_post_purchase_email

client = anthropic.Anthropic()

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"outputs/FEMFIT_FULL_CAMPAIGN_SYSTEM_{timestamp}.txt"

    with open(output_filename, "w", encoding="utf-8") as f:

        # ── Master header ────────────────────────────────────────────────
        master_header = "\n".join([
            "=" * 60,
            "FEMFIT.FIT — COMPLETE EMAIL CAMPAIGN SYSTEM",
            f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
            "Brand: FemFit.fit | Platform: Klaviyo | Powered by Claude AI",
            "=" * 60,
            "",
            "SYSTEM CONTENTS:",
            "1. Welcome Series (3 emails)",
            "2. Promotional Campaigns (3 emails)",
            "3. Re-engagement Sequence (3 emails)",
            "4. Post-Purchase Follow-Up (4 emails)",
            "-" * 60,
            "Total: 13 emails across 4 campaign types",
            "=" * 60
        ])
        print(master_header)
        f.write(master_header + "\n")

        # ── Section 1: Welcome Series ────────────────────────────────────
        section1 = "\n".join([
            "",
            "#" * 60,
            "SECTION 1: WELCOME SERIES",
            "Trigger: New subscriber joins the FemFit.fit list",
            "Platform: Klaviyo Welcome Flow",
            "#" * 60
        ])
        print(section1)
        f.write(section1 + "\n")

        for brief in welcome_briefs:
            email_header = "\n".join([
                "",
                "=" * 60,
                f"EMAIL {brief['email_number']} OF 3 — {brief['timing'].upper()}",
                "=" * 60
            ])
            print(email_header)
            f.write(email_header + "\n")
            email_copy = generate_welcome_email(brief)
            print(email_copy)
            f.write(email_copy + "\n" + "-" * 60 + "\n")

        # ── Section 2: Promotional Campaigns ────────────────────────────
        section2 = "\n".join([
            "",
            "#" * 60,
            "SECTION 2: PROMOTIONAL CAMPAIGNS",
            "Trigger: Business events — sales, launches, seasonal moments",
            "Platform: Klaviyo Campaigns",
            "#" * 60
        ])
        print(section2)
        f.write(section2 + "\n")

        for i, campaign in enumerate(promo_campaigns):
            email_header = "\n".join([
                "",
                "=" * 60,
                f"CAMPAIGN {i + 1} OF 3: {campaign['campaign_name'].upper()}",
                "=" * 60
            ])
            print(email_header)
            f.write(email_header + "\n")
            email_copy = generate_promo_email(campaign)
            print(email_copy)
            f.write(email_copy + "\n" + "-" * 60 + "\n")

        # ── Section 3: Re-engagement Sequence ───────────────────────────
        section3 = "\n".join([
            "",
            "#" * 60,
            "SECTION 3: RE-ENGAGEMENT SEQUENCE",
            "Trigger: Subscriber inactive for 90+ days",
            "Platform: Klaviyo Flow — Winback",
            "#" * 60
        ])
        print(section3)
        f.write(section3 + "\n")

        for brief in reengagement_briefs:
            email_header = "\n".join([
                "",
                "=" * 60,
                f"EMAIL {brief['email_number']} OF 3 — {brief['strategy'].upper()}",
                "=" * 60
            ])
            print(email_header)
            f.write(email_header + "\n")
            email_copy = generate_reengagement_email(brief)
            print(email_copy)
            f.write(email_copy + "\n" + "-" * 60 + "\n")

        # ── Section 4: Post-Purchase Sequence ───────────────────────────
        section4 = "\n".join([
            "",
            "#" * 60,
            "SECTION 4: POST-PURCHASE FOLLOW-UP",
            "Trigger: Customer completes a purchase on Shopify",
            "Platform: Klaviyo Flow — Post-Purchase",
            "#" * 60
        ])
        print(section4)
        f.write(section4 + "\n")

        for brief in post_purchase_briefs:
            email_header = "\n".join([
                "",
                "=" * 60,
                f"EMAIL {brief['email_number']} OF 4 — {brief['phase'].upper()}",
                "=" * 60
            ])
            print(email_header)
            f.write(email_header + "\n")
            email_copy = generate_post_purchase_email(brief)
            print(email_copy)
            f.write(email_copy + "\n" + "-" * 60 + "\n")

        # ── Master footer ────────────────────────────────────────────────
        footer = "\n".join([
            "",
            "=" * 60,
            "SYSTEM GENERATION COMPLETE",
            "13 emails generated across 4 campaign types.",
            "All copy is brand-voice consistent and Klaviyo-ready.",
            f"Output saved to: {output_filename}",
            "=" * 60
        ])
        print(footer)
        f.write(footer)

    print(f"\n✓ Full campaign system saved to {output_filename}")