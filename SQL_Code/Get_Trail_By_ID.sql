CREATE OR ALTER PROCEDURE CW2.Get_Trail_By_ID
    @trail_id INT
AS
BEGIN
    -- If trail doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_id = @trail_id) BEGIN
        ;THROW 50005, 'Trail does not exist', 5;
        RETURN;
    END

    -- If above check is passed
    SELECT * FROM CW2.Trails WHERE trail_id = @trail_id;
END;
