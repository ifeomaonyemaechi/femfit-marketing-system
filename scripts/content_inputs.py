# content_inputs.py
# This file defines the brand voice, content pillars, platform specs,
# and content briefs for the FemFit.fit social media content engine.
# Every generator script in this project imports from this file.

# ── Brand voice rules ────────────────────────────────────────────────────────
# Condensed from the full brand voice document in Project 2.
# Used as the system prompt foundation for all content generation.

BRAND_VOICE = """
You are a social media content writer for FemFit.fit — a women's fitness
DTC brand on Shopify selling gym wear, gym shoes, and home workout equipment.

BRAND PERSONALITY:
- Motivated but not preachy
- No-nonsense and direct
- Warm without being soft
- Knowledgeable like a friend who trains — not a brand that sells

VOICE RULES:
- Short sentences. Active verbs. No filler.
- Never use: amazing, incredible, game-changing, slay, queen, goddess
- No exclamation marks unless they genuinely earn their place
- No generic fitness clichés — no "smash your goals" or "unleash your potential"
- Minimal emoji — only where it adds something, never as decoration
- Write in second person (you/your) unless specified otherwise
- Assume the reader already trains — do not try to motivate her to start

TARGET AUDIENCE:
Women aged 24-42 who train seriously at home or in the gym.
Self-motivated, time-poor, allergic to performative fitness culture.
They want gear that works and content that respects their intelligence.

QUICK VOICE TEST:
Before finalising any content ask: Would a woman who trains say this
to another woman who trains? If it sounds like a brand — rewrite it.
"""


# ── Content pillars ──────────────────────────────────────────────────────────
# Four pillars from the Project 2 brand strategy.
# Each piece of content belongs to one pillar.

CONTENT_PILLARS = [
    {
        "name": "Real Training Real Results",
        "description": "Content showing actual women using FemFit gear in real training scenarios. Not posed. Not filtered. Real sessions.",
        "tone": "Authentic and grounded. Let the training speak.",
        "primary_channel": "TikTok",
        "secondary_channel": "Instagram Reels"
    },
    {
        "name": "Fit and Function",
        "description": "Educational content about finding the right fit, understanding gear quality, and what makes FemFit products different.",
        "tone": "Knowledgeable and specific. Lead with product details not marketing language.",
        "primary_channel": "Instagram Carousels",
        "secondary_channel": "Email"
    },
    {
        "name": "Home Gym Life",
        "description": "Content for women who train at home — practical, space-smart, and realistic about what home training actually looks like.",
        "tone": "Practical and relatable. No aspirational home gym fantasy.",
        "primary_channel": "Instagram Reels",
        "secondary_channel": "TikTok"
    },
    {
        "name": "Train For You",
        "description": "Content centred on the philosophy that women train for themselves — for how it makes them feel, not for how they look.",
        "tone": "Empowering but never preachy. Let the message land quietly.",
        "primary_channel": "Instagram Stories",
        "secondary_channel": "Email"
    }
]


# ── Platform specifications ──────────────────────────────────────────────────
# Technical and stylistic requirements for each platform.
# Used to ensure content is formatted correctly for each channel.

PLATFORM_SPECS = {
    "instagram_feed": {
        "caption_length": "150-300 words",
        "hook_length": "First line under 10 words — must stop the scroll",
        "hashtag_count": "5-10 relevant hashtags",
        "cta_style": "Question or soft invitation — not a command",
        "emoji_use": "1-3 maximum — only where meaningful",
        "line_breaks": "Short paragraphs — max 3 lines each"
    },
    "instagram_reels": {
        "caption_length": "50-150 words",
        "hook_length": "On-screen text hook under 7 words",
        "hashtag_count": "3-8 hashtags",
        "cta_style": "Direct and simple — one action only",
        "emoji_use": "1-2 maximum",
        "video_length": "30-90 seconds optimal"
    },
    "tiktok": {
        "caption_length": "50-100 words",
        "hook_length": "First 3 seconds must hook — state the payoff immediately",
        "hashtag_count": "3-6 hashtags",
        "cta_style": "Conversational — like ending a chat with a friend",
        "emoji_use": "2-4 — TikTok audience expects slightly more",
        "video_length": "15-60 seconds optimal"
    },
    "instagram_carousel": {
        "slide_count": "5-8 slides",
        "slide_1": "Hook slide — bold claim or question that earns the swipe",
        "slide_2_to_last": "One clear point per slide — no cramming",
        "last_slide": "Summary or CTA — give them something to save or share",
        "caption_length": "100-200 words",
        "hashtag_count": "5-10 hashtags"
    }
}


# ── Content batch briefs ─────────────────────────────────────────────────────
# One week of content briefs — 5 pieces across 3 channels.
# Each brief is a specific content request the generators will execute.
# These map directly to Week 1 of the 30-day calendar from Project 2.

CONTENT_BRIEFS = [
    {
        "brief_id": "BRIEF001",
        "day": "Monday",
        "platform": "instagram_carousel",
        "pillar": "Fit and Function",
        "format": "Carousel — 6 slides",
        "title": "The 60-second squat-proof test (and why most leggings fail it)",
        "objective": "Educate the audience on how to test whether leggings are genuinely squat-proof. Position FemFit leggings as the ones that pass. Drive saves and shares.",
        "key_messages": [
            "Most brands claim squat-proof — few actually deliver",
            "There is a simple 60-second test anyone can do in store or at home",
            "FemFit leggings were designed specifically to pass this test",
            "Knowing how to test means never wasting money on leggings that fail mid-session"
        ],
        "cta": "Save this for your next leggings purchase",
        "tone_note": "Educational and confident. Let the test speak for itself. Do not oversell."
    },
    {
        "brief_id": "BRIEF002",
        "day": "Tuesday",
        "platform": "tiktok",
        "pillar": "Real Training Real Results",
        "format": "Reel — 45 seconds",
        "title": "What 6 months of leg days did to my relationship with leggings",
        "objective": "First-person founder or customer perspective on how serious training changes what you need from gym wear. Authentic and specific.",
        "key_messages": [
            "After 6 months of serious leg days you know exactly what matters in a legging",
            "Rolling waistband, see-through fabric, and poor compression are dealbreakers",
            "FemFit leggings were built by someone who learned this the hard way",
            "Gear should be the last thing on your mind when you are training"
        ],
        "cta": "What is your biggest legging dealbreaker? Drop it below.",
        "tone_note": "Personal and direct. Reads like a genuine reflection, not a product review."
    },
    {
        "brief_id": "BRIEF003",
        "day": "Wednesday",
        "platform": "instagram_feed",
        "pillar": "Train For You",
        "format": "Single image caption",
        "title": "Why I stopped training for anyone else",
        "objective": "Brand values content that resonates emotionally without preaching. Speaks to the woman who trains for herself — not for aesthetics or anyone else's approval.",
        "key_messages": [
            "There is a shift that happens when you start training for yourself",
            "The sessions get better. The results follow. The noise stops mattering.",
            "FemFit.fit was built for women who have already made that shift"
        ],
        "cta": "Tell us — what made you start training for yourself?",
        "tone_note": "Quiet and grounded. No empowerment slogans. Let the idea breathe."
    },
    {
        "brief_id": "BRIEF004",
        "day": "Thursday",
        "platform": "instagram_reels",
        "pillar": "Home Gym Life",
        "format": "Reel — 60 seconds",
        "title": "5:47am. Kids asleep. 20 minutes. Let's go.",
        "objective": "Relatable home training content for the mum or busy woman who trains in the margins of her day. Practical and real — no aspirational home gym setup.",
        "key_messages": [
            "The best training session is the one you actually do",
            "20 minutes in your living room before the house wakes up counts",
            "You do not need a full hour or a perfect setup to train seriously",
            "FemFit gear works as hard in your living room as it does in the gym"
        ],
        "cta": "What time do you train? Early birds reply below.",
        "tone_note": "Warm and real. This should feel like a text from a friend who also trains at 5am."
    },
    {
        "brief_id": "BRIEF005",
        "day": "Friday",
        "platform": "tiktok",
        "pillar": "Fit and Function",
        "format": "Reel — 30 seconds",
        "title": "Sports bra red flags (from someone who has worn them all)",
        "objective": "Quick educational content about what to avoid when buying sports bras. Positions FemFit as the brand that solved these problems.",
        "key_messages": [
            "There are four sports bra red flags that serious trainers know to avoid",
            "Underwire that digs, straps that slip, cups that gap, fabric that pills",
            "FemFit sports bras were designed to eliminate all four",
            "Your sports bra should be completely forgotten mid-session"
        ],
        "cta": "Which red flag have you experienced? We want to know.",
        "tone_note": "Quick and punchy. List format works well here. Authoritative without being preachy."
    }
]


# ── Hashtag sets ─────────────────────────────────────────────────────────────
# Pre-researched hashtag sets by pillar and platform.
# Generators append these to captions automatically.

HASHTAG_SETS = {
    "Real Training Real Results": {
        "instagram": "#womenwhолift #girlswholift #strengthtraining #realtraining #femfit #womensfitness #gymwear #trainhard #liftinglife #powerlifting",
        "tiktok": "#girlswholift #strengthtraining #femfit #womensfitness #gymtok"
    },
    "Fit and Function": {
        "instagram": "#gymwear #activewear #gymleggings #sportsbra #workoutgear #femfit #womensfitness #gymfashion #functionalfitness #qualitygear",
        "tiktok": "#gymwear #activewear #gymleggings #femfit #workoutgear"
    },
    "Home Gym Life": {
        "instagram": "#homegym #hometraining #homeworkout #homegymlife #womenwhотrain #femfit #garageгym #homegymsetup #workoutathome #fitnessmotivation",
        "tiktok": "#homegym #hometraining #homeworkout #femfit #homegymlife"
    },
    "Train For You": {
        "instagram": "#trainforYOU #womensfitness #selfcare #mindsetmatters #femfit #strongwomen #fitnessjourney #workoitmotivation #mentalhealthfitness #strongnotskinny",
        "tiktok": "#trainforyou #womensfitness #femfit #strongwomen #mindset"
    }
}