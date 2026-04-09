-- 1. Create nutrients FIRST (parent table)
CREATE TABLE nutrients (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  unit VARCHAR(20)  NOT NULL
);

-- 2. Ingredients
CREATE TABLE ingredients (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  INDEX idx_ingredients_name (name)
);

-- 3. Ingredient ↔ Nutrients mapping
CREATE TABLE ingredient_nutrients (
  ingredient_id   INT NOT NULL,
  nutrient_id     INT NOT NULL,
  value_per_100g  DOUBLE NOT NULL,
  PRIMARY KEY (ingredient_id, nutrient_id),
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
  FOREIGN KEY (nutrient_id)   REFERENCES nutrients(id)   ON DELETE CASCADE
);

-- 4. Dishes
CREATE TABLE dishes (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  INDEX idx_dishes_name (name)
);

-- 5. Dish ↔ Nutrients mapping
CREATE TABLE dish_nutrients (
  dish_id         INT NOT NULL,
  nutrient_id     INT NOT NULL,
  value_per_100g  DOUBLE NOT NULL,
  PRIMARY KEY (dish_id, nutrient_id),
  FOREIGN KEY (dish_id)     REFERENCES dishes(id)    ON DELETE CASCADE,
  FOREIGN KEY (nutrient_id) REFERENCES nutrients(id) ON DELETE CASCADE
);