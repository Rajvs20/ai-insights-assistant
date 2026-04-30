#!/usr/bin/env python3
"""
Generate sample PDF documents for the AI Insights Assistant.

Produces 5 PDF files in data/pdfs/ with realistic entertainment company content
that complements the CSV data and supports the 6 required example questions:
1. Which titles performed best in 2025?
2. Why is Stellar Run trending recently?
3. Compare Dark Orbit vs Last Kingdom
4. Which city had the strongest engagement last month?
5. What explains weak comedy performance?
6. What recommendations would you give for leadership?

Requires: fpdf2 (pip install fpdf2)
"""

import os

from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")


class ReportPDF(FPDF):
    """Custom PDF class with consistent header/footer styling."""

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_title = title

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "StreamVision Entertainment - CONFIDENTIAL", align="L")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_title_page(self, subtitle: str = ""):
        self.add_page()
        self.ln(40)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(30, 60, 120)
        self.multi_cell(0, 14, self.report_title, align="C")
        if subtitle:
            self.ln(8)
            self.set_font("Helvetica", "", 14)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 8, subtitle, align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "StreamVision Entertainment Inc.", align="C")
        self.ln(6)
        self.cell(0, 8, "Internal Use Only", align="C")

    def section_heading(self, text: str):
        self.ln(6)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 10, text)
        self.ln(4)
        self.set_draw_color(30, 60, 120)
        self.line(10, self.get_y(), 100, self.get_y())
        self.ln(6)

    def sub_heading(self, text: str):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, text)
        self.ln(6)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def bullet_point(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)


# ---------------------------------------------------------------------------
# 1. Quarterly Executive Report
# ---------------------------------------------------------------------------

def generate_quarterly_executive_report():
    pdf = ReportPDF("Q1 2025 Quarterly Executive Report")
    pdf.alias_nb_pages()
    pdf.add_title_page("January - March 2025")

    # Executive Summary
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Q1 2025 has been a landmark quarter for StreamVision Entertainment. "
        "Total platform revenue reached $1.62 billion, representing a 23% increase "
        "year-over-year. Subscriber growth accelerated with 4.2 million net new "
        "subscribers, bringing our total active subscriber base to 38.7 million globally. "
        "Content engagement metrics showed significant improvement across all tiers, "
        "with average watch time per subscriber increasing by 18 minutes per week."
    )
    pdf.body_text(
        "The quarter was anchored by three standout titles: Stellar Run, Neon Horizon, "
        "and The Last Ember. Stellar Run, our flagship Sci-Fi release, generated $420 million "
        "in revenue against a $95 million production budget, delivering a 4.4x return on "
        "investment. Neon Horizon followed with $380 million in revenue, while The Last Ember "
        "surprised with $310 million on a modest $45 million budget, making it the most "
        "cost-efficient title of the quarter."
    )

    # Overall Performance
    pdf.section_heading("2. Overall Performance Metrics")
    pdf.sub_heading("2.1 Revenue Overview")
    pdf.body_text(
        "Total Q1 2025 revenue: $1.62 billion (vs. $1.32 billion in Q1 2024). "
        "Subscription revenue accounted for 62% of total revenue ($1.00 billion), "
        "while content licensing and advertising contributed 24% and 14% respectively. "
        "Operating margin improved to 18.5%, up from 15.2% in the prior year quarter."
    )
    pdf.sub_heading("2.2 Subscriber Metrics")
    pdf.body_text(
        "Net new subscribers: 4.2 million (Q1 2024: 3.1 million). "
        "Churn rate decreased to 3.8% from 4.5% in Q4 2024. "
        "Premium tier adoption increased to 28% of total subscribers, up from 22%. "
        "VIP tier showed the strongest growth at 45% quarter-over-quarter, driven by "
        "exclusive early access to Stellar Run and The Last Ember."
    )

    # Revenue Trends
    pdf.section_heading("3. Revenue Trends and Analysis")
    pdf.body_text(
        "Monthly revenue trajectory showed consistent growth throughout Q1: "
        "January delivered $480 million, February reached $520 million, and March "
        "closed at $620 million. The March spike was driven primarily by the release "
        "of The Last Ember on March 10 and sustained viewership of Stellar Run, which "
        "continued to attract new viewers three months after its January 15 premiere."
    )
    pdf.body_text(
        "Revenue per subscriber (ARPU) increased to $41.86 from $38.24 in Q4 2024. "
        "This improvement was driven by higher Premium and VIP tier adoption, as well as "
        "increased advertising revenue from our ad-supported Free tier, which saw a 32% "
        "increase in ad impressions."
    )

    # Top Titles
    pdf.add_page()
    pdf.section_heading("4. Top Performing Titles")
    pdf.sub_heading("4.1 Stellar Run (Sci-Fi)")
    pdf.body_text(
        "Stellar Run has emerged as the defining title of Q1 2025. Released on January 15, "
        "the film achieved 28 million unique viewers within its first 30 days, setting a new "
        "platform record. Key performance indicators include: revenue of $420 million, "
        "average viewer rating of 8.7/10, completion rate of 85%, and social media mentions "
        "exceeding 2.3 million across platforms. The film's success is attributed to its "
        "innovative visual effects, strong word-of-mouth, and a highly effective multi-channel "
        "marketing campaign that included influencer partnerships and viral social media content."
    )
    pdf.sub_heading("4.2 Neon Horizon (Action)")
    pdf.body_text(
        "Neon Horizon, released February 20, delivered strong performance with $380 million "
        "in revenue. The action title attracted a broad demographic, with particularly strong "
        "engagement among 18-34 year olds. Viewer rating averaged 8.2/10 with a 78% completion "
        "rate. The film benefited from a $110 million production budget that delivered "
        "blockbuster-quality action sequences."
    )
    pdf.sub_heading("4.3 The Last Ember (Drama)")
    pdf.body_text(
        "The Last Ember stands out as the quarter's most efficient performer. With a production "
        "budget of just $45 million, the drama generated $310 million in revenue, a remarkable "
        "6.9x return on investment. Director Elena Ruiz delivered a critically acclaimed "
        "performance piece that resonated deeply with audiences, achieving the highest viewer "
        "rating of the quarter at 8.9/10. The film's success demonstrates the continued "
        "appetite for high-quality dramatic content on our platform."
    )

    # Genre Performance
    pdf.section_heading("5. Genre Performance Breakdown")
    pdf.body_text(
        "Genre analysis reveals clear winners and areas requiring strategic attention:"
    )
    pdf.bullet_point(
        "Sci-Fi: Strongest genre with $770 million combined revenue. Stellar Run and "
        "Echoes of Tomorrow drove exceptional performance. Viewer engagement metrics "
        "consistently exceeded platform averages by 35%."
    )
    pdf.bullet_point(
        "Action: Second strongest at $670 million. Neon Horizon and Velocity anchored "
        "the category. Action titles showed the broadest demographic appeal."
    )
    pdf.bullet_point(
        "Drama: $540 million in revenue with the highest average viewer ratings (8.5/10). "
        "The Last Ember and The Verdict demonstrated that quality drama commands premium "
        "engagement and strong word-of-mouth."
    )
    pdf.bullet_point(
        "Animation: $280 million with strong family audience engagement. Dreamscape "
        "performed well with an 8.1 rating. The genre shows growth potential."
    )
    pdf.bullet_point(
        "Comedy: Underperforming at $59 million combined revenue. Average ratings of 5.2/10 "
        "indicate quality issues. Titles like Laugh Track, Funny Business, and Joke's On You "
        "failed to connect with audiences. Comedy completion rates averaged just 45%, "
        "significantly below the platform average of 68%. This genre requires a strategic "
        "overhaul in content development and talent acquisition."
    )
    pdf.bullet_point(
        "Horror: Moderate performance at $168 million. Niche but loyal audience base."
    )
    pdf.bullet_point(
        "Romance: Steady at $150 million. Midnight Bloom performed adequately but the "
        "genre lacks a breakout title."
    )

    # Strategic Priorities
    pdf.add_page()
    pdf.section_heading("6. Strategic Priorities for Q2 2025")
    pdf.body_text(
        "Based on Q1 performance analysis, the executive team has identified the following "
        "strategic priorities for Q2 2025:"
    )
    pdf.bullet_point(
        "Double down on Sci-Fi and Action content: These genres deliver the highest ROI "
        "and broadest audience appeal. Increase Q2 content investment by 20% in these categories."
    )
    pdf.bullet_point(
        "Restructure Comedy strategy: Commission an external review of our comedy development "
        "pipeline. Consider partnerships with established comedy creators and invest in "
        "audience testing before greenlighting new comedy projects."
    )
    pdf.bullet_point(
        "Expand international markets: London and Mumbai showed strong engagement growth. "
        "Allocate additional marketing budget to these regions."
    )
    pdf.bullet_point(
        "Leverage Stellar Run momentum: Develop franchise opportunities including a sequel, "
        "behind-the-scenes content, and merchandise partnerships."
    )
    pdf.bullet_point(
        "Improve Premium tier conversion: Target Free and Basic tier subscribers with "
        "personalized upgrade offers tied to upcoming exclusive content."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "quarterly_executive_report.pdf")
    pdf.output(filepath)
    print(f"  Generated -> {filepath}")


# ---------------------------------------------------------------------------
# 2. Campaign Performance Summary
# ---------------------------------------------------------------------------

def generate_campaign_performance_summary():
    pdf = ReportPDF("Campaign Performance Summary")
    pdf.alias_nb_pages()
    pdf.add_title_page("Marketing Analysis - Q1 2025")

    # Overview
    pdf.add_page()
    pdf.section_heading("1. Campaign Overview")
    pdf.body_text(
        "This report provides a comprehensive analysis of StreamVision Entertainment's "
        "marketing campaigns during Q1 2025. Total marketing expenditure for the quarter "
        "was $48.3 million across 120+ individual campaigns spanning seven primary channels. "
        "Overall campaign ROI averaged 8.2x, a significant improvement over Q4 2024's 6.1x."
    )
    pdf.body_text(
        "The marketing team executed campaigns across Social Media, Television, Search Ads, "
        "Email Marketing, Influencer Partnerships, Display Advertising, and Streaming Ads. "
        "Each channel demonstrated varying levels of effectiveness, with Social Media and "
        "Influencer channels delivering the strongest returns."
    )

    # Channel ROI Analysis
    pdf.section_heading("2. Channel ROI Analysis")
    pdf.sub_heading("2.1 Social Media")
    pdf.body_text(
        "Social Media campaigns delivered the highest ROI at 12.4x return on spend. "
        "Total spend: $8.2 million. Total attributed revenue: $101.7 million. "
        "Key metrics: 245 million impressions, 14.7 million clicks (6.0% CTR), "
        "and 1.1 million conversions. Social media was particularly effective for "
        "Stellar Run, where viral TikTok content and Twitter discussions drove "
        "organic amplification that exceeded paid reach by 3x."
    )
    pdf.sub_heading("2.2 Television")
    pdf.body_text(
        "TV campaigns provided broad reach but lower efficiency with a 5.8x ROI. "
        "Total spend: $12.5 million. Total attributed revenue: $72.5 million. "
        "TV was most effective for Neon Horizon's launch campaign, reaching 85 million "
        "households during prime-time slots. However, attribution remains challenging "
        "and the true impact may be higher than measured."
    )
    pdf.sub_heading("2.3 Influencer Partnerships")
    pdf.body_text(
        "Influencer campaigns achieved a 10.8x ROI, the second-highest channel. "
        "Total spend: $5.4 million. Total attributed revenue: $58.3 million. "
        "Stellar Run's influencer campaign was the standout, with 45 creators across "
        "YouTube, Instagram, and TikTok generating 180 million combined views. "
        "The authenticity of influencer endorsements drove higher conversion rates "
        "(8.2%) compared to traditional advertising (3.1%)."
    )
    pdf.sub_heading("2.4 Search Ads")
    pdf.body_text(
        "Search advertising delivered a solid 7.5x ROI. Total spend: $6.8 million. "
        "Total attributed revenue: $51.0 million. Search campaigns were most effective "
        "during the first two weeks following a title's release, capturing high-intent "
        "audiences actively seeking information about new content."
    )
    pdf.sub_heading("2.5 Email Marketing")
    pdf.body_text(
        "Email campaigns achieved a 9.2x ROI with the lowest cost per conversion. "
        "Total spend: $2.1 million. Total attributed revenue: $19.3 million. "
        "Personalized recommendation emails drove the highest open rates (34%) and "
        "click-through rates (8.5%). Segmented campaigns targeting lapsed subscribers "
        "re-activated 120,000 accounts during the quarter."
    )
    pdf.sub_heading("2.6 Display Ads")
    pdf.body_text(
        "Display advertising showed moderate performance with a 4.2x ROI. "
        "Total spend: $7.3 million. Total attributed revenue: $30.7 million. "
        "Programmatic display was effective for awareness but showed lower "
        "conversion rates compared to other digital channels."
    )
    pdf.sub_heading("2.7 Streaming Ads")
    pdf.body_text(
        "Streaming platform ads delivered a 6.5x ROI. Total spend: $6.0 million. "
        "Total attributed revenue: $39.0 million. Pre-roll and mid-roll ads on "
        "partner streaming platforms effectively reached cord-cutter demographics."
    )

    # Top Campaigns
    pdf.add_page()
    pdf.section_heading("3. Top Performing Campaigns")
    pdf.sub_heading("3.1 Stellar Run Launch Campaign")
    pdf.body_text(
        "The Stellar Run multi-channel launch campaign was the quarter's most successful "
        "initiative. Total campaign spend: $12.8 million across Social Media ($3.2M), "
        "Influencer ($2.8M), TV ($3.5M), Search ($1.8M), and Streaming Ads ($1.5M). "
        "The campaign generated 420 million total impressions and directly attributed "
        "to 8.5 million new viewer sign-ups. The Social Media component featured a "
        "'#StellarRunChallenge' that generated 45 million user-created videos."
    )
    pdf.sub_heading("3.2 Stellar Run Sustained Reach Campaign")
    pdf.body_text(
        "Following the successful launch, a sustained reach campaign maintained momentum "
        "through February and March. Spend: $4.2 million. This campaign focused on "
        "retargeting viewers who watched the trailer but hadn't yet viewed the film, "
        "achieving a 15% conversion rate. The campaign also promoted behind-the-scenes "
        "content that kept Stellar Run in social media conversations."
    )
    pdf.sub_heading("3.3 Neon Horizon Opening Weekend Blitz")
    pdf.body_text(
        "Neon Horizon's concentrated opening weekend campaign spent $8.5 million in a "
        "10-day window. The blitz strategy generated 180 million impressions and drove "
        "6.2 million first-week viewers. TV spots during major sporting events provided "
        "the broadest reach, while social media drove the highest engagement."
    )
    pdf.sub_heading("3.4 The Last Ember Word-of-Mouth Campaign")
    pdf.body_text(
        "The Last Ember took a different approach with a modest $3.8 million campaign "
        "focused on critical acclaim and word-of-mouth. Early screening events for "
        "influencers and critics generated organic buzz that amplified paid efforts. "
        "The campaign achieved a 14.2x ROI, the highest of any individual campaign."
    )

    # Budget Allocation Recommendations
    pdf.section_heading("4. Budget Allocation Recommendations")
    pdf.body_text(
        "Based on Q1 performance data, the marketing team recommends the following "
        "budget allocation adjustments for Q2 2025:"
    )
    pdf.bullet_point(
        "Increase Social Media allocation by 25%: Highest ROI channel with proven "
        "ability to drive viral organic reach. Recommended Q2 budget: $10.3 million."
    )
    pdf.bullet_point(
        "Increase Influencer budget by 30%: Second-highest ROI with strong conversion "
        "rates. Expand creator partnerships beyond entertainment to lifestyle and tech "
        "influencers. Recommended Q2 budget: $7.0 million."
    )
    pdf.bullet_point(
        "Maintain TV spend with better targeting: Shift from broad reach to targeted "
        "placements during high-affinity programming. Recommended Q2 budget: $12.0 million."
    )
    pdf.bullet_point(
        "Reduce Display Ads allocation by 15%: Lowest digital ROI. Redirect budget to "
        "higher-performing channels. Recommended Q2 budget: $6.2 million."
    )
    pdf.bullet_point(
        "Invest in Email personalization: Upgrade recommendation engine for email "
        "campaigns. Low cost, high ROI channel deserves infrastructure investment. "
        "Recommended Q2 budget: $2.5 million."
    )
    pdf.bullet_point(
        "Allocate dedicated comedy marketing budget: If comedy content strategy is "
        "restructured, allocate $3 million for targeted comedy audience acquisition "
        "campaigns to rebuild the genre's subscriber base."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "campaign_performance_summary.pdf")
    pdf.output(filepath)
    print(f"  Generated -> {filepath}")


# ---------------------------------------------------------------------------
# 3. Content Roadmap
# ---------------------------------------------------------------------------

def generate_content_roadmap():
    pdf = ReportPDF("2025 Content Strategy Roadmap")
    pdf.alias_nb_pages()
    pdf.add_title_page("Content Planning and Investment Strategy")

    # Strategic Vision
    pdf.add_page()
    pdf.section_heading("1. Strategic Vision")
    pdf.body_text(
        "StreamVision Entertainment's 2025 content strategy is built on three pillars: "
        "doubling down on proven high-ROI genres, strategically restructuring underperforming "
        "categories, and expanding our international content portfolio. Our goal is to reach "
        "45 million subscribers by year-end while improving content efficiency metrics across "
        "all genres."
    )
    pdf.body_text(
        "The strategy is informed by comprehensive analysis of Q1 2025 performance data, "
        "audience behavior research, competitive landscape assessment, and emerging market "
        "trends. Key decisions include significant increases in Sci-Fi and Animation investment, "
        "a measured reduction in Comedy spending pending quality improvements, and new "
        "partnership models for international co-productions."
    )

    # Upcoming Releases
    pdf.section_heading("2. Upcoming Releases - Q2/Q3 2025")
    pdf.sub_heading("2.1 Tentpole Releases")
    pdf.body_text(
        "Phantom Menace II (Sci-Fi, July 4): Our biggest Q3 release with a $140 million "
        "budget. Director Sophia Lin returns after the success of Galactic Drift. Early "
        "test screenings show exceptional audience scores (92% positive). Marketing campaign "
        "will launch May 15 with a $18 million multi-channel push."
    )
    pdf.body_text(
        "Turbo Charge (Action, June 1): Marcus Webb directs this $100 million action "
        "spectacle. The film targets the 18-34 demographic with high-octane sequences "
        "and a diverse ensemble cast. Pre-release social media buzz is strong."
    )
    pdf.body_text(
        "Toy Galaxy (Animation, June 15): David Park's latest animated feature has a "
        "$85 million budget and targets family audiences. Early reviews from animation "
        "festivals have been overwhelmingly positive (8.3 average rating from critics)."
    )
    pdf.sub_heading("2.2 Mid-Tier Releases")
    pdf.body_text(
        "Orbit Station (Sci-Fi, May 28): A $115 million Sci-Fi thriller that expands "
        "our presence in the space exploration sub-genre. Rapid Fire (Action, May 15): "
        "A $78 million action film from James Carter. Ocean Deep (Thriller, April 25): "
        "A $60 million underwater thriller from Marcus Webb. Mind Games (Thriller, June 10): "
        "A $48 million psychological thriller from Sophia Lin."
    )
    pdf.sub_heading("2.3 Targeted Releases")
    pdf.body_text(
        "Wanderlust (Romance, April 12): A $22 million romantic drama targeting the "
        "25-44 female demographic. Nightmare Lane (Horror, April 18): A $12 million "
        "horror entry for our dedicated horror audience segment."
    )

    # Genre Investment Plans
    pdf.add_page()
    pdf.section_heading("3. Genre Investment Plans")
    pdf.sub_heading("3.1 Sci-Fi - INCREASE Investment (+35%)")
    pdf.body_text(
        "Sci-Fi has proven to be our highest-performing genre with consistent audience "
        "engagement and premium subscriber conversion. Q1 2025 Sci-Fi titles averaged "
        "an 8.2 rating and 4.1x ROI. We will increase Sci-Fi content investment from "
        "$320 million to $432 million annually. This includes greenlighting two additional "
        "original Sci-Fi series and one franchise expansion (Stellar Run sequel)."
    )
    pdf.sub_heading("3.2 Animation - INCREASE Investment (+25%)")
    pdf.body_text(
        "Animation delivers strong family audience engagement and has the longest content "
        "shelf life on our platform. Titles like Pixel World and Dreamscape continue to "
        "generate views months after release. We will increase Animation investment from "
        "$250 million to $312 million, focusing on original IP development and international "
        "co-productions with studios in Japan and France."
    )
    pdf.sub_heading("3.3 Action - MAINTAIN Investment")
    pdf.body_text(
        "Action remains our second-strongest genre and will maintain its current investment "
        "level of $380 million. Focus will shift toward diverse action sub-genres (heist, "
        "martial arts, espionage) to broaden audience appeal beyond the traditional "
        "action demographic."
    )
    pdf.sub_heading("3.4 Drama - MAINTAIN Investment")
    pdf.body_text(
        "Drama investment stays at $180 million. The genre's strength lies in critical "
        "acclaim and awards potential, which drives brand prestige and Premium tier "
        "subscriptions. The Last Ember's success validates our approach of backing "
        "visionary directors with modest budgets."
    )
    pdf.sub_heading("3.5 Comedy - REDUCE Investment (-40%)")
    pdf.body_text(
        "Comedy investment will be reduced from $120 million to $72 million pending a "
        "comprehensive quality review. Q1 comedy titles averaged a 5.2 rating with "
        "completion rates 23 percentage points below the platform average. Rather than "
        "producing more comedy content, we will focus on fewer, higher-quality projects. "
        "Key actions include: hiring a dedicated comedy development executive, establishing "
        "partnerships with proven comedy showrunners, implementing mandatory audience "
        "testing before production greenlight, and exploring comedy-drama hybrid formats "
        "that have shown stronger performance on competing platforms."
    )
    pdf.sub_heading("3.6 Thriller - SLIGHT INCREASE (+10%)")
    pdf.body_text(
        "Thriller investment increases from $200 million to $220 million. The genre "
        "shows consistent mid-tier performance with loyal audiences. Focus on psychological "
        "thrillers and limited series formats."
    )
    pdf.sub_heading("3.7 Horror - MAINTAIN Investment")
    pdf.body_text(
        "Horror maintains its $60 million investment level. The genre delivers reliable "
        "returns with low production costs and a dedicated audience segment."
    )
    pdf.sub_heading("3.8 Romance - SLIGHT DECREASE (-10%)")
    pdf.body_text(
        "Romance investment decreases from $100 million to $90 million. The genre lacks "
        "a breakout title and will benefit from a quality-over-quantity approach."
    )

    # Partnership Opportunities
    pdf.add_page()
    pdf.section_heading("4. Partnership Opportunities")
    pdf.sub_heading("4.1 International Co-Productions")
    pdf.body_text(
        "We are in advanced discussions with three international studios for co-production "
        "agreements: Toho Studios (Japan) for anime-inspired Sci-Fi content, Gaumont (France) "
        "for premium drama series, and Yash Raj Films (India) for Bollywood-crossover action "
        "titles. These partnerships will provide access to new talent pools and international "
        "audiences while sharing production costs."
    )
    pdf.sub_heading("4.2 Technology Partnerships")
    pdf.body_text(
        "A partnership with NVIDIA for AI-assisted visual effects is expected to reduce "
        "post-production costs by 15-20% while maintaining quality. Additionally, a deal "
        "with Dolby for exclusive Atmos content will differentiate our Premium tier offering."
    )
    pdf.sub_heading("4.3 Talent Development")
    pdf.body_text(
        "The StreamVision Emerging Creators Program will invest $15 million in discovering "
        "and developing new directorial talent. The program specifically targets diverse "
        "voices in Sci-Fi, Animation, and Drama, our three highest-growth genres."
    )

    # Content Calendar Summary
    pdf.section_heading("5. 2025 Content Calendar Summary")
    pdf.body_text(
        "Full-year 2025 content plan includes 52 original titles across all genres: "
        "12 Sci-Fi (up from 8), 10 Action (unchanged), 8 Drama (unchanged), "
        "8 Animation (up from 6), 4 Comedy (down from 8), 5 Thriller (up from 4), "
        "3 Horror (unchanged), and 2 Romance (down from 3). Total content investment: "
        "$1.57 billion, a 12% increase over 2024."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "content_roadmap.pdf")
    pdf.output(filepath)
    print(f"  Generated -> {filepath}")


# ---------------------------------------------------------------------------
# 4. Policy Guidelines
# ---------------------------------------------------------------------------

def generate_policy_guidelines():
    pdf = ReportPDF("Internal Policy Guidelines")
    pdf.alias_nb_pages()
    pdf.add_title_page("Data Handling, Privacy, and Security Standards\nEffective January 1, 2025")

    # Data Handling Policies
    pdf.add_page()
    pdf.section_heading("1. Data Handling Policies")
    pdf.sub_heading("1.1 Data Classification")
    pdf.body_text(
        "All data within StreamVision Entertainment is classified into four tiers: "
        "Public (marketing materials, press releases), Internal (operational reports, "
        "performance metrics), Confidential (subscriber data, financial projections, "
        "content strategies), and Restricted (authentication credentials, encryption keys, "
        "personally identifiable information). Each tier has specific handling requirements "
        "that must be followed by all employees and contractors."
    )
    pdf.sub_heading("1.2 Data Access Controls")
    pdf.body_text(
        "Access to data is governed by the principle of least privilege. Employees are "
        "granted access only to the data necessary for their role. All data access requests "
        "must be approved by the data owner and the Information Security team. Access reviews "
        "are conducted quarterly, and unused access is revoked within 30 days of the review."
    )
    pdf.sub_heading("1.3 Data Retention and Disposal")
    pdf.body_text(
        "Viewer activity data is retained for 24 months for analytics purposes and then "
        "anonymized. Financial records are retained for 7 years per regulatory requirements. "
        "Marketing campaign data is retained for 36 months. All data disposal must follow "
        "the approved destruction procedures: digital data must be cryptographically erased, "
        "and physical media must be physically destroyed."
    )
    pdf.sub_heading("1.4 Data Transfer Policies")
    pdf.body_text(
        "All data transfers between systems must use encrypted channels (TLS 1.3 minimum). "
        "Cross-border data transfers must comply with applicable data protection regulations "
        "(GDPR, CCPA, PIPEDA). No Confidential or Restricted data may be transferred to "
        "personal devices or unauthorized cloud services."
    )

    # Privacy Guidelines
    pdf.section_heading("2. Privacy Guidelines")
    pdf.sub_heading("2.1 Subscriber Privacy")
    pdf.body_text(
        "StreamVision is committed to protecting subscriber privacy. All subscriber data "
        "collection must have a clear business purpose and legal basis. Subscribers must be "
        "informed about data collection through our privacy notice, and consent must be "
        "obtained where required. Subscriber viewing history is considered Confidential data "
        "and must not be shared externally without explicit subscriber consent."
    )
    pdf.sub_heading("2.2 Analytics and Reporting")
    pdf.body_text(
        "Internal analytics reports must use aggregated data whenever possible. Reports "
        "containing individual subscriber data must be marked as Confidential and distributed "
        "only to authorized personnel. The AI Insights Assistant system accesses data through "
        "controlled tool interfaces and never exposes raw database connections or file paths "
        "to the AI model. All queries are logged for audit purposes."
    )
    pdf.sub_heading("2.3 Third-Party Data Sharing")
    pdf.body_text(
        "Data sharing with third parties (advertising partners, analytics providers, "
        "content licensors) must be governed by a Data Processing Agreement (DPA). "
        "Only anonymized or aggregated data may be shared unless the subscriber has "
        "provided explicit consent. All third-party data recipients must demonstrate "
        "adequate security controls."
    )

    # Content Moderation Standards
    pdf.add_page()
    pdf.section_heading("3. Content Moderation Standards")
    pdf.sub_heading("3.1 Content Rating System")
    pdf.body_text(
        "All content on the StreamVision platform must be rated according to our internal "
        "content rating system, which aligns with industry standards (MPAA, BBFC). Ratings "
        "must be assigned before content is made available to subscribers. Content ratings "
        "determine parental control restrictions and advertising eligibility."
    )
    pdf.sub_heading("3.2 User-Generated Content")
    pdf.body_text(
        "User reviews and ratings are subject to automated moderation for profanity, "
        "hate speech, and spam. Reviews flagged by the automated system are queued for "
        "human review within 24 hours. Users who repeatedly violate content guidelines "
        "may have their review privileges suspended."
    )
    pdf.sub_heading("3.3 Content Removal Procedures")
    pdf.body_text(
        "Content may be removed from the platform if it violates licensing agreements, "
        "contains unauthorized material, or receives valid legal takedown requests. "
        "All removal decisions must be documented and approved by the Legal team. "
        "Subscribers affected by content removal must be notified within 48 hours."
    )

    # Security Protocols
    pdf.section_heading("4. Security Protocols")
    pdf.sub_heading("4.1 Authentication and Authorization")
    pdf.body_text(
        "All internal systems require multi-factor authentication (MFA). API access "
        "uses JWT tokens with a maximum validity of 24 hours. Service-to-service "
        "communication uses mutual TLS authentication. Password requirements: minimum "
        "12 characters, must include uppercase, lowercase, numbers, and special characters. "
        "Passwords must be rotated every 90 days."
    )
    pdf.sub_heading("4.2 API Security")
    pdf.body_text(
        "All API endpoints must implement rate limiting to prevent abuse. Input validation "
        "must be performed on all user-supplied data before processing. SQL queries must "
        "use parameterized statements to prevent injection attacks. Error responses must "
        "not expose internal system details, database schemas, or file paths."
    )
    pdf.sub_heading("4.3 Incident Response")
    pdf.body_text(
        "Security incidents must be reported to the Security Operations Center (SOC) "
        "within 1 hour of detection. The incident response team will classify incidents "
        "as Critical (data breach, system compromise), High (unauthorized access attempt, "
        "vulnerability exploitation), Medium (policy violation, suspicious activity), or "
        "Low (failed login attempts, minor policy deviations). Critical and High incidents "
        "require executive notification within 4 hours."
    )
    pdf.sub_heading("4.4 Audit and Compliance")
    pdf.body_text(
        "All system access and data queries are logged with timestamps, user identifiers, "
        "and correlation IDs. Audit logs are retained for 12 months and reviewed monthly "
        "by the compliance team. Annual penetration testing is conducted by an independent "
        "security firm. SOC 2 Type II compliance is maintained and audited annually."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "policy_guidelines.pdf")
    pdf.output(filepath)
    print(f"  Generated -> {filepath}")


# ---------------------------------------------------------------------------
# 5. Audience Behavior Report
# ---------------------------------------------------------------------------

def generate_audience_behavior_report():
    pdf = ReportPDF("Audience Behavior Report")
    pdf.alias_nb_pages()
    pdf.add_title_page("Viewer Demographics, Engagement, and Insights\nQ1 2025 Analysis")

    # Viewer Demographics
    pdf.add_page()
    pdf.section_heading("1. Viewer Demographics")
    pdf.sub_heading("1.1 Age Distribution")
    pdf.body_text(
        "Our subscriber base spans a wide age range with the following distribution: "
        "16-24 years: 22% of subscribers, 25-34 years: 31% (largest segment), "
        "35-44 years: 24%, 45-54 years: 14%, 55+: 9%. The 25-34 segment shows the "
        "highest engagement per capita with an average of 12.3 hours of weekly viewing. "
        "The 16-24 segment has the highest growth rate at 28% year-over-year, driven "
        "primarily by Sci-Fi and Animation content."
    )
    pdf.sub_heading("1.2 Gender Distribution")
    pdf.body_text(
        "Subscriber gender distribution: Male 48%, Female 46%, Non-binary 6%. "
        "Genre preferences show notable variation: Action and Sci-Fi skew 60% male, "
        "Romance and Drama skew 58% female, while Animation and Comedy show the most "
        "balanced gender distribution. Non-binary subscribers show the highest engagement "
        "with Sci-Fi content (35% above average)."
    )
    pdf.sub_heading("1.3 Geographic Distribution")
    pdf.body_text(
        "Our subscriber base is distributed across 15 major metropolitan areas. "
        "The top 5 markets by subscriber count are: New York (4.8 million), "
        "Los Angeles (3.9 million), London (3.2 million), Mumbai (2.8 million), "
        "and Chicago (2.4 million). International markets (London, Toronto, Sydney, "
        "Mumbai, Tokyo) collectively represent 38% of total subscribers, up from 31% "
        "in Q1 2024."
    )

    # Engagement Patterns by Region
    pdf.section_heading("2. Engagement Patterns by Region")
    pdf.sub_heading("2.1 Regional Engagement Rankings")
    pdf.body_text(
        "Regional engagement analysis for Q1 2025 reveals significant variation across "
        "markets. Engagement is measured as a composite score combining average watch time, "
        "completion rate, review activity, and subscription tier distribution."
    )
    pdf.body_text(
        "Top engagement markets (ranked by composite engagement score):"
    )
    pdf.bullet_point(
        "New York: Engagement score 92/100 (STRONGEST). Average weekly watch time: "
        "14.2 hours. Completion rate: 78%. Premium/VIP tier: 42% of subscribers. "
        "New York leads in every engagement metric and shows the highest concentration "
        "of VIP subscribers. The market responds strongly to Drama and Sci-Fi content."
    )
    pdf.bullet_point(
        "London: Engagement score 86/100. Average weekly watch time: 13.1 hours. "
        "Completion rate: 74%. Premium/VIP tier: 38%. London shows particularly strong "
        "engagement with Drama and Thriller content. International content performs "
        "exceptionally well in this market."
    )
    pdf.bullet_point(
        "Mumbai: Engagement score 82/100. Average weekly watch time: 12.8 hours. "
        "Completion rate: 71%. Premium/VIP tier: 30%. Mumbai is our fastest-growing "
        "market with 45% subscriber growth year-over-year. Action and Drama genres "
        "dominate viewing patterns."
    )
    pdf.bullet_point(
        "Los Angeles: Engagement score 80/100. Average weekly watch time: 12.5 hours. "
        "Completion rate: 72%. Premium/VIP tier: 35%. LA shows strong engagement across "
        "all genres with particular strength in Action and Animation."
    )
    pdf.bullet_point(
        "Austin: Engagement score 78/100. Average weekly watch time: 12.1 hours. "
        "Completion rate: 70%. Premium/VIP tier: 33%. Austin punches above its weight "
        "relative to market size, with strong Sci-Fi and Thriller engagement."
    )
    pdf.body_text(
        "Lower engagement markets include Phoenix (score: 58), San Antonio (score: 52), "
        "and Philadelphia (score: 55). These markets show higher Free tier concentration "
        "and lower completion rates, suggesting opportunities for targeted engagement campaigns."
    )

    # Device Preferences
    pdf.add_page()
    pdf.section_heading("3. Device Preferences")
    pdf.body_text(
        "Viewing device distribution across the platform shows evolving consumption patterns:"
    )
    pdf.bullet_point(
        "Smart TV: 38% of total viewing hours (up from 32% in Q1 2024). Smart TV viewers "
        "have the highest completion rates (82%) and longest average session duration "
        "(2.1 hours). This is the preferred device for Premium and VIP subscribers."
    )
    pdf.bullet_point(
        "Mobile: 28% of total viewing hours. Mobile viewing peaks during commute hours "
        "(7-9 AM, 5-7 PM) and lunch breaks. Average session duration: 45 minutes. "
        "Mobile viewers show the highest engagement with short-form content and trailers."
    )
    pdf.bullet_point(
        "Desktop: 18% of total viewing hours. Desktop viewing is concentrated during "
        "work hours (suggesting background viewing) and late evening. Average session "
        "duration: 1.4 hours."
    )
    pdf.bullet_point(
        "Tablet: 10% of total viewing hours. Tablet usage peaks on weekends and shows "
        "strong correlation with family content (Animation, Comedy). Average session "
        "duration: 1.6 hours."
    )
    pdf.bullet_point(
        "Gaming Console: 6% of total viewing hours. Console viewers skew heavily male "
        "(72%) and 18-34 (68%). Strong preference for Action and Sci-Fi content. "
        "Average session duration: 1.8 hours."
    )

    # Subscription Tier Analysis
    pdf.section_heading("4. Subscription Tier Analysis")
    pdf.sub_heading("4.1 Tier Distribution")
    pdf.body_text(
        "Current subscriber tier distribution: Free: 25% (9.7 million), Basic: 32% "
        "(12.4 million), Premium: 28% (10.8 million), VIP: 15% (5.8 million). "
        "The Premium and VIP tiers have grown significantly, with VIP showing 45% "
        "quarter-over-quarter growth driven by exclusive early access to Stellar Run "
        "and The Last Ember."
    )
    pdf.sub_heading("4.2 Tier Behavior Patterns")
    pdf.body_text(
        "Free tier subscribers average 4.2 hours of weekly viewing with a 45% completion "
        "rate. They primarily watch older catalog content and are most responsive to "
        "ad-supported recommendations. Basic tier subscribers average 7.8 hours weekly "
        "with a 62% completion rate. They engage with a mix of new and catalog content. "
        "Premium subscribers average 11.5 hours weekly with a 76% completion rate and "
        "are the most active reviewers. VIP subscribers average 15.2 hours weekly with "
        "an 85% completion rate and show the highest engagement with new releases."
    )
    pdf.sub_heading("4.3 Upgrade Triggers")
    pdf.body_text(
        "Analysis of tier upgrades reveals key triggers: 42% of Free-to-Basic upgrades "
        "occur within 48 hours of a tentpole release. 35% of Basic-to-Premium upgrades "
        "are triggered by exclusive content announcements. 28% of Premium-to-VIP upgrades "
        "are driven by early access features. Personalized upgrade offers sent via email "
        "have a 12% conversion rate, 3x higher than generic promotions."
    )

    # Audience Segment Insights
    pdf.add_page()
    pdf.section_heading("5. Audience Segment Insights")
    pdf.sub_heading("5.1 Power Viewers")
    pdf.body_text(
        "Power Viewers (top 10% by watch time) account for 35% of total platform viewing "
        "hours. This segment averages 22 hours of weekly viewing, maintains a 91% completion "
        "rate, and contributes 28% of all reviews. 78% are Premium or VIP subscribers. "
        "They are the earliest adopters of new content and serve as organic amplifiers "
        "through social media sharing and word-of-mouth."
    )
    pdf.sub_heading("5.2 Weekend Warriors")
    pdf.body_text(
        "Weekend Warriors (25% of subscribers) concentrate 70% of their viewing on "
        "Friday-Sunday. They prefer longer content (films over 120 minutes) and show "
        "strong engagement with Action and Drama genres. This segment has the highest "
        "Smart TV usage (52%) and often watches with family members."
    )
    pdf.sub_heading("5.3 Commuter Viewers")
    pdf.body_text(
        "Commuter Viewers (18% of subscribers) primarily watch on mobile devices during "
        "transit hours. They prefer content under 30 minutes or use the 'continue watching' "
        "feature for longer content. This segment shows the highest engagement with "
        "trailers and short-form promotional content, making them valuable for new "
        "release awareness campaigns."
    )
    pdf.sub_heading("5.4 Genre Loyalists")
    pdf.body_text(
        "Genre Loyalists (20% of subscribers) watch 80%+ of their content within a single "
        "genre. The largest loyalist groups are Sci-Fi (32% of loyalists), Action (25%), "
        "and Horror (18%). These subscribers have the lowest churn rate (2.1%) but are "
        "difficult to cross-sell into other genres. Personalized recommendations within "
        "their preferred genre maintain engagement."
    )
    pdf.sub_heading("5.5 Casual Browsers")
    pdf.body_text(
        "Casual Browsers (27% of subscribers) watch less than 3 hours per week and have "
        "the highest churn risk (8.2% monthly). They are predominantly Free tier (62%) "
        "and show no strong genre preference. Targeted engagement campaigns with "
        "personalized content recommendations have shown a 15% reduction in churn "
        "for this segment in pilot programs."
    )

    # Recommendations
    pdf.section_heading("6. Recommendations")
    pdf.body_text(
        "Based on the audience behavior analysis, we recommend the following actions:"
    )
    pdf.bullet_point(
        "Invest in New York market activation: As our strongest engagement market, "
        "New York should receive priority for live events, early screenings, and "
        "localized marketing campaigns."
    )
    pdf.bullet_point(
        "Accelerate Mumbai growth: The fastest-growing market deserves increased "
        "content localization and regional partnership investment."
    )
    pdf.bullet_point(
        "Launch Smart TV experience upgrade: With 38% of viewing on Smart TVs and "
        "the highest completion rates, investing in the Smart TV app experience will "
        "have the broadest positive impact."
    )
    pdf.bullet_point(
        "Implement personalized tier upgrade journeys: Use viewing behavior triggers "
        "to deliver timely, relevant upgrade offers to Free and Basic subscribers."
    )
    pdf.bullet_point(
        "Develop Casual Browser retention program: Targeted content recommendations "
        "and engagement nudges to reduce churn in this high-risk segment."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "audience_behavior_report.pdf")
    pdf.output(filepath)
    print(f"  Generated -> {filepath}")


# ---------------------------------------------------------------------------
# Main: generate all PDF documents
# ---------------------------------------------------------------------------

def main():
    print("Generating sample PDF documents...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    generate_quarterly_executive_report()
    generate_campaign_performance_summary()
    generate_content_roadmap()
    generate_policy_guidelines()
    generate_audience_behavior_report()

    print(f"\nDone! All PDF documents generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
