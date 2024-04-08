-- This will be a script for adding fake temporary users to the db

-- Delete existing data from test tables to avoid conflicts
DELETE FROM WeatherInstance;
DELETE FROM UsersCities;
DELETE FROM User;
DELETE FROM City;

-- Ensure test tables exist
CREATE TABLE IF NOT EXISTS City (
    cityId int,
    cityName varchar(30),
    latitude int,
    longitude int,
    PRIMARY KEY (cityId)
);

CREATE TABLE IF NOT EXISTS User (
    userId int,
    firstName varchar(30),
    lastName varchar(30),
    email varchar(50),
    emailList boolean,
    password varchar(128),
    PRIMARY KEY(userId)
);

CREATE TABLE IF NOT EXISTS UsersCities (
    userId int,
    cityId int,
    PRIMARY KEY(userId, cityId),
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (cityId) REFERENCES City(cityId)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS WeatherInstance (
    cityId int,
    date DATETIME,
    tempMin DECIMAL(3,1),
    tempMax DECIMAL(3,1),
    sunshine int,
    rainfall DECIMAL(5,1),
    evaporation DECIMAL(5,1),
    cloud9am int,
    cloud3pm int,
    pressure9am DECIMAL(4,1),
    pressure3pm DECIMAL(4,1),
    humidity9am int,
    humidity3pm int,
    windGustSpeed int,
    windGustDir varchar(3),
    windSpeed9am int,
    windSpeed3pm int,
    windDir9am varchar(3),
    windDir3pm varchar(3),
    rainToday boolean,
    rainTomorrow boolean,
    PRIMARY KEY(cityId, date),
    FOREIGN KEY(cityId) REFERENCES City(cityId)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Insert data for testing into test tables

-- Cities
INSERT INTO City (cityId, cityName) VALUES
(99, 'Springfield'), -- cityId set to 99 and 100 so it doesn't fail UNIQUE constraint 
(100, 'Shelbyville'); -- error when populating actual database

-- Users
INSERT INTO User (userId, firstName, lastName, email, emailList, password, cityId) VALUES
(1, 'Homer', 'Simpson', 'homer@example.com', true, 'password123', 99),
(2, 'Marge', 'Simpson', 'marge@example.com', true, 'password123', 100),
(3, 'Bart', 'Simpson', 'bart@example.com', true, 'password123', 100),
(4, 'Lisa', 'Simpson', 'lisa@example.com', false, 'password123', 100);

-- UsersCities
INSERT INTO UsersCities (userId, cityId) VALUES
(1, 99),
(2, 100),
(3, 100),
(4, 100);

-- WeatherInstance
INSERT INTO WeatherInstance
    (cityId,        date, tempMin, tempMax, sunshine, rainfall, evaporation, cloud9am, cloud3pm, pressure9am, pressure3pm, humidity9am, humidity3pm, windGustSpeed, windGustDir, windSpeed9am, windSpeed3pm, windDir9am, windDir3pm, rainToday, rainTomorrow)
VALUES
    (    99, '2023-01-01',   -5.0,    10.0,        8,      0.0,         4.5,        1,        3,      1013.5,      1010.5,          80,          50,            12,         'W',           10,           20,        'N',        'S',      'No',        'Yes'),
    (    99, '2023-01-02',   -3.0,    'NA',        4,      5.0,         3.0,        1,        3,      1013.5,      1010.5,          80,          50,            35,       'NNE',           10,           20,        'N',        'S',     'Yes',        'Yes'),
    (    99, '2023-01-03',   'NA',    30.0,        1,     'NA',         0.1,        1,        3,      1013.5,      1010.5,          80,          50,           123,        'SW',           10,           20,        'N',        'S',     'Yes',         'No'),
    (   100, '2023-01-02',    0.0,    15.0,       10,      0.0,         5.0,        0,        1,      1015.0,      1012.0,          70,          40,            25,         'E',            5,           15,        'E',        'W',      'No',        'Yes');

-- Note: It might seem strange to be entering the strings 'No' and 'Yes' for `rainToday` and 
-- `rainTomorrow` since those columns are supposed to be booleans, but that's how weatherAUS.csv
-- does it and it has to work like that for our tests. So deal. 