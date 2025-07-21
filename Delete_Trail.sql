CREATE OR ALTER PROCEDURE CW2.Delete_Trail
    @trail_id INT
AS
BEGIN
    -- Delete any comments on the trail
    DELETE FROM CW2.Comments WHERE trail_id = @trail_id;

    -- Delete trail
    DELETE FROM CW2.Trails WHERE trail_id = @trail_id;
END;
