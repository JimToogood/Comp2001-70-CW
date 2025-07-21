CREATE OR ALTER PROCEDURE CW2.Update_Trail
    @trail_id INT,
    @trail_name NVARCHAR(50),
    @distance FLOAT,
    @elevation_gain FLOAT,
    @estimated_time FLOAT,
    @route_type NVARCHAR(10),
    @difficulty NVARCHAR(10),
    @location_id INT
AS
BEGIN
    -- If trail doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_id = @trail_id) BEGIN
        ;THROW 50005, 'Trail does not exist', 5;
        RETURN;
    END

    -- If location doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
        ;THROW 50001, 'Invalid location ID', 1;
        RETURN;
    END

    -- If above checks are passed
    UPDATE CW2.Trails
        SET trail_name = @trail_name,
        distance = @distance,
        elevation_gain = @elevation_gain,
        estimated_time = @estimated_time,
        route_type = @route_type,
        difficulty = @difficulty,
        location_id = @location_id
    WHERE trail_id = @trail_id;
END;
