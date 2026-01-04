# 📚 User Manual

This manual walks you through every part of the Trading Settings Learning Lab.

1️⃣ Home Page

Purpose
A welcoming dashboard that introduces the student to the platform.

What you’ll find
Project title and description

Student profile card

Quick navigation guidance

A snapshot of current settings

A tip for first‑time learners

Recommended first step
Start with Learning Lab to understand each setting before entering the Simulation Arena.

2️⃣ Learning Lab
Purpose
To explore and understand how different trading settings affect behavior and outcomes.

Sections
The Learning Lab is divided into three categories:

🎛 Trading Settings
Show Executions

Beep on Execution

Quick Trade Mode

🏦 Broker Settings
Default Size

Trigger Spread

Stop‑Loss Spread

🧍 Market Profile
Profile Information

Privacy Preferences

Features
Apply preset configurations (Conservative, Moderate, Aggressive)

Read metaphors and explanations

Adjust settings interactively

Reflect on how each setting influences clarity, speed, and emotional load

3️⃣ Trading Settings Page
Each setting includes:

Explain
A clear description, metaphor, and explanation of why the setting matters.

Adjust
Interactive controls to modify the setting.

Learn
Reflection prompts to deepen understanding.

Examples
Space for before/after illustrations or explanations.

4️⃣ Broker Settings Page
Similar structure to Trading Settings, but focused on:

Position sizing

Spread tolerance

Stop‑loss breathing room

These settings directly influence risk and execution quality.

5️⃣ Market Profile Page
Helps students define:

Their trading identity

Their privacy preferences

This page encourages self‑awareness and intentionality.

6️⃣ Simulation Arena
Purpose
The heart of the platform — a safe environment to practice trading with the settings you configured.

Features
Market Controls
Step the market forward (1x, 2x, 5x)

Watch price and spread evolve

Trade Placement
Buy or Sell

Choose size

Orders may be blocked if spread is too high

Automatic stop‑loss calculation

Chart Preview
Price line

Execution markers (open, add, close)

Real‑time updates

Spread Meter
Shows whether conditions are calm, moderate, or noisy.

Emotional Meter
Students record their emotional state during the session.

Risk Summary
Open positions

Realized P&L

Max drawdown (placeholder)

Trade Log
A table of all trades executed in the session.

Reflection Prompts
Triggered by events like:

Spread block

Stop‑loss hit

Opening a position

Closing a position

7️⃣ Badges & Progress
Purpose
To reward awareness, discipline, and reflection — not profit.

Examples of badges:
Spread Whisperer – Recognizing spread behavior

Footprint Finder – Placing trades and studying executions

Pencil First – Keeping Quick Trade Mode off while learning

Badges help students celebrate learning milestones.

8️⃣ Teacher Dashboard
Purpose
A classroom‑friendly analytics panel.

Shows:
Total sessions

Total trades

Total reflections

Spread blocks

Stop‑loss hits

Reflection keyword themes

Bar chart of emotional load

This helps teachers understand class behavior patterns.

9️⃣ Session Summary
Purpose
To help students reflect on each session.

Includes:
Narrative summary

Learning objectives triggered

Trades in the session

Reflections

Emotional load chart

This page turns raw activity into meaningful insight.

🔟 Compare Sessions
Purpose
To help students see how their behavior changes over time.

Features:
Select two sessions

Compare narratives

Identify growth, patterns, or repeated mistakes

🛠 Technical Notes
Requirements
Code
streamlit
pandas
numpy
altair
plotly
scikit-learn
pyyaml
python-dateutil
Run the app
Code
streamlit run app.py
Folder Structure
Code
trading_settings_lab/
│ app.py
│ requirements.txt
│ .gitignore
│
├── pages/
├── components/
├── logic/
├── data/
└── assets/
🎓 Who This Lab Is For
Students learning trading fundamentals

Teachers running workshops

Beginners exploring market mechanics

Anyone wanting to understand how settings influence behavior

Traders practicing emotional awareness

🌱 Educational Philosophy
This lab is built on three pillars:

1. Awareness
Settings shape perception.
Perception shapes decisions.

2. Reflection
Trading is not just numbers — it’s behavior.

3. Experimentation
Safe simulation encourages curiosity without fear
