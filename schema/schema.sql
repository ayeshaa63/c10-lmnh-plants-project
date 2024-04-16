DROP TABLE s_alpha.continent; GO
DROP TABLE s_alpha.country; GO
DROP TABLE s_alpha.origin; GO
DROP TABLE s_alpha.plant; GO
DROP TABLE s_alpha.botanist; GO
DROP TABLE s_alpha.image; GO
DROP TABLE s_alpha.recording; GO
DROP TABLE s_alpha.watering; GO

CREATE TABLE s_alpha.continent(
    continent_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(13)
);
GO

CREATE TABLE s_alpha.country(
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    continent_id TINYINT NOT NULL,
    FOREIGN KEY(continent_id) REFERENCES s_alpha.continent(continent_id)
);
GO

CREATE TABLE s_alpha.origin(
    origin_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    long FLOAT NOT NULL,
    lat FLOAT NOT NULL,
    location_name VARCHAR(30) NOT NULL,
    country_id SMALLINT NOT NULL,
    FOREIGN KEY(country_id) REFERENCES s_alpha.country(country_id)
);
GO

CREATE TABLE s_alpha.plant(
    plant_id SMALLINT UNIQUE NOT NULL,
    name VARCHAR(30) NOT NULL,
    scientific_name VARCHAR(30),
    origin_id SMALLINT,
    FOREIGN KEY(origin_id) REFERENCES s_alpha.origin(origin_id)
);
GO

CREATE TABLE s_alpha.botanist(
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    phone VARCHAR(15) NOT NULL,
);
GO

CREATE TABLE s_alpha.image(
    image_id INT IDENTITY(1,1) PRIMARY KEY,
    license INT,
    license_name TEXT,
    license_url TEXT,
    origin_url TEXT NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);
GO

CREATE TABLE s_alpha.recording(
    recording_id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temp FLOAT,
    soil_moisture FLOAT,
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(botanist_id) REFERENCES s_alpha.botanist(botanist_id),
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);
GO

CREATE TABLE s_alpha.watering(
    watering_id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY(plant_id) REFERENCES s_alpha.plant(plant_id)
);
GO
