# lead_profiles.py
# This file defines the ideal client profile for AIMarketer.co
# and contains a database of simulated leads — realistic Shopify DTC
# brands that match the target customer criteria.
# Every other script in this project imports from this file.

# ── Ideal Client Profile ─────────────────────────────────────────────────────
# This defines exactly who AIMarketer.co is targeting.
# Used by the lead researcher to score and qualify each lead.

IDEAL_CLIENT_PROFILE = {
    "business_type": "Shopify DTC brand",
    "industries": [
        "fitness and activewear",
        "beauty and skincare",
        "wellness and supplements",
        "home and lifestyle",
        "sustainable fashion"
    ],
    "revenue_signals": [
        "Active paid advertising (Meta or Google ads visible)",
        "1,000 to 50,000 Instagram followers",
        "Has an email list (Klaviyo or Mailchimp signup visible on site)",
        "Shopify store with 10 or more products",
        "Regular posting cadence — at least 3 times per week"
    ],
    "pain_point_signals": [
        "Inconsistent posting schedule — gaps of 5 or more days visible",
        "Generic captions with no clear brand voice",
        "No welcome email or delayed welcome sequence",
        "Low engagement relative to follower count",
        "Mixed tone across different platforms",
        "Promotional posts with no educational or brand content",
        "No re-engagement or post-purchase email flows visible"
    ],
    "disqualifiers": [
        "Enterprise brands with in-house marketing teams",
        "Brands with over 100,000 followers — likely already resourced",
        "Service businesses — not product-based",
        "Brands that have posted nothing in the last 30 days"
    ],
    "ideal_budget_signal": "Spending on ads suggests marketing budget exists",
    "decision_maker": "Founder, co-founder, or head of marketing"
}


# ── Lead database ────────────────────────────────────────────────────────────
# 6 realistic simulated leads across different niches.
# Each lead has enough detail for Claude to generate personalised outreach.
# Fields mirror what you would find in a real prospecting tool like Apollo.

LEADS = [
    {
        "id": "LEAD001",
        "brand_name": "RootGlow Skincare",
        "founder_name": "Priya Nair",
        "role": "Founder and CEO",
        "website": "rootglowskincare.com",
        "industry": "Beauty and skincare",
        "product_focus": "Natural skincare for women of colour — serums, oils, and SPF",
        "shopify": True,
        "instagram_followers": 8400,
        "instagram_handle": "@rootglowskincare",
        "email_platform": "Klaviyo",
        "posting_frequency": "4-5 times per week",
        "pain_points_observed": [
            "Captions are very generic — no consistent brand voice",
            "No pinned welcome post or brand story content",
            "Email signup on site but no welcome sequence visible",
            "Promotional posts far outnumber educational content"
        ],
        "recent_activity": "Just launched a new SPF50 facial oil — announced on Instagram 3 days ago",
        "tone_of_current_content": "Friendly but inconsistent — some posts sound corporate, others very casual",
        "qualification_score": None,
        "qualified": None
    },
    {
        "id": "LEAD002",
        "brand_name": "StrongForm Co",
        "founder_name": "Marcus Webb",
        "role": "Co-founder",
        "website": "strongformco.com",
        "industry": "Fitness and activewear",
        "product_focus": "Functional gym wear for men — lifting shorts, compression tops, belts",
        "shopify": True,
        "instagram_followers": 14200,
        "instagram_handle": "@strongformco",
        "email_platform": "Mailchimp",
        "posting_frequency": "2-3 times per week",
        "pain_points_observed": [
            "Posting inconsistently — 3 posts in last 2 weeks then nothing for 6 days",
            "No re-engagement or winback emails visible",
            "Strong product photography but weak copy across all platforms",
            "No post-purchase email sequence — only transactional receipts"
        ],
        "recent_activity": "Running a Meta ad for their new lifting belt — ad copy is very generic",
        "tone_of_current_content": "Tries to be motivational but uses too many clichés",
        "qualification_score": None,
        "qualified": None
    },
    {
        "id": "LEAD003",
        "brand_name": "Bloom & Ritual",
        "founder_name": "Sophie Alderton",
        "role": "Founder",
        "website": "bloomandritual.com",
        "industry": "Wellness and supplements",
        "product_focus": "Women's wellness supplements — adaptogens, sleep support, cycle care",
        "shopify": True,
        "instagram_followers": 3100,
        "instagram_handle": "@bloomandritual",
        "email_platform": "Klaviyo",
        "posting_frequency": "Daily",
        "pain_points_observed": [
            "Posts daily but engagement is very low relative to follower count",
            "Content is all promotional — no education or community building",
            "Welcome email exists but is a single generic confirmation",
            "No segmentation visible — same email to entire list"
        ],
        "recent_activity": "Recently started a TikTok account — only 3 videos posted so far",
        "tone_of_current_content": "Warm and soft but lacks authority and specificity",
        "qualification_score": None,
        "qualified": None
    },
    {
        "id": "LEAD004",
        "brand_name": "Haus of Linen",
        "founder_name": "Amara Osei",
        "role": "Founder and Creative Director",
        "website": "hausoflinen.com",
        "industry": "Sustainable fashion",
        "product_focus": "Sustainable linen clothing — dresses, sets, and loungewear",
        "shopify": True,
        "instagram_followers": 22600,
        "instagram_handle": "@hausoflinen",
        "email_platform": "Klaviyo",
        "posting_frequency": "3-4 times per week",
        "pain_points_observed": [
            "Beautiful visual content but captions are thin — one or two lines only",
            "No email flows beyond order confirmation visible",
            "Brand story is strong on About page but never referenced in content",
            "Seasonal campaigns but no lifecycle email strategy"
        ],
        "recent_activity": "Just released a summer collection — launch was a single Instagram post",
        "tone_of_current_content": "Minimal and aesthetic but does not convert — no CTAs in captions",
        "qualification_score": None,
        "qualified": None
    },
    {
        "id": "LEAD005",
        "brand_name": "Vivace Nutrition",
        "founder_name": "Daniel Ferreira",
        "role": "CEO",
        "website": "vivacenutrition.com",
        "industry": "Wellness and supplements",
        "product_focus": "Sports nutrition for everyday athletes — protein, pre-workout, recovery",
        "shopify": True,
        "instagram_followers": 31000,
        "instagram_handle": "@vivacenutrition",
        "email_platform": "Klaviyo",
        "posting_frequency": "5-6 times per week",
        "pain_points_observed": [
            "High follower count but engagement has dropped noticeably in last 60 days",
            "No re-engagement campaign visible despite clear list decay signals",
            "Email campaigns are batch-and-blast — no segmentation or personalisation",
            "Content is repetitive — product shots and discount codes dominate"
        ],
        "recent_activity": "Sent a discount code email to full list last week — no segmentation",
        "tone_of_current_content": "High energy and enthusiastic but generic — sounds like every other supplement brand",
        "qualification_score": None,
        "qualified": None
    },
    {
        "id": "LEAD006",
        "brand_name": "Canopy Home",
        "founder_name": "Yuki Tanaka",
        "role": "Founder",
        "website": "canopyhome.co",
        "industry": "Home and lifestyle",
        "product_focus": "Minimalist home organisation and storage products",
        "shopify": True,
        "instagram_followers": 6800,
        "instagram_handle": "@canopyhome",
        "email_platform": "Mailchimp",
        "posting_frequency": "2-3 times per week",
        "pain_points_observed": [
            "Posts have strong aesthetics but no brand voice in captions",
            "No email marketing beyond abandoned cart — no newsletter visible",
            "Product descriptions on site are functional but not brand-consistent",
            "No content strategy visible — posts seem reactive not planned"
        ],
        "recent_activity": "Featured in a home organisation blog post last month — did not leverage it in content",
        "tone_of_current_content": "Clean and minimal visually but silent in terms of brand communication",
        "qualification_score": None,
        "qualified": None
    }
]


# ── Qualification scoring criteria ───────────────────────────────────────────
# Used by the lead researcher to calculate a score for each lead.
# Each criterion is worth a set number of points.
# Maximum possible score is 100.

SCORING_CRITERIA = {
    "uses_shopify": 15,
    "has_email_platform": 20,
    "follower_range_1k_to_50k": 15,
    "posts_regularly": 10,
    "has_pain_points": 25,
    "recent_activity_detected": 15
}

QUALIFICATION_THRESHOLD = 70