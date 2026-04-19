# Skill: Write Welcome Series
# FemFit.fit Marketing Operations System

## WHAT THIS SKILL DOES
Generates a 3-email welcome series for new FemFit.fit subscribers.
This skill is called by the email-copywriter agent. It produces
Klaviyo-ready copy for all three emails in sequence.

## WHEN TO USE THIS SKILL
Use when:
- A new subscriber joins the FemFit.fit email list
- The welcome flow needs to be rebuilt or refreshed
- A client brief requests a welcome sequence

## SERIES STRUCTURE

### Email 1 — Sent immediately on signup
PURPOSE: Warm welcome + deliver the discount code
TONE: Confident, direct, genuine. Not gushing.
LENGTH: 150-200 words
MUST INCLUDE:
- Acknowledge they just joined
- One sentence on what FemFit.fit stands for
- Discount code FEMFIT15 for 15% off first order
- Single CTA to shop

### Email 2 — Sent 3 days after signup
PURPOSE: Brand story + social proof
TONE: Personal, founder-voice, real
LENGTH: 200-250 words
MUST INCLUDE:
- Founder origin story (brief — 2-3 sentences)
- Who the real FemFit customer is
- 2 customer quotes (realistic, specific, not generic)
- Reminder that discount code is still active
- CTA to see customer reviews or shop

### Email 3 — Sent 7 days after signup
PURPOSE: Urgency — discount expires in 48 hours
TONE: Direct, no drama, respectful of their time
LENGTH: 150-180 words
MUST INCLUDE:
- Clear statement that code expires in 48 hours
- 3 recommended products with one-line descriptions each
- Single CTA using the discount code
- No guilt, no countdown pressure language

## EXECUTION INSTRUCTIONS
1. Write all 3 emails in sequence
2. Each email must include: subject line, preview text, body, CTA
3. Provide 3 subject line A/B variants per email
4. Check all copy against brand-voice-guardian rules
5. Save output to outputs/FEMFIT_WELCOME_SERIES_[YYYYMMDD].md

## QUALITY GATES
Before saving output, confirm:
[ ] No banned words in any of the 3 emails
[ ] Each email has exactly one CTA
[ ] Subject lines are under 50 characters
[ ] Preview text is under 90 characters
[ ] Discount code FEMFIT15 appears in emails 1 and 3
[ ] Email 2 includes founder voice, not corporate voice
[ ] All 3 emails sound like the same brand

## OUTPUT EXAMPLE STRUCTURE
EMAIL 1 OF 3 — SENT IMMEDIATELY
================================
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
- Total word count across series
- Subject line character counts