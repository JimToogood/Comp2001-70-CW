CREATE OR ALTER PROCEDURE CW2.Get_Location_By_ID
    @location_id INT
AS
BEGIN
    -- If location doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Locations WHERE location_id = @location_id) BEGIN
        ;THROW 50007, 'Location does not exist', 7;
        RETURN;
    END

    -- If above check is passed
    SELECT * FROM CW2.Locations WHERE location_id = @location_id;
END;
