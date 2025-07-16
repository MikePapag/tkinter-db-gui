CREATE TABLE boats (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    latitude DOUBLE,
    longitude DOUBLE,
    moving BOOLEAN
);

INSERT INTO boats (id, name, latitude, longitude, moving) VALUES
(1, 'Boat One', 45.0, -70.0, TRUE),
(2, 'Boat Two', 46.0, -71.0, FALSE);
