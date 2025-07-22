CREATE OR ALTER PROCEDURE CW2.Update_User
    @user_id INT,
    @email NVARCHAR(50),
    @role NVARCHAR(10)
AS
BEGIN
    -- If user doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE user_id = @user_id) BEGIN
        ;THROW 50006, 'User does not exist', 6;
        RETURN;
    END

    -- If email already exists
    IF EXISTS (SELECT 1 FROM CW2.Users WHERE email = @email) BEGIN
        ;THROW 50003, 'Email already exists', 3;
        RETURN;
    END

    -- If above checks are passed
    UPDATE CW2.Users
        SET email = @email,
        role = @role
    WHERE user_id = @user_id;
END;
