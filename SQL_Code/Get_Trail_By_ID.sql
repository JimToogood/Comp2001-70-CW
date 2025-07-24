CREATE OR ALTER PROCEDURE CW2.Get_Trail_By_ID
    @trail_id INT
AS
BEGIN
    SELECT * FROM CW2.Trails WHERE trail_id = @trail_id;
END;
