CREATE OR ALTER PROCEDURE CW2.Insert_Trail
    @trail_name NVARCHAR(50),
    @distance FLOAT,
    @elevation_gain FLOAT,
    @estimated_time FLOAT,
    @route_type NVARCHAR(10),
    @difficulty NVARCHAR(10),
    @location_id INT
AS
BEGIN
    INSERT INTO CW2.Trails(
        trail_name,
        distance,
        elevation_gain,
        estimated_time,
        route_type,
        difficulty,
        location_id
    )
    VALUES (
        @trail_name,
        @distance,
        @elevation_gain,
        @estimated_time,
        @route_type,
        @difficulty,
        @location_id
    );
END;
