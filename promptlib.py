# -*- coding: utf-8 -*-
"""
Created on MON Jun 23 09:55:20 2025

@author: LKohl
"""

from flask import Flask, render_template_string, request, redirect, url_for
from markupsafe import Markup, escape
import re

app = Flask(__name__)

# Default prompts
prompt_library = {
    "Writing": [
        "Write a blog post about the future of AI.",
        "Write a professional email to a member on the marketing team."
    ],
    "Generation": [
        "Generate an image of xyz.",
        "Generate ideas on how to maximize reach for social media posts."
    ],
    "Video": [
        "Script a 30-second product demo video for a new product.",
        "Create a narration for a 2-minute animated video explaing a new product."
    ]
}

# Track user-submitted prompts as (category, prompt) tuples
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
    <ul style="line-height: 1.8;">
        <li><strong>Be Specific:</strong> Tell the model exactly what you want it to do.</li>
        <li><strong>Give Context:</strong> Include background or examples if needed.</li>
        <li><strong>Use Constraints:</strong> Limit output length, format, or style.</li>
        <li><strong>Guide the Tone:</strong> Want formal, friendly, concise, humorous?</li>
        <li><strong>Iterate:</strong> Try and refine based on results.</li>
    </ul>
    <p>Example:</p>
    <code>“Write a 3-sentence summary of this article in a humorous tone.”</code>
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