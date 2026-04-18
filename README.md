# Recipe Nutrition System

## Overview

A backend system to compute nutritional values of foods using standardized **per-100g composition data**.
Supports both ingredient-level aggregation and predefined dish-based calculations.

---

## Key Features

### Ingredient Mode

* Search and select multiple ingredients

* Compute total nutrition using weighted aggregation:

  total = Σ(value_per_100g × grams / 100)

* Returns both total values and per-ingredient contributions

---

### Dish Mode

* Search predefined dishes
* Compute scaled nutrition based on input grams
* Optimized for fast lookup and calculation

---

## System Design

* **Normalized Database Schema**

  * Eliminates redundancy by separating:

    * foods (ingredients/dishes)
    * nutrients
    * mapping tables (`value_per_100g`)

* Supports easy addition of new nutrients without schema changes

* **Efficient Querying**

  * Single JOIN-based query for aggregation
  * Prefix-based indexed search for autosuggest

---

## Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL
* **Data Processing:** Pandas

---

## API Endpoints

* `GET /ingredients/search`
* `GET /dishes/search`
* `GET /nutrients`
* `POST /nutrition/ingredients`
* `POST /nutrition/dishes`

## Setup

```bash id="9r3u7v"
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```