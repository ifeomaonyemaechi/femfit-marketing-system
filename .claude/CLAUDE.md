# FemFit.fit — AI Marketing Operations System
# Powered by Claude Code | Built by Ifeoma Onyemaechi, AIMarketer.co

## SYSTEM OVERVIEW
This is the AI marketing operations system for FemFit.fit, a women's
fitness DTC brand selling gym wear, shoes, and home workout equipment
for women aged 24-42. All marketing tasks for this brand are handled
by specialised subagents defined in this system.

## BRAND CONTEXT
- Brand: FemFit.fit
- Platform: Klaviyo (email), Shopify (ecommerce), Instagram, TikTok
- Target customer: Women 24-42, busy, motivated, training at home or gym
- Price point: Mid-market, value-conscious but quality-focused
- Location: UK/US markets

## BRAND VOICE RULES — ALWAYS ENFORCE
NEVER use: amazing, incredible, game-changing, transform your body,
slay, queen, goddess, boss babe, exclusive collection, luxurious,
best-selling, perfect for any occasion

ALWAYS use: squat-proof, built for, real women, holds up, train,
no-fuss, fast delivery, your pace, gear, fits right

Voice: Direct, no-nonsense, empowering without being preachy.
Knowledgeable like a friend who trains — not a brand that sells.

## AGENTS
All subagents live in .claude/agents/. Each handles one marketing
function.

- email-copywriter — writes all email campaigns and flows
- social-media-manager — writes Instagram and TikTok content
- content-strategist — builds content calendars and pillars
- brand-voice-guardian — checks all output against brand rules
- marketing-auditor — runs channel audits and scoring
- ad-copywriter — writes Meta and Google ad copy
- seo-strategist — writes product descriptions and blog content

## SKILLS
Reusable task templates live in .claude/skills/. Use these before
writing any content from scratch.

- write-welcome-series.md
- write-promo-campaign.md
- write-reengagement-sequence.md
- write-post-purchase-flow.md
- generate-subject-lines.md
- write-instagram-caption.md
- write-tiktok-script.md
- generate-content-calendar.md
- run-channel-audit.md
- write-product-description.md

## SLASH COMMANDS
/email [campaign type] — generate a full email campaign
/social [platform] [concept] — generate social content
/audit [channel] — run a channel audit
/subjectlines [email brief] — generate 10 subject line variants
/calendar [month] — generate a 30-day content calendar
/voice-check [content] — check content against brand voice rules

## FOLDER STRUCTURE
.claude/agents/ — subagent definition files
.claude/skills/ — reusable skill markdown files
.claude/hooks/ — pre and post hooks for quality control
context/ — brand context, audience profiles, campaign history
scripts/ — Python scripts using the Anthropic API
outputs/ — all generated content saved here

## OUTPUT RULES
- All generated content saved to outputs/ with timestamp
- Format: FEMFIT_[TYPE]_[YYYYMMDD].md
- Every output must pass brand voice check before saving
- Klaviyo-ready emails must include subject line, preview text,
  body copy, and CTA button text

## METRICS TO TRACK
Log these for every generation run:
- Time to completion (seconds)
- Number of pieces generated
- Word count of output
- Agent used 