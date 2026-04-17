# Recipe Nutrition System

## Overview

A backend-focused system to compute nutritional values of food using standard **per 100g composition data**.
Supports both ingredient-based calculations and predefined dishes.

---

## Features

### Ingredient Mode (Completed)

* Search ingredients (`/ingredients/search`)
* Add multiple ingredients with grams
* Compute:

  * Total nutrients
  * Per-ingredient contribution

---

### Dish Mode (Partially Implemented)

* Endpoint: `/nutrition/dishes`
* Nutrient scaling based on grams
* Pending:

  * Dish data ingestion
  * Search endpoint (`/dishes/search`)

---

## Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL (normalized schema)
* **Data Processing:** Pandas

---

## API Endpoints

* `GET /ingredients/search?q=...`
* `GET /nutrients`
* `POST /nutrition/ingredients`
* `POST /nutrition/dishes`

---

## Database Design

Normalized schema:

* `ingredients`, `dishes`
* `nutrients`
* Mapping tables for nutrient values (per 100g)

---

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create `.env` in backend:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=nutrition_db
```

---

## Status

* Ingredient Mode: Completed
* Dish Mode: Backend ready, data + search pending

---
