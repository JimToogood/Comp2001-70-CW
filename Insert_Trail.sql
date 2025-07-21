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
    -- If location doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
        ;THROW 50001, 'Location does not exist', 1;
        RETURN;
    END

    -- If trail name already exists
    IF EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_name = @trail_name) BEGIN
        ;THROW 50002, 'Trail with that name already exists', 2;
        RETURN;
    END

    -- If above checks are passed
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
