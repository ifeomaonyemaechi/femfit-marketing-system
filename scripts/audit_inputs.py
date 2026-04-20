# audit_inputs.py
# This file defines the marketing audit framework for FemFit.fit.
# It contains the brand snapshot, channel data, audit criteria,
# and scoring weights used across the entire audit pipeline.
# Every other script in this project imports from this file.

# ── Brand snapshot ───────────────────────────────────────────────────────────
# Current state of FemFit.fit's marketing as of the audit date.
# In a real engagement this data comes from a client intake form
# or direct access to their platforms.

BRAND_SNAPSHOT = {
    "brand_name": "FemFit.fit",
    "founded": "2022",
    "platform": "Shopify",
    "niche": "Women's fitness — gym wear, shoes, home workout equipment",
    "target_customer": "Women aged 24-42 who train at home and in the gym",
    "monthly_revenue_range": "R150,000 — R300,000",
    "team_size": "Founder plus one part-time assistant",
    "audit_date": "April 2026"
}


# ── Channel data ─────────────────────────────────────────────────────────────
# Current performance data for each marketing channel.
# Metrics are realistic estimates for a brand at this stage.

CHANNEL_DATA = {
    "email": {
        "platform": "Klaviyo",
        "list_size": 8400,
        "average_open_rate": 18.2,
        "average_ctr": 1.8,
        "welcome_flow": True,
        "abandoned_cart_flow": True,
        "post_purchase_flow": False,
        "winback_flow": False,
        "browse_abandonment_flow": False,
        "campaigns_per_month": 2,
        "list_growth_rate_monthly": 3.2,
        "revenue_attributed_to_email": 22,
        "segmentation": "Basic — active vs inactive only",
        "ab_testing": False,
        "notes": "Open rate below industry benchmark of 25-30% for fitness DTC. Only 2 of 5 core flows active. No segmentation beyond basic active/inactive split. Campaigns are batch-and-blast with no personalisation."
    },
    "instagram": {
        "followers": 8400,
        "average_engagement_rate": 1.9,
        "posting_frequency": "4-5 times per week",
        "content_mix": {
            "product_posts": 60,
            "lifestyle_posts": 25,
            "educational_posts": 10,
            "user_generated_content": 5
        },
        "reels_percentage": 30,
        "stories_frequency": "3-4 times per week",
        "paid_ads_active": False,
        "instagram_shop_active": True,
        "average_saves_per_post": 12,
        "notes": "Engagement rate of 1.9% is below the 3-6% benchmark for accounts this size. Content is too product-heavy — 60% product posts suppresses organic reach. Reels are underutilised at only 30% of content. No paid ads running despite clear product-market fit signals."
    },
    "tiktok": {
        "followers": 1200,
        "videos_posted": 8,
        "average_views": 340,
        "posting_frequency": "Inconsistent — 1-2 per week at best",
        "content_type": "Product showcases mainly",
        "notes": "TikTok presence is nascent — only 8 videos posted. Average views of 340 suggests algorithm has not picked up the account yet. Content is too polished and product-focused for TikTok's native style. Huge untapped opportunity given the brand's home gym and training content potential."
    },
    "website": {
        "platform": "Shopify",
        "monthly_visitors": 4200,
        "bounce_rate": 68,
        "average_session_duration_minutes": 1.8,
        "conversion_rate": 1.4,
        "email_popup_active": True,
        "email_popup_conversion_rate": 3.1,
        "product_pages_have_reviews": True,
        "blog_active": False,
        "seo_optimised": False,
        "page_speed_score": 71,
        "notes": "Conversion rate of 1.4% is below the 2-4% benchmark for Shopify fashion and fitness brands. Bounce rate of 68% is high — suggests traffic quality or landing page issues. No blog means no organic SEO traffic. Page speed of 71 needs improvement — below 90 impacts both SEO and conversion."
    },
    "sms": {
        "active": False,
        "platform": None,
        "notes": "No SMS marketing active. Klaviyo SMS is available on their current plan. Given the brand's direct and no-nonsense voice, SMS could perform well for flash sales and product launches."
    }
}


# ── Competitor data ──────────────────────────────────────────────────────────
# Three competitors at different scales for comparison.

COMPETITOR_DATA = [
    {
        "name": "Gymshark",
        "type": "Enterprise competitor — aspirational benchmark",
        "instagram_followers": 6800000,
        "email_strategy": "Highly segmented — behavioural triggers, personalisation at scale",
        "content_strategy": "70% community and lifestyle, 30% product",
        "strengths": "Brand community, influencer network, content volume",
        "weaknesses": "Too large to feel personal — FemFit.fit can out-authenticity them",
        "relevance": "Shows where the category leader invests — community over product"
    },
    {
        "name": "Tala",
        "type": "Direct competitor — same positioning, larger scale",
        "instagram_followers": 280000,
        "email_strategy": "Weekly newsletters, strong brand voice, regular flow optimisation",
        "content_strategy": "60% lifestyle and values, 25% product, 15% educational",
        "strengths": "Extremely strong brand voice, sustainability angle, founder visibility",
        "weaknesses": "UK-focused, premium price point limits audience size",
        "relevance": "Closest positioning match — proves the no-nonsense women's fitness brand model works at scale"
    },
    {
        "name": "Adapt Clothing",
        "type": "Emerging competitor — similar stage to FemFit.fit",
        "instagram_followers": 45000,
        "email_strategy": "Basic flows active, monthly campaigns, growing list",
        "content_strategy": "Mix of product, UGC, and training content",
        "strengths": "Strong UGC strategy, good TikTok presence",
        "weaknesses": "Less defined brand voice than FemFit.fit",
        "relevance": "Same stage competitor proving TikTok and UGC drive growth at this scale"
    }
]


# ── Audit framework ──────────────────────────────────────────────────────────
# The criteria used to score each channel and the overall marketing setup.
# Each area is scored out of 10. Weights reflect strategic importance.

AUDIT_FRAMEWORK = {
    "scoring_areas": [
        {
            "area": "Email Marketing",
            "weight": 25,
            "criteria": [
                "Flow coverage — are all 5 core flows active?",
                "Open rate vs industry benchmark",
                "CTR vs industry benchmark",
                "Segmentation sophistication",
                "Campaign frequency and consistency",
                "Revenue attribution"
            ]
        },
        {
            "area": "Social Media",
            "weight": 20,
            "criteria": [
                "Engagement rate vs benchmark",
                "Content mix balance",
                "Posting consistency",
                "Reels and video usage",
                "Platform diversification",
                "Community building activity"
            ]
        },
        {
            "area": "Website and Conversion",
            "weight": 25,
            "criteria": [
                "Conversion rate vs benchmark",
                "Bounce rate",
                "Page speed",
                "SEO foundation",
                "Email capture optimisation",
                "Product page quality"
            ]
        },
        {
            "area": "Brand and Content Strategy",
            "weight": 20,
            "criteria": [
                "Brand voice consistency across channels",
                "Content strategy clarity",
                "Educational content ratio",
                "Brand story visibility",
                "Content repurposing system"
            ]
        },
        {
            "area": "Growth and Acquisition",
            "weight": 10,
            "criteria": [
                "Paid advertising strategy",
                "Organic growth rate",
                "Referral or UGC programme",
                "SMS readiness"
            ]
        }
    ],
    "benchmark_sources": [
        "Klaviyo Email Benchmarks 2025 — Fitness and Activewear",
        "Later Instagram Benchmarks 2025",
        "Shopify Conversion Rate Benchmarks 2025",
        "Littledata Shopify Performance Report 2025"
    ]
}


# ── Priority matrix ──────────────────────────────────────────────────────────
# Used by the strategy report to prioritise recommendations.
# Each recommendation gets an impact score and effort score.
# High impact, low effort = do first.

PRIORITY_LEVELS = {
    "P1": "Do this week — high impact, low effort",
    "P2": "Do this month — high impact, moderate effort",
    "P3": "Do this quarter — high impact, higher effort",
    "P4": "Nice to have — lower impact or very high effort"
}