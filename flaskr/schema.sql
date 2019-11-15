DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Anthropometric;

CREATE TABLE User(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    email TEXT unique NOT NULL,
    birth_date DATE NOT NULL,
    password TEXT NOT NULL,
    medicalRegister TEXT,
    userType TEXT NOT NULL,
);

CREATE TABLE Anthropometric(
    userId INTEGER NOT NULL,
    heartBeats FLOAT NOT NULL,
    systolicPressure FLOAT NOT NULL,
    diastolicPressure FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi FLOAT NOT NULL,
    armCircunference FLOAT NOT NULL,
    waistCircunference FLOAT NOT NULL,
    sagittalAbdominalDiameter FLOAT NOT NULL,
    fistStrength FLOAT NOT NULL,
    age FLOAT NOT NULL,
    calories FLOAT NOT NULL,
    proteins FLOAT NOT NULL,
    carbohydrates FLOAT NOT NULL,
    totalSugar FLOAT NOT NULL,
    fibers FLOAT NOT NULL,
    fats FLOAT NOT NULL,
    saturatedFat FLOAT NOT NULL,
    monounsaturatedFat FLOAT NOT NULL,
    polyunsaturatedFat FLOAT NOT NULL,
    cholesterol FLOAT NOT NULL,
    alcohol FLOAT NOT NULL
 )

 CREATE TABLE