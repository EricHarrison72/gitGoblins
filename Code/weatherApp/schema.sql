DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UsersCities;
DROP TABLE IF EXISTS WeatherInstance;


CREATE TABLE City (
	cityId int,
	cityName varchar(30),
	latiude int,
	longitude int,
	PRIMARY KEY (cityId)
);

CREATE TABLE User (
	userId int AUTOINCREMENT PRIMARY KEY,
	firstName varchar(30),
	lastName varchar(30),
	email varchar(50),
	emailList boolean,
	password varchar(128),
	
);

CREATE TABLE UsersCities (
	userId int,
	cityId int,
	PRIMARY KEY(userId, cityId),
	FOREIGN KEY (userId) REFERENCES User(userId)
		ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY (cityId) REFERENCES City(cityId)
		ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE WeatherInstance (
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
	
