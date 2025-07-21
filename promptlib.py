"""
Created on MON Jun 23 0:55:20 2025

@author: LKohl
"""

from flask import Flask, render_template_string, request, redirect, url_for
from markupsafe import Markup, escape
import re

app = Flask(__name__)

prompt_library = {
    "Chat GPT": [
        "List [number] blog post ideas about [topic] that incldue [key themes or keywords].",
        "Outline a long blog post (1500+ words) on [topic] targeted at [audience].",
        "Write a blog introduction paragraph for a post about [product or topic] in a [specific tone] tone.",
        "Summarize this [article or blog] into a brief paragraph.",
        "Write a how-to blog on resolving [problem] featuring the [product].",
        "Give [number] catchy blog titles about [topic] that would do well on the website.",
        "Generate a description using [number] characters for this blog. [insert blog link]",
        "Turn this webinar topic into [number] blog post titles.",
        "Write a product comparison post outline for [product] vs [product].",
        "Create a [number]-day social media content plan for [product] on [platforms].",
        "Write [number] instagram captions about [product]",
        "Suggest LinkedIn content ideas that would grab more attention of [audience] using [product].",
        "What trending hashtags should we use for a post about [topic] on [platform]?",
        "Write a LinkedIn post promoting our laste blog post [insert blog link].",
        "Write a [duration]-second script for an ad about [product and description].",
        "List [number] promotion ideas for our [event] targeting [audience].",
        "Suggest variations of our ad headline to make it more click-worthy: '[Insert headline]'",
        "Generate a full-funnel marketing campaign plan for [product], including awareness, consideration, and conversion stages.",
        "Write re-targeting ad copy for users who viewed [product] but chose another solution.",
        "List ideas for ad creative that visually communicates [key product benefit].",
        "Write [number] subject lines for a welcome email sequence for [product].",
        "Draft the body of a promotional email for [product] that emphasizes [benefit].",
        "Structure a [number]-email re-engagement sequence for dormant users of [product].",
        "Write a launch announcement email for [product] aimed at [audience] that includes [key words].",
        "You're an email expert. Write a copy for a weekly newsletter about [specific topic].",
        "Write an A/B test variation of this subject line: [subject line]. Suggest why it might perform better.",
        "List [number] ways to segment the email list for [product category].",
        "Create a follow-up email for [event] attendees to try [product].",
        "What are the top [number] KPIs for a [type] campaign. Explain how to track them.",
        "Write a summary of marketing performance if the click-through rate increased by [number]%.",
        "Explain how to use certain parameters to track campaign performance in Google Analytics.",
        "List ways to improve ROI for underperforming campagins in [channel].",
        "What insights can be gained from comparing Q1 and Q2 ad spends?"
    ],    
    "Copilot": [
        "Summarize this marketing strategy document [attach file] into [number] key priorities.",
        "Write an executive summary of the Q[quarter number] reort [attach file] for senior leadership.",
        "Extract KPIs from this report [attach Excel or Word file] and highlight areas of concern.",
        "List major takeaways from this competitive analysis [attach file] in [number] bullet points.",
        "Convert this internal roadmap [attach file] into a presentation outline.",
        "Summarize this brainstorming doc [attach file] into [number] clear action items.",
        "Write a [length] paper explaining the pain points of this [campaign name] plan. [attach file]",
        "Draft a memo summarizing this meeting transcript [attach file] and include next steps.",
        "Create a bulleted summary of our top [number] campaigns from this report [attach file].",
        "Outline the core messaging strategy form this document [attach brand guide].",
        "Analyze performance from this Excel file [attach file] and summarize the impressions and conversions by channel.",
        "Compare performance from Q[quarter number] to Q[quarter number] using this file. [Attach file]",
        "Create visual charts showing growth in leads over the past [number] months. [attach Excel file]",
        "Summarize customer behavior data from this file [attach Excel file] and make 3 actionable suggestions.",
        "Highlight underperforming ads from this report [attach file] with possible causes.",
        "Create a slide summarizing the key takeaways from this analytics dashboard export. [insert dashboard export]",
        "Extract open and click rates from this email report and compart to benchmarks. [attach file]",
        "Summarize pain points and needs from these interview notes [attach file].",
        "Generate customer quotes from this feedback form [attach form] to use in social media posts.",
        "Extract demographic data from this survey [attach file] and format as a table.",
        "Summarize how customer preferences have changed over time using this data [attach Excel file].",
        "Draft a marketing update email to the company using this report [attach file].",
        "Convert this internal marketing deck [attach PowerPoint] into client-facing language.",
        "Turn this report [attach file] into a press release draft announcing the results.",
        "Create a team briefing document using the top points from this presentation [attach file].",
        "Create a summary email to partners based on this campaign performance deck. [attach file]",
        "Turn this big blog post [attach file] into an email newsletter and [number] social media posts.",
        "Summarize this paper into a [number] page overview for prospects.",
        "Write [number] ad headlines and descriptions on this product spec sheet [attach file].",
        "Repurpose this survey report [attach file] into a refreshed strategy for [new audience].",
        "Rewrite this email template [attach file] to match the company's brand voice aimed towards [purpose and tone]."
        "Summarize the last [number] unread emails in my inbox. Highligh anything urgent or time-sensitive.",
        "Group eamils from [person/team] this week and summarize key topics that are discussed.",
        "Identify which emails in my inbox from the past [number] days are action items or require responses.",
        "Draft responses to these [number] emails marked unread. Use a [specific tone] tone.",
        "Summarize this email thread and suggest a response that acknowledges all key points.",
        "Rank my last [number] emails by importance based on sender, subject, and content.",
        "Summarize all email mentions of [project/campaign name] from the past [number] days into a bullet-point update.",
        "Find any follow-up tasks or deadlines mentioned in emails this week and list them with corresponding due dates.",
        "Write a thank-you email to [name] based on this thread, acknowledging their input on [topic]."
    ],
    "Jasper": [
        "Write a product description for [product] that highlights its top 3 benefits to [audience].",
        "Create a blog introduction for a post about [topic] using a conversational tone.",
        "Generate [number] potential blog titles for a post targeting [industry] professionals about [pain point or trend].",
        "Summarize this blog post [copy link] ito a one-paragraph email teaser.",
        "Turn this list of bullet points [insert] into a polished, engaging paragraph.",
        "Create an FAQ section for the website about [product] using friendly, helpful language.",
        "Write a launch announcement for [product] in a tone that is confidnet but doesn't sound too much like a sales pitch.",
        "Generate three ad copy variations of this promotion [insert] using urgency, curiosity, and emotional appeal.",
        "Turn this technical paragraph [insert] into simpler language a first-time customer would understand."
        "Write a thank-you message to customers after a successful campaign, mentioning [result/impact].",
        "Turn these campaign insights [insert] into a concise marketing recap.",
        "Create messaging that compares the product to a competitor, focusing on its unique advantages.",
        "Write a short campaign blurb that can be reused across emails, ads, and socials for [event/product].",
        "Summarize this blog into a [number]-slide carousel format. Include title suggestions and bullet points for each slide.",
        "Draft a post announcing [event, product, report] in a way that encourages engagement and sharing.",
    ],
    "Claude": [
        "Brainstorm 10 unique marketing angles for [product] that appeal to [audience].",
        "Compare the pros and cons of a product-led vs sales-led launch strategy for [product].",
        "Analyze the messaging on the website homepage and suggest how it could be clearer or more compelling.",
        "Outline a launch strategy for a digital prodcut targeting [niche audience] with a low marketing budget.",
        "What are some potential challenges we could face in launching [campaign type] and how can each be planned for?",
        "Write a detailed outline about [industry trend] for a B2B audience.",
        "Expand this outline [insert] into a full-length blog that explains [technical concept] in simple terms for [audience].",
        "Create a guide that walks through how [persona] can use [product] to solve [specific need].",
        "Look at the current value proposition: [insert]. Suggest improvements based on clarity, differentiation, and tone.",
        "Evaluate brand messaging: [insert] for consistency with overall voice and audience fit.",
        "Review this marketing strategy [insert] and identify any gaps or assumptions.",
        "Identify conflicting and unclear language in this cmpaign [insert] and suggest alternatives.",
        "Summarize this email [insert] into a more concise version without losing the message.",
        "Turn this dense technical copy [insert] into a version that would resonate with non-experts."
    ]
}

user_prompts = []

html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Prompt Library</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: white;
        }
        header {
            background-color: #4F4F4F;
            padding: 20px;
            text-align: center;
        }
        header h1 {
            color: #ccdd37;
            margin: 0;
            font-size: 36px;
        }
        .container {
            padding: 40px;
            max-width: 800px;
            margin: auto;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            margin: 20px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        .btn {
            padding: 10px 20px;
            background-color: #ccdd37;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        .category {
            margin-top: 30px;
        }
        .category h2 {
            color: #001F3F;
        }
        .prompt {
            background: #f0f0f0;
            padding: 10px 15px;
            margin: 5px 0;
            border-left: 4px solid #ccdd37;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<header>
    <h1>AI Prompt Library</h1>
    <img src="/static/matthews.png" alt="Company Logo" style="height:50px; vertical-align: middle; margin-top: 10px;">
</header>

<div class="container">
    <div style="margin-bottom: 20px;">
        <a href="/?mode=search" class="btn" style="background-color: {% if mode == 'search' %}#ccdd37{% else %}#ccc{% endif %}; margin-right: 10px;">Prompt Finder</a>
        <a href="/?mode=browse" class="btn" style="background-color: {% if mode == 'browse' %}#ccdd37{% else %}#ccc{% endif %}; margin-right: 10px;">Search by Category</a>
        <a href="/?mode=create" class="btn" style="background-color: {% if mode == 'create' %}#ccdd37{% else %}#ccc{% endif %}; margin-right: 10px;">Creating a Prompt</a>
        <a href="/?mode=submit" class="btn" style="background-color: {% if mode == 'submit' %}#ccdd37{% else %}#ccc{% endif %}; margin-right: 10px;">Submit Prompt</a>
    </div>

    {% if mode == 'search' %}
    <h2>Search Prompts</h2>
    <form method="POST">
        <input type="text" name="search_term" value="{{ search_term }}" placeholder="Search prompts..." required>
        <button class="btn" type="submit">Search</button>
    </form>

    {% if search_term %}
        <h3>Results for "{{ search_term }}"</h3>
        {% if filtered_prompts %}
            {% for category, prompts in filtered_prompts.items() %}
                <div class="category">{{ category }}</div>
                {% for prompt in prompts %}
                    <div class="prompt">{{ prompt|safe }}</div>
                {% endfor %}
            {% endfor %}
        {% else %}
            <p>No prompts found.</p>
        {% endif %}
    {% endif %}

    {% elif mode == 'browse' %}
    <h2>All Prompts</h2>
    {% if filtered_prompts %}
    <div class="prompt" style="background-color: #e7f0c3; font-weight: bold;">
        You are a [role/expert]. Create a [format: blog, email, etc.]  
        Target: [audience role and industry]  
        Goal: [lead gen, awareness, conversion]  
        Key details: [benefits, differentiators, CTA]  
        Tone: [professional, confident, concise]  
        Framework: [optional, like AIDA or PAS]
    </div>    
    {% for category, prompts in filtered_prompts.items() %}
            <div class="category"><h2>{{ category }}</h2></div>
            {% for prompt in prompts %}
                <div class="prompt">
                    {{ prompt }}
                    {% if (category, prompt) in user_prompts %}
                    <form method="POST" action="{{ url_for('delete_prompt') }}" style="display:inline;">
                        <input type="hidden" name="category" value="{{ category }}">
                        <input type="hidden" name="prompt" value="{{ prompt }}">
                        <button class="btn" type="submit" style="background-color: red; margin-left: 10px;" onclick="return confirm('Delete this prompt?');">Delete</button>
                    </form>
                    {% endif %}
                </div>
            {% endfor %}
        {% endfor %}
    {% else %}
        <p>No prompts available.</p>
    {% endif %}

    {% elif mode == 'submit' %}
    <h2>Submit a New Prompt</h2>
    <form method="POST">
        <label for="new_prompt">Prompt:</label><br>
        <input type="text" id="new_prompt" name="new_prompt" placeholder="Enter your prompt here" required><br><br>

        <label for="category">Category:</label><br>
        <select id="category" name="category" required>
            {% for cat in prompt_library.keys() %}
                <option value="{{ cat }}">{{ cat }}</option>
            {% endfor %}
        </select><br><br>

        <button class="btn" type="submit">Add Prompt</button>
    </form>

    {% elif mode == 'create' %}
    <h2>How to Create a Prompt</h2>
    <ul>
        <li><strong>Prompt Template:</strong> You are a [role/expert]. Create a [format: blog, email, etc.] Target: [audience role and industry] Goal: [lead gen, awareness, conversion] Key details: [benefits, differentiators, CTA] Tone: [professional, confident, concise] Framework: [optional, like AIDA or PAS]</li><br>
        <li><strong>Define the goal:</strong> Know the purpose—lead gen, awareness, SEO, etc.</li><br>
        <li><strong>Clarify the audience:</strong> Include role, industry, pain points, and tone preferences.</li><br>
        <li><strong>Provide product/offer context:</strong> Include benefits, differentiators, and CTAs.</li><br>
        <li><strong>Specify format and tone:</strong> E.g., blog post, bullet list, carousel, casual/professional.</li><br>
        <li><strong>Use role-based prompting:</strong> Assign a persona like “You are a senior B2B copywriter.”</li><br>
        <li><strong>Tell AI what to avoid:</strong> Help keep it on-brand and concise.</li><br>
        <li><strong>Use frameworks:</strong> Add AIDA, PAS, StoryBrand, or similar to enhance structure.</li><br>
        <li><strong>Use the C.R.A.F.T. structure:</strong> Context, Role, Action, Format, Target Audience for detailed, powerful prompts.</li><br>
        <li><strong>Iterate like a dialogue:</strong> Refine responses just like a real conversation.</li><br>
        <li><strong>Prompt the prompter:</strong> Ask AI to ask you questions and help refine your initial idea into a detailed prompt.</li><br>
    </ul>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/delete', methods=['POST'])
def delete_prompt():
    category = request.form.get('category')
    prompt = request.form.get('prompt')

    if (category, prompt) in user_prompts:
        if category in prompt_library and prompt in prompt_library[category]:
            prompt_library[category].remove(prompt)
            user_prompts.remove((category, prompt))
            if not prompt_library[category]:
                del prompt_library[category]
    return redirect(url_for('home', mode='browse'))

@app.route('/', methods=['GET', 'POST'])
def home():
    mode = request.args.get('mode', 'search')
    search_term = ''
    filtered_prompts = {}

    if mode == 'submit' and request.method == 'POST':
        new_prompt = request.form.get('new_prompt', '').strip()
        category = request.form.get('category', '').strip()
        if new_prompt and category:
            prompt_library.setdefault(category, []).append(new_prompt)
            user_prompts.append((category, new_prompt))
        return render_template_string(
            html,
            filtered_prompts=prompt_library,
            search_term='',
            mode='browse',
            prompt_library=prompt_library,
            user_prompts=user_prompts
        )

    elif mode == 'search' and request.method == 'POST':
        search_term = request.form.get('search_term', '').strip().lower()
        keywords = search_term.split()
        for category, prompts in prompt_library.items():
            matches = []
            for prompt in prompts:
                lower_prompt = prompt.lower()
                if all(keyword in lower_prompt for keyword in keywords):
                    highlighted = escape(prompt)
                    for kw in keywords:
                        pattern = re.compile(re.escape(kw), re.IGNORECASE)
                        highlighted = pattern.sub(
                            lambda m: f"<span style='background-color:#ccdd37'>{m.group(0)}</span>",
                            highlighted
                        )
                    matches.append(Markup(highlighted))
            if matches:
                filtered_prompts[category] = matches

    elif mode == 'browse':
        filtered_prompts = prompt_library

    return render_template_string(
        html,
        filtered_prompts=filtered_prompts,
        search_term=search_term,
        mode=mode,
        prompt_library=prompt_library,
        user_prompts=user_prompts
    )

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)