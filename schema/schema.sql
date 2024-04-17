DROP TABLE IF EXISTS s_alpha.watering;
DROP TABLE IF EXISTS s_alpha.recording;
DROP TABLE IF EXISTS s_alpha.image;
DROP TABLE IF EXISTS s_alpha.botanist;
DROP TABLE IF EXISTS s_alpha.plant;
DROP TABLE IF EXISTS s_alpha.origin;
DROP TABLE IF EXISTS s_alpha.country;
DROP TABLE IF EXISTS s_alpha.continent;

CREATE TABLE s_alpha.continent(
    continent_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(13)
);


CREATE TABLE s_alpha.country(
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    continent_id TINYINT NOT NULL,
    FOREIGN KEY(continent_id) REFERENCES s_alpha.continent(continent_id)
);


CREATE TABLE s_alpha.origin(
    origin_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    long FLOAT NOT NULL,
    lat FLOAT NOT NULL,
    location_name VARCHAR(30) NOT NULL,
    country_id SMALLINT NOT NULL,
    FOREIGN KEY(country_id) REFERENCES s_alpha.country(country_id)
);


CREATE TABLE s_alpha.plant(
    plant_id SMALLINT UNIQUE NOT NULL,
    name VARCHAR(30) NOT NULL,
    scientific_name VARCHAR(30),
    origin_id SMALLINT,
    FOREIGN KEY(origin_id) REFERENCES s_alpha.origin(origin_id)
);


CREATE TABLE s_alpha.botanist(
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    phone VARCHAR(20) NOT NULL,
);


CREATE TABLE s_alpha.image(
    image_id INT IDENTITY(1,1) PRIMARY KEY,
    license INT,
    license_name TEXT,
    license_url TEXT,
    origin_url TEXT NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);


CREATE TABLE s_alpha.recording(
    recording_id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    temp FLOAT,
    soil_moisture FLOAT,
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(botanist_id) REFERENCES s_alpha.botanist(botanist_id),
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);


CREATE TABLE s_alpha.watering(
    watering_id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);

