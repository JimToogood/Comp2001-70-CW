CREATE OR ALTER TRIGGER CW2.Last_Edited_Trigger
-- Only trigger when Comments has been updated
ON CW2.Comments
AFTER UPDATE
AS
BEGIN
    -- Change last_edited_dt to current datetime, only for comments where the content is different
    UPDATE comment
    SET last_edited_dt = GETDATE()
    FROM CW2.Comments comment
        INNER JOIN inserted ON comment.comment_id = inserted.comment_id
        INNER JOIN deleted ON inserted.comment_id = deleted.comment_id
    WHERE inserted.content <> deleted.content;
END;
