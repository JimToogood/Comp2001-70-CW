CREATE OR ALTER PROCEDURE CW2.Get_User_By_ID
    @user_id INT
AS
BEGIN
    -- If user doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE user_id = @user_id) BEGIN
        ;THROW 50006, 'User does not exist', 6;
        RETURN;
    END

    -- If above check is passed
    SELECT * FROM CW2.Users WHERE user_id = @user_id;
END;
