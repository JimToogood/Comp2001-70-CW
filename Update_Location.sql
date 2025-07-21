CREATE OR ALTER PROCEDURE CW2.Update_Location
    @location_id INT,
    @location_name NVARCHAR(50)
AS
BEGIN
    -- If location doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
        ;THROW 50007, 'Location does not exist', 7;
        RETURN;
    END

    -- If location name already exists
    IF EXISTS (SELECT 1 FROM CW2.Locations WHERE location_name = @location_name) BEGIN
        ;THROW 50004, 'Location with that name already exists', 4;
        RETURN;
    END

    -- If above checks are passed
    UPDATE CW2.Locations
        SET location_name = @location_name
    WHERE location_id = @location_id;
END;
