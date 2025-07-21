CREATE OR ALTER PROCEDURE CW2.Delete_Comment
    @comment_id INT
AS
BEGIN
    DELETE FROM CW2.Comments WHERE comment_id = @comment_id;
END;
