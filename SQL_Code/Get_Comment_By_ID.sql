CREATE OR ALTER PROCEDURE CW2.Get_Comment_By_ID
    @comment_id INT
AS
BEGIN
    -- If comment doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Comments WHERE comment_id = @comment_id) BEGIN
        ;THROW 50001, 'Comment does not exist', 1;
        RETURN;
    END
    
    -- If above check is passed
    SELECT * FROM CW2.Comments WHERE comment_id = @comment_id;
END;
