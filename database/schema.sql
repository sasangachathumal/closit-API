DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS clothingItem;
DROP TABLE IF EXISTS clothingItemDressCode;
DROP TABLE IF EXISTS clothingItemOccasion;
DROP TABLE IF EXISTS clothingItemWeather;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    accessToken VARCHAR(255),
    resetToken VARCHAR(255),
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clothingItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    colorCode VARCHAR(50) NOT NULL,
    material VARCHAR(50) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE clothingItemDressCode (
    clothingItemId INTEGER NOT NULL,
    dressCode VARCHAR(50) NOT NULL,
    PRIMARY KEY (clothingItemId, dressCode),
    FOREIGN KEY (clothingItemId) REFERENCES clothingItem(id) ON DELETE CASCADE
);

CREATE TABLE clothingItemOccasion (
    clothingItemId INTEGER NOT NULL,
    occasion VARCHAR(255) NOT NULL,
    PRIMARY KEY (clothingItemId, occasion),
    FOREIGN KEY (clothingItemId) REFERENCES clothingItem(id) ON DELETE CASCADE
);

CREATE TABLE clothingItemWeather (
    clothingItemId INTEGER NOT NULL,
    weather VARCHAR(100) NOT NULL,
    PRIMARY KEY (clothingItemId, weather),
    FOREIGN KEY (clothingItemId) REFERENCES clothingItem(id) ON DELETE CASCADE
);
