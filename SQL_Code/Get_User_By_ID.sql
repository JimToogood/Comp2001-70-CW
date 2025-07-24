CREATE OR ALTER PROCEDURE CW2.Get_User_By_ID
    @user_id INT
AS
BEGIN
    SELECT * FROM CW2.Users WHERE user_id = @user_id;
END;
