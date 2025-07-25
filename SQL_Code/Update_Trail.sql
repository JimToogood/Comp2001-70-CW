CREATE OR ALTER PROCEDURE CW2.Update_Trail
    @trail_id INT,
    @trail_name NVARCHAR(50) = NULL,
    @distance FLOAT = NULL,
    @elevation_gain FLOAT = NULL,
    @estimated_time FLOAT = NULL,
    @route_type NVARCHAR(10) = NULL,
    @difficulty NVARCHAR(10) = NULL,
    @location_id INT = NULL
AS
BEGIN
    -- If trail doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_id = @trail_id) BEGIN
        ;THROW 50005, 'Trail does not exist', 5;
        RETURN;
    END

    -- If location is provided, but doesnt exist
    IF @location_id IS NOT NULL BEGIN
        IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
            ;THROW 50007, 'Location does not exist', 7;
            RETURN;
        END
    END

    -- If above checks are passed
    UPDATE CW2.Trails
        -- COALESCE is used so only values that are to be changed have to be provided
        SET trail_name = COALESCE(@trail_name, trail_name),
        distance = COALESCE(@distance, distance),
        elevation_gain = COALESCE(@elevation_gain, elevation_gain),
        estimated_time = COALESCE(@estimated_time, estimated_time),
        route_type = COALESCE(@route_type, route_type),
        difficulty = COALESCE(@difficulty, difficulty),
        location_id = COALESCE(@location_id, location_id)
    WHERE trail_id = @trail_id;
END;
