CREATE OR ALTER PROCEDURE CW2.Update_Comment
    @comment_id INT,
    @content NVARCHAR(255)
AS
BEGIN
    -- If comment doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Comments WHERE comment_id = @comment_id) BEGIN
        ;THROW 50001, 'Comment does not exist', 1;
        RETURN;
    END

    -- If above check is passed
    UPDATE CW2.Comments
        SET content = @content
    WHERE comment_id = @comment_id;
END;
