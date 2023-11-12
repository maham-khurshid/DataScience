CREATE DATABASE gans;
USE gans;
-- City	Country	Population	latitude	longitude

CREATE TABLE cities (
	city_id INT AUTO_INCREMENT,
	City VARCHAR(100),
    Country VARCHAR(10),
    Population INT,
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (city_id)
);

CREATE TABLE airports (
	ICAO VARCHAR(6),
    city_id INT,
    PRIMARY KEY (ICAO),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- city_id	forecast_time	temperature	wind_speed	humidity

CREATE TABLE weathers (
	weather_id INT AUTO_INCREMENT,
	city_id INT,
    forecast_time DATETIME,
    temperature FLOAT,
    wind_speed FLOAT,
    humidity FLOAT,
    PRIMARY KEY (weather_id),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);


-- Arrival_airport	Departure_airport_icao	Departure_airport_city	Departure_terminal	Arrival_time_local

CREATE TABLE flights (
	flight_id INT AUTO_INCREMENT,
    Arrival_airport VARCHAR(6),
    Departure_airport_icao VARCHAR(6),
    Departure_airport_city VARCHAR(100),
    Departure_terminal VARCHAR(50),
    Arrival_time_local DATETIME,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (Arrival_airport) REFERENCES airports(ICAO)
);

select * from cities;
select * from airports;
select * from weathers;
select * from flights;