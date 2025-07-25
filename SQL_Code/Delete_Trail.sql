CREATE OR ALTER PROCEDURE CW2.Delete_Trail
    @trail_id INT
AS
BEGIN
    -- If trail doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_id = @trail_id) BEGIN
        ;THROW 50005, 'Trail does not exist', 5;
        RETURN;
    END

    -- If above check is passed
    -- Delete any comments on the trail
    DELETE FROM CW2.Comments WHERE trail_id = @trail_id;

    -- Delete trail
    DELETE FROM CW2.Trails WHERE trail_id = @trail_id;
END;
