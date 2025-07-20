CREATE OR ALTER PROCEDURE CW2.Insert_Location
    @location_name NVARCHAR(50)
AS
BEGIN
    INSERT INTO CW2.Locations(
        location_name
    )
    VALUES (
        @location_name
    );
END;
