CREATE OR ALTER PROCEDURE CW2.Update_User
    @user_id INT,
    @user_name NVARCHAR(50) = NULL,
    @email NVARCHAR(50) = NULL,
    @role NVARCHAR(10) = NULL
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
        SET user_name = COALESCE(@user_name, user_name),
        email = COALESCE(@email, email),
        role = COALESCE(@role, role)
    WHERE user_id = @user_id;
END;
