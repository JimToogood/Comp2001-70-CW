CREATE OR ALTER PROCEDURE CW2.Insert_Comment
    @trail_id INT,
    @user_id INT,
    @content NVARCHAR(255)
AS
BEGIN
    -- If trail doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Trails WHERE trail_id = @trail_id) BEGIN
        ;THROW 50005, 'Trail does not exist', 5;
        RETURN;
    END

    -- If user doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE user_id = @user_id) BEGIN
        ;THROW 50006, 'User does not exist', 6;
        RETURN;
    END

    -- If above checks are passed
    INSERT INTO CW2.Comments(
        trail_id,
        user_id,
        content
    )
    VALUES (
        @trail_id,
        @user_id,
        @content
    );
END;
