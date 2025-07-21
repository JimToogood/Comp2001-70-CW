CREATE OR ALTER PROCEDURE CW2.Insert_User
    @email NVARCHAR(50),
    @role NVARCHAR(10)
AS
BEGIN
    -- If email already exists
    IF EXISTS (SELECT 1 FROM CW2.Users WHERE email = @email) BEGIN
        ;THROW 50003, 'Email already exists', 3;
        RETURN;
    END

    -- If email is unique, insert user
    INSERT INTO CW2.Users(
        email,
        role
    )
    VALUES (
        @email,
        @role
    );
END;
