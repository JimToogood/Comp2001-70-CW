CREATE OR ALTER PROCEDURE CW2.Insert_Comment
    @trail_id INT,
    @user_id INT,
    @content NVARCHAR(255)
AS
BEGIN
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
