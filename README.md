# Asana RL Seed Data Simulation

This repository contains code and documentation for generating a realistic, enterprise-grade Asana workspace simulation. The generated dataset is intended to serve as high-quality seed data for reinforcement learning (RL) environments that evaluate computer-use AI agents operating within project management tools.

---

## Overview

The simulation represents a mid-to-large B2B SaaS company with approximately **7,500 employees** using Asana for **Engineering, Marketing, and Operations** workflows.  
The dataset spans approximately **six months of historical activity** and models realistic organizational structure, task lifecycles, collaboration patterns, and metadata usage.

The primary goal is to avoid synthetic shortcuts and produce data that closely resembles real-world Asana usage, enabling meaningful evaluation and fine-tuning of RL agents.

---

## Simulated Asana Entities

The dataset includes the following core Asana entities:

- Organizations / Workspaces  
- Teams and Team Memberships  
- Users  
- Projects and Sections  
- Tasks and Subtasks  
- Comments (task discussions)  
- Custom Field Definitions and Values  
- Tags and Task–Tag Associations  

All entities are connected through a fully relational schema with enforced referential integrity.

---

## Project Structure

asana-rl-seed-data/
├── src/
|
│ ├── main.py # Entry point for data generation
|
│ ├── generators/ # Entity-specific data generators
|
│ │ ├── organizations.py
|
│ │ ├── teams.py
|
│ │ ├── users.py
|
│ │ ├── team_memberships.py
|
│ │ ├── projects.py
|
│ │ ├── sections.py
|
│ │ ├── tasks.py
|
│ │ ├── comments.py
|
│ │ ├── custom_fields.py
|
│ │ └── tags.py
|
│ ├── utils/ # Shared utilities
|
│ │ ├── db.py
|
│ │ ├── dates.py
|
│ │ └── random_utils.py
|
├── prompts/ # LLM prompt templates (optional)
|
├── output/ # Generated SQLite database (local only)
|
├── schema.sql # SQLite schema (DDL)
|
├── requirements.txt # Python dependencies
|
├── .env.example # Example environment variables
|
└── README.md


---

## Setup Instructions

### 1. (Optional) Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Run the Data Generation Pipeline
bash
Copy code
python src/main.py
Output
After successful execution, the generated SQLite database will be available at:

bash
Copy code
output/asana_simulation.sqlite
This database contains all simulated entities and relationships as described in the documentation.

Configuration
Dataset scale, date ranges, and generation parameters (e.g., number of users, projects, tasks) are configurable through environment variables and configuration logic within the codebase.
An example environment configuration file is provided in .env.example.

Notes
The codebase is designed to be modular and extensible.

Data generation prioritizes realism over volume.

Temporal and relational consistency is enforced throughout the dataset.

LLM usage (if enabled) is limited to text generation for task names, descriptions, and comments.

License
This project is intended for evaluation and research purposes only.
