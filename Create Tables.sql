USE COMP2001_JToogood;

--DROP TABLE CW2.Comments;
--DROP TABLE CW2.Users;
--DROP TABLE CW2.Trails;
--DROP TABLE CW2.Locations;

CREATE TABLE CW2.Locations (
    location_id INT PRIMARY KEY IDENTITY(1, 1),
    location_name NVARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE CW2.Trails (
    trail_id INT PRIMARY KEY IDENTITY(1, 1),
    trail_name NVARCHAR(50) UNIQUE NOT NULL,
    distance FLOAT NOT NULL,
    elevation_gain FLOAT NOT NULL,
    estimated_time FLOAT NOT NULL,
    route_type NVARCHAR(20) NOT NULL,
    difficulty NVARCHAR(10) NOT NULL,
    location_id INT NOT NULL REFERENCES CW2.Locations(location_id)
);

CREATE TABLE CW2.Users (
    user_id INT PRIMARY KEY IDENTITY(1, 1),
    email NVARCHAR(50) UNIQUE NOT NULL,
    role NVARCHAR(10) NOT NULL
);

CREATE TABLE CW2.Comments (
    comment_id INT PRIMARY KEY IDENTITY(1, 1),
    trail_id INT NOT NULL REFERENCES CW2.Trails(trail_id),
    user_id INT NOT NULL REFERENCES CW2.Users(user_id),
    content NVARCHAR(255) NOT NULL,
    created_dt DATETIME NOT NULL DEFAULT GETDATE(),
    last_edited_dt DATETIME NULL,
    is_archived BIT NOT NULL DEFAULT 0
);
