CREATE OR ALTER PROCEDURE CW2.Delete_Location
    @location_id INT
AS
BEGIN
    -- If location doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
        ;THROW 50007, 'Location does not exist', 7;
        RETURN;
    END

    -- If location is used in any trails
    IF EXISTS (SELECT 1 FROM CW2.Trails WHERE location_id = @location_id) BEGIN
        ;THROW 50000, 'Cannot delete location as it is still referenced in CW2.Trails', 0;
        RETURN;
    END

    -- If above checks are passed
    DELETE FROM CW2.Locations WHERE location_id = @location_id;
END;
