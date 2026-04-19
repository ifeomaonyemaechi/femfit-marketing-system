# Skill: Run Channel Audit
# FemFit.fit Marketing Operations System

## WHAT THIS SKILL DOES
Runs a structured audit on a single marketing channel for
FemFit.fit. Scores performance against benchmarks, identifies
the top 3 issues, and produces quick wins plus strategic
recommendations. Called by the marketing-auditor agent.

## WHEN TO USE THIS SKILL
Use when:
- A full 5-channel audit is requested
- A single channel needs a deep dive
- Monthly performance review is due
- A channel score has dropped and needs diagnosis

## SUPPORTED CHANNELS
- email
- instagram
- tiktok
- website
- sms

## BENCHMARKS BY CHANNEL

### EMAIL
Open rate: 25-30%
CTR: 2.5-3%
Active flows: 5 of 5
Revenue attribution: 30-35% of total

### INSTAGRAM
Engagement rate: 3-6% (under 10K followers)
Saves per post: 25-40
Reels percentage: 60%+
Product post ratio: maximum 30%
UGC content: 15-20%

### TIKTOK
Weekly posts: 5-7
Average views: 1,800+
Total videos at 3 months: 40+
Content style: lifestyle and authentic (not product-focused)

### WEBSITE
Conversion rate: 2.4%
Bounce rate: 45%
Page speed score: 90+
Email popup capture rate: 3-5%

### SMS
List size: 500+ subscribers
Revenue: 8-15% of email revenue
Opt-in rate: 5-8%
Active flows: welcome + abandoned cart minimum

## SCORING GUIDE
10: Benchmark exceeded, best-in-class execution
8-9: At or near benchmark, minor optimisations only
6-7: Below benchmark, specific fixes needed this month
4-5: Significantly underperforming, priority action required
1-3: Critical failure, immediate intervention needed

## EXECUTION INSTRUCTIONS
1. Confirm which channel is being audited
2. Request current performance data from brief
3. Compare each metric against benchmark
4. Identify top 3 issues with specific data evidence
5. Calculate revenue impact for each issue
6. Write 2 quick wins (actionable this week)
7. Write 3 strategic recommendations (this quarter)
8. Generate benchmark comparison table
9. Assign channel score out of 10
10. Save to outputs/FEMFIT_AUDIT_[CHANNEL]_[YYYYMMDD].md

## QUALITY GATES
Before saving output, confirm:
[ ] Every issue includes specific data (not vague observations)
[ ] Every issue includes revenue impact in rands
[ ] Quick wins can be executed in under 4 hours each
[ ] Strategic recommendations include success metrics
[ ] Benchmark comparison table is complete
[ ] Score is justified by the data, not estimated

## OUTPUT STRUCTURE
CHANNEL AUDIT — FemFit.fit
===========================
Channel: [channel name]
Audit date: [date]
Data period: [period covered]

CHANNEL SCORE: [X]/10

PERFORMANCE SUMMARY:
[2-3 sentences with specific numbers vs benchmarks]

TOP 3 ISSUES:
1. [Issue name]
   Data: [specific metric vs benchmark]
   Revenue impact: R[amount] monthly / R[amount] annually

2. [Issue name]
   Data: [specific metric vs benchmark]
   Revenue impact: R[amount] monthly / R[amount] annually

3. [Issue name]
   Data: [specific metric vs benchmark]
   Revenue impact: R[amount] monthly / R[amount] annually

QUICK WINS (This Week):
1. [Action] — Time required: [X hours] — Owner: [Founder/Assistant]
2. [Action] — Time required: [X hours] — Owner: [Founder/Assistant]

STRATEGIC RECOMMENDATIONS (This Quarter):
1. [Action] — Success metric: [specific target]
2. [Action] — Success metric: [specific target]
3. [Action] — Success metric: [specific target]

BENCHMARK COMPARISON:
| Metric | FemFit.fit | Benchmark | Gap |
|--------|-----------|-----------|-----|
| [metric] | [current] | [target] | [difference] |

## METRICS TO LOG
- Channel audited
- Score out of 10
- Time to complete
- Number of issues found
- Total revenue impact identified