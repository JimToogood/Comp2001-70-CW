CREATE OR ALTER PROCEDURE CW2.Delete_User
    @user_id INT
AS
BEGIN
    -- Delete any comments made by the user
    DELETE FROM CW2.Comments WHERE user_id = @user_id;

    -- Delete user
    DELETE FROM CW2.Users WHERE user_id = @user_id;
END;
