CREATE OR ALTER PROCEDURE CW2.Get_User_By_Email
    -- This procedure works because email is a UNIQUE field
    @email NVARCHAR(50)
AS
BEGIN
    -- If user doesnt exist
    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE email = @email) BEGIN
        ;THROW 50006, 'User does not exist', 6;
        RETURN;
    END

    -- If above check is passed
    SELECT * FROM CW2.Users WHERE email = @email;
END;
