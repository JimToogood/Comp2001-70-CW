CREATE OR ALTER PROCEDURE CW2.Insert_Location
    @location_name NVARCHAR(50)
AS
BEGIN
    -- If location name already exists
    IF EXISTS (SELECT 1 FROM CW2.Locations WHERE location_name = @location_name) BEGIN
        ;THROW 50004, 'Location with that name already exists', 4;
        RETURN;
    END

    -- If location name is unique, insert location
    INSERT INTO CW2.Locations(
        location_name
    )
    VALUES (
        @location_name
    );
END;
