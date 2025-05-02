pip freeze > requirements.txt
pip install -r requirements.txt
playwright install
python -m backend.database.create_tables
python -m backend.scraper.fetcher
uvicorn backend.api.server:app --reload

# Student Results Analyzer

A web application for analyzing and comparing student academic performance.

## Deployment Guide

### Prerequisites

- A GitHub account
- A Railway.app account

### Step 1: Prepare Repository

1. Push your code to GitHub if you haven't already:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app/)
2. Sign up/Login with your GitHub account
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Railway will automatically detect your Python application

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard
2. Click "New"
3. Select "Database"
4. Choose "PostgreSQL"
5. Railway will automatically add the database and provide connection details

### Step 4: Environment Variables

Railway will automatically set up:

- `DATABASE_URL`: Connection string for your PostgreSQL database
- `PORT`: The port your application will run on

### Step 5: Verify Deployment

1. Railway will automatically build and deploy your application
2. Once complete, click on your deployment to see the deployment URL
3. Your application should now be live!

## Local Development

1. Clone the repository

```bash
git clone <your-github-repo-url>
```

2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your local database credentials
```

3. Install dependencies

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
playwright install
python -m backend.database.create_tables
python -m backend.scraper.fetcher

```
