# Riftbound Card Database

A custom collection tracker and visual database for the Riftbound card game.

This repository consists of two main components:
1. A Python-based CLI tool for data ingestion and card tracking (`riftbound/`).
2. A React/TypeScript frontend for searching, filtering, and displaying the collection (`front/`).

## Tech Stack

**Data Ingestion:**
- Python 3
- Local CSV file storage (`cards.csv`)

**Frontend Gallery:**
- React 19 (Vite)
- TypeScript
- Vanilla CSS + Bootstrap grid/utility classes
- PapaParse (for CSV ingestion in-browser)

## Usage

### 1. Adding Cards to the Database
Navigate to the data ingestion directory and run the interactive CLI script to append new cards to your local collection.

```bash
cd riftbound
python cardadd.py
```

The CLI handles:
- Color validation (FURY, MIND, CHAOS, etc.)
- Metadata logging (Set ID, Quantity, Type, Alt-art variants)
- Image URL resolution from the master `all_cards_database.csv`

### 2. Running the Visual Frontend
The frontend reads the generated CSV and provides a filterable UI to view your collection.

```bash
cd front
npm install
npm run dev
```

Open the provided local Vite server URL in your browser to view and search the gallery.
