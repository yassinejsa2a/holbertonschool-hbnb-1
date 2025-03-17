-- Create user table
CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create place table
CREATE TABLE place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Create review table
CREATE TABLE review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    place_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- Create amenity table
CREATE TABLE amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Create place_amenity table
CREATE TABLE place_amenity (
    place_id CHAR(36) PRIMARY KEY,
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    amenity_id CHAR(36) PRIMARY KEY,
    FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
);

-- Insert values for admin user
INSERT INTO user (id, email, first_name, last_name, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', '$2a$12$NlGI.VPRaWrTnR/1NcX0XuOnoa4f8jIrqW26cG0perXVH21HTpqnC', TRUE)

-- insert values for amenities
INSERT INTO amenity (id, name)
VALUES
    ('38081a56-3ae9-4eb2-b4f1-596cf86af448', 'WiFi'),
    ('1442db40-dd9f-41a6-9179-38fac8e039d2', 'Swimming Pool'),
    ('4b5510a8-bd96-425a-9a15-5d28f44f595a', 'Air Conditioning');

-- CRUD
-- Select
SELECT * FROM user;
SELECT * FROM amenity;
SELECT * FROM place;
SELECT * FROM review;

-- Update
-- User
UPDATE user
SET first_name = 'jonas'
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- review
UPDATE review
SET rating = 5
WHERE id = 'bdf0e51c-f2e1-4251-ac54-e63d2fa67c9e';

-- 




