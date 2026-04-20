# post_purchase.py
# This script generates a 4-email post-purchase follow-up sequence
# for FemFit.fit. Target: customers who have just completed a purchase
# on the Shopify store.
# Goal: reduce returns, build loyalty, and drive a second purchase.

import anthropic
import os
from brand_voice import FEMFIT_BRAND_VOICE

# Set up the Anthropic client.
client = anthropic.Anthropic()

# ── Post-purchase sequence briefs ────────────────────────────────────────────
# Four emails covering the full post-purchase journey.
# Tone moves from: celebratory → anticipatory → supportive → rewarding

post_purchase_briefs = [
    {
        "email_number": 1,
        "phase": "Order Confirmation",
        "timing": "Sent immediately after purchase",
        "objective": "Confirm the order, reinforce that the customer made a great decision, and set a warm tone for the relationship going forward. This is not a cold transactional receipt — it is the first message in an ongoing relationship.",
        "context": "Customer has just purchased from FemFit.fit for the first time. They may have bought gym wear, shoes, or home equipment.",
        "key_messages": [
            "Your order is confirmed and being packed",
            "You made a solid choice — here is why your gear is worth the wait",
            "What to expect next — delivery timeline and tracking"
        ],
        "offer": "None — do not sell anything in this email",
        "primary_cta": "Track your order",
        "tone_note": "Warm, confident, and reassuring. Like a confirmation from a brand that actually cares about what happens after the sale. Not a robot receipt. Not over-the-top excitement. Just solid and genuine."
    },
    {
        "email_number": 2,
        "phase": "Pre-Delivery Anticipation",
        "timing": "Sent 3 days after purchase, before the order arrives",
        "objective": "Build anticipation before the order arrives. Give the customer something useful to do while they wait — prepare for their first session in the new gear. Reduce the chance of returns by reinforcing product quality and what to expect.",
        "context": "Order is in transit. Customer is waiting for delivery. This is a good moment to set expectations about product quality and first use.",
        "key_messages": [
            "Your order is on its way",
            "Here is what to expect when you first wear or use your FemFit gear",
            "A few tips for getting the most out of your new kit from day one"
        ],
        "offer": "None — this email is purely value-add",
        "primary_cta": "Check your tracking",
        "tone_note": "Excited but grounded. Like a training partner texting you the night before a new program starts. Practical and warm. Include one specific product care or first-use tip relevant to fitness gear."
    },
    {
        "email_number": 3,
        "phase": "Post-Delivery Check-in",
        "timing": "Sent 7 days after purchase — assuming delivery has happened",
        "objective": "Check in after delivery. Encourage the customer to actually use the gear and share their experience. Open a two-way conversation. This is the email that turns a transaction into a relationship.",
        "context": "Order should have been delivered by now. Customer has had a few days to use the product.",
        "key_messages": [
            "Your order should have arrived — how is it fitting?",
            "We want to know how your first session went",
            "If anything is not right, we will fix it — no questions asked"
        ],
        "offer": "None — focus entirely on the customer experience",
        "primary_cta": "Share your experience",
        "tone_note": "Genuine and conversational. This email should feel like it was written by a real person who actually wants to know how the gear performed — not a feedback-farming template. Short. Direct. Human."
    },
    {
        "email_number": 4,
        "phase": "Second Purchase Nudge",
        "timing": "Sent 21 days after purchase",
        "objective": "Introduce the customer to a complementary product they have not bought yet. Reward their first purchase with a loyalty discount. Make the second purchase feel like a natural next step, not a hard sell.",
        "context": "Customer bought gym wear or shoes on their first order. Now we introduce them to complementary categories — equipment if they bought apparel, apparel if they bought equipment.",
        "key_messages": [
            "You have been training in your FemFit gear for three weeks now",
            "Here is what our customers add to their kit after their first order",
            "As a thank you for your first purchase — here is an exclusive returning customer discount"
        ],
        "offer": "12% off next order — code: FEMFITNEXT12 — valid for 7 days",
        "primary_cta": "Shop your next piece",
        "tone_note": "Confident and reward-focused. The customer has earned this. Do not be sycophantic about it — just treat them like a valued customer who has proven they train. The discount has a deadline but do not make urgency the headline."
    }
]


# ── Email generation function ────────────────────────────────────────────────

def generate_post_purchase_email(brief):
    """
    Sends a post-purchase email brief to Claude and returns the copy.

    Parameters:
        brief (dict): Dictionary containing the email brief details.

    Returns:
        str: The full post-purchase email copy generated by Claude.
    """

    user_prompt = f"""
    Write Email {brief['email_number']} of 4 in the FemFit.fit post-purchase sequence.

    PHASE: {brief['phase']}
    TIMING: {brief['timing']}
    
    OBJECTIVE: {brief['objective']}
    
    CONTEXT: {brief['context']}
    
    KEY MESSAGES TO INCLUDE:
    {chr(10).join(f"- {msg}" for msg in brief['key_messages'])}
    
    OFFER: {brief['offer']}
    PRIMARY CTA: {brief['primary_cta']}
    
    TONE GUIDANCE: {brief['tone_note']}
    
    OUTPUT FORMAT — use exactly these labels:
    SUBJECT LINE:
    PREVIEW TEXT:
    EMAIL BODY:
    CTA BUTTON TEXT:
    
    Keep the email body between 120 and 170 words.
    Write in second person (you/your).
    Do not add any commentary before or after the email output.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=FEMFIT_BRAND_VOICE,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content[0].text


# ── Main runner with file output ─────────────────────────────────────────────

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/post_purchase_output.txt", "w", encoding="utf-8") as f:

        header = (
            "=" * 60 + "\n"
            "FEMFIT.FIT — POST-PURCHASE FOLLOW-UP GENERATOR\n"
            "Target: Customers who have just completed a purchase\n"
            "Generating 4-email post-purchase sequence...\n"
            + "=" * 60
        )
        print(header)
        f.write(header + "\n")

        for brief in post_purchase_briefs:

            email_header = (
                f"\n{'=' * 60}\n"
                f"EMAIL {brief['email_number']} OF 4 — {brief['phase'].upper()}\n"
                f"Timing: {brief['timing']}\n"
                f"{'=' * 60}\n"
            )

            print(email_header)
            f.write(email_header)

            email_copy = generate_post_purchase_email(brief)

            print(email_copy)
            f.write(email_copy + "\n")

            divider = f"\n{'─' * 60}\n"
            print(divider)
            f.write(divider)

    print("\n✓ Post-purchase sequence saved to outputs/post_purchase_output.txt")