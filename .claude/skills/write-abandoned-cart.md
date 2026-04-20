# Skill: Write Abandoned Cart Sequence
# FemFit.fit Marketing Operations System

## WHAT THIS SKILL DOES
Generates a 3-email abandoned cart recovery sequence for
FemFit.fit. Called by the email-copywriter agent. Produces
Klaviyo-ready copy that recovers lost sales without being
pushy or guilt-tripping the customer.

## WHEN TO USE THIS SKILL
Use when:
- A customer adds to cart but does not complete purchase
- The abandoned cart flow needs to be built or refreshed
- Cart recovery rate is below the 12-15% benchmark

## SEQUENCE STRUCTURE

### Email 1 — Sent 1 hour after abandonment
PURPOSE: Gentle reminder, no pressure
TONE: Helpful, assuming the best — maybe they got distracted
LENGTH: 100-130 words
MUST INCLUDE:
- Reference to what they left behind (use merge tag)
- One key product benefit reminder
- Clear CTA back to cart
- No discount in this email — save it for email 3
MUST NOT:
- Guilt trip or create fake urgency
- Say "you forgot" — say "still thinking it over"

### Email 2 — Sent 24 hours after abandonment
PURPOSE: Address the hesitation
TONE: Direct, empathetic, slightly more urgent
LENGTH: 130-160 words
MUST INCLUDE:
- Acknowledge they may be weighing up the decision
- Address the most common objection (fit, quality, price)
- Social proof — one specific customer quote
- CTA back to cart
- Still no discount — build value first

### Email 3 — Sent 72 hours after abandonment
PURPOSE: Final recovery attempt with incentive
TONE: Direct, respectful, clear deadline
LENGTH: 100-130 words
MUST INCLUDE:
- Clear statement this is the last reminder
- Discount code COMEBACK10 for 10% off
- Specific expiry — 48 hours from send
- Single CTA using the discount
MUST NOT:
- Be dramatic or use loss language
- Say "last chance" more than once

## KLAVIYO MERGE TAGS
Use these exactly as written:
- {{ first_name }} — customer first name
- {{ event.extra.line_items }} — abandoned cart items
- {{ event.extra.checkout_url }} — link back to cart

## EXECUTION INSTRUCTIONS
1. Write all 3 emails in sequence
2. Each email must include subject line, preview text,
   body, and CTA button text
3. Provide 3 subject line A/B variants per email
4. Check all copy against brand-voice-guardian rules
5. Save to outputs/FEMFIT_ABANDONED_CART_[YYYYMMDD].md

## QUALITY GATES
Before saving output, confirm:
[ ] No banned words in any of the 3 emails
[ ] Email 1 has no discount
[ ] Email 2 includes social proof
[ ] Email 3 includes COMEBACK10 with 48-hour expiry
[ ] Each email has exactly one CTA
[ ] Subject lines under 50 characters
[ ] Preview text under 90 characters
[ ] No guilt language or fake urgency

## OUTPUT STRUCTURE
EMAIL 1 OF 3 — SENT 1 HOUR AFTER ABANDONMENT
=============================================
SUBJECT LINE: [text]
PREVIEW TEXT: [text]
EMAIL BODY: [full copy]
CTA BUTTON TEXT: [text]

SUBJECT LINE VARIANTS:
A: [variant]
B: [variant]
C: [variant]

[repeat for emails 2 and 3]

## METRICS TO LOG
- Time to generate all 3 emails
- Total word count across sequence
- Discount code used
- Subject line character counts