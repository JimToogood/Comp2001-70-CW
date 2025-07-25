CREATE OR ALTER PROCEDURE CW2.Delete_User
    @user_id INT
AS
BEGIN
    -- If user doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE user_id = @user_id) BEGIN
        ;THROW 50006, 'User does not exist', 6;
        RETURN;
    END

    -- If above check is passed
    -- Delete any comments made by the user
    DELETE FROM CW2.Comments WHERE user_id = @user_id;

    -- Delete user
    DELETE FROM CW2.Users WHERE user_id = @user_id;
END;
