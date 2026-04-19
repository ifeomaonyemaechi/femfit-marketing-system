# Skill: Write Promotional Campaign
# FemFit.fit Marketing Operations System

## WHAT THIS SKILL DOES
Generates a single promotional campaign email for FemFit.fit.
Used for flash sales, new product launches, and seasonal moments.
Called by the email-copywriter agent.

## WHEN TO USE THIS SKILL
Use when:
- Running a flash sale or limited-time offer
- Launching a new product or collection
- Sending a seasonal campaign (January, Black Friday, etc.)
- Clearing stock before new drops

## CAMPAIGN TYPES AND RULES

### Flash Sale
TONE: Urgent but not desperate. Direct.
LENGTH: 100-150 words — short on purpose
MUST INCLUDE:
- What is on sale and for how long
- Discount code clearly stated
- Hard end time — no extensions language
- Single CTA

### New Product Launch
TONE: Confident, specific, product-led
LENGTH: 200-250 words
MUST INCLUDE:
- What problem the product solves
- 3 specific product features (not benefits dressed as features)
- How it was tested before launch
- Launch offer if applicable (free shipping, early access)
- Single CTA

### Seasonal Push
TONE: Anti-hype. Acknowledge the season without clichés.
LENGTH: 150-200 words
MUST INCLUDE:
- Acknowledge the moment without performative language
- Reason to buy now that is genuine, not manufactured
- Discount code if applicable
- Single CTA

## EXECUTION INSTRUCTIONS
1. Confirm campaign type before writing
2. Write one email per campaign brief
3. Include subject line, preview text, body, CTA
4. Provide 3 subject line A/B variants
5. Check against brand-voice-guardian rules
6. Save to outputs/FEMFIT_PROMO_[CAMPAIGNNAME]_[YYYYMMDD].md

## QUALITY GATES
Before saving output, confirm:
[ ] No banned words used
[ ] Subject line is under 50 characters
[ ] Preview text is under 90 characters
[ ] Exactly one CTA
[ ] Discount code is clearly visible if applicable
[ ] End date or urgency is specific, not vague
[ ] Copy does not use countdown pressure language

## OUTPUT STRUCTURE
CAMPAIGN TYPE: [flash sale / launch / seasonal]
CAMPAIGN NAME: [name]
================================
SUBJECT LINE: [text]
PREVIEW TEXT: [text]
EMAIL BODY: [full copy]
CTA BUTTON TEXT: [text]

SUBJECT LINE VARIANTS:
A: [variant]
B: [variant]
C: [variant]

## METRICS TO LOG
- Campaign type
- Time to generate
- Word count
- Discount code used (if any)