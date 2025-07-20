CREATE OR ALTER PROCEDURE CW2.Delete_Trail
    @trail_id INT
AS
BEGIN
    DELETE FROM CW2.Trails WHERE trail_id = @trail_id;
END;
