CREATE OR ALTER PROCEDURE CW2.Get_Location_By_ID
    @location_id INT
AS
BEGIN
    SELECT * FROM CW2.Locations WHERE location_id = @location_id;
END;
