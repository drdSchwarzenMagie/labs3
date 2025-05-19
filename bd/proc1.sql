CREATE PROCEDURE usp_GetOwnersWithOperationCount
AS
BEGIN
    SET NOCOUNT ON;

    -- Удаляем временную таблицу, если она уже существует
    IF OBJECT_ID('tempdb..#OwnerOperations') IS NOT NULL
        DROP TABLE #OwnerOperations;

    -- Создаем временную таблицу
    CREATE TABLE #OwnerOperations (
        OwnerFullName NVARCHAR(100),
        OperationCount INT
    );

    -- Заполняем таблицу данными
    INSERT INTO #OwnerOperations (OwnerFullName, OperationCount)
    SELECT 
        o.txtOwnerSurname + ' ' + o.txtOwnerName + 
            ISNULL(' ' + o.txtOwnerSecondName, '') AS OwnerFullName,
        COUNT(op.intOperationId) AS OperationCount
    FROM tblOwner o
    LEFT JOIN tblFlat f ON o.intOwnerId = f.intOwnerId
    LEFT JOIN tblOperation op ON f.intFlatId = op.intFlatId
    GROUP BY o.txtOwnerSurname, o.txtOwnerName, o.txtOwnerSecondName;

    -- Выводим результат
    SELECT * FROM #OwnerOperations;
END;