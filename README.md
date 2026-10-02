# XLabs AI Guide

A focused learning assistant that helps technical learners identify knowledge gaps and decide what to learn next.

## The Problem

Technical learners can struggle to tell the difference between what they recognize and what they can actually apply. Without targeted feedback, it is difficult to know which concepts to revisit or what to practice next.

## What It Does

Learners answer practical technical questions and troubleshooting scenarios in one focused domain. The guide evaluates their responses against trusted technical documentation, identifies likely knowledge gaps, and returns a structured assessment with personalized learning and practice recommendations.

## Setup

1. Install uv if you don't have it yet: https://docs.astral.sh/uv/getting-started/installation/

2. Clone this repository (or download the zip and extract it).

3. Create a `.env` file from the template and add your API key:

       cp .env.example .env

4. Install dependencies:

       uv sync

5. Start Jupyter:

       uv run jupyter notebook

## Notebooks

- `notebooks/01-setup.ipynb` - smoke test that confirms your environment works
- `notebooks/02-rag.ipynb` - a minimal RAG baseline you can adapt to your own data

## Data

Put trusted technical documentation and other project data in the `data/` folder. See `notebooks/02-rag.ipynb` for how to load it.
