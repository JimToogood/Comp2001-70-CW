CREATE OR ALTER PROCEDURE CW2.Delete_Location
    @location_id INT
AS
BEGIN
    -- Check if location is used in any trails
    IF EXISTS (SELECT 1 FROM CW2.Trails WHERE location_id = @location_id) BEGIN
        ;THROW 50000, 'Cannot delete location as it is still referenced in CW2.Trails', 0;
        RETURN;
    END

    -- Only delete location if it is unused in any trails
    DELETE FROM CW2.Locations WHERE location_id = @location_id;
END;
