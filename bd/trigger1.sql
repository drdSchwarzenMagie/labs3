CREATE TRIGGER trg_CheckOneOperationPerDayPerFlat
ON tblOperation
AFTER INSERT
AS
BEGIN
    -- Проверяем, есть ли вставленные записи, нарушающие правило
    IF EXISTS (
        SELECT 1
        FROM tblOperation o
        INNER JOIN inserted i 
            ON o.intFlatId = i.intFlatId
            AND o.datOperationDate = i.datOperationDate
        WHERE o.intOperationId <> i.intOperationId  -- Исключаем только что вставленную запись
        GROUP BY o.intFlatId, o.datOperationDate
        HAVING COUNT(*) > 0
    )
    BEGIN
        -- Откатываем транзакцию
        ROLLBACK TRANSACTION;

        -- Сообщение об ошибке
        THROW 50001, 'Нельзя добавить более одной работы для одной квартиры в один день.', 1;
        RETURN;
    END
END;