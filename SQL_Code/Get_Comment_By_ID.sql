CREATE OR ALTER PROCEDURE CW2.Get_Comment_By_ID
    @comment_id INT
AS
BEGIN
    SELECT * FROM CW2.Comments WHERE comment_id = @comment_id;
END;
