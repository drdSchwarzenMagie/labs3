CREATE TRIGGER trg_CheckOneWorkPerDay
ON tblOperation
INSTEAD OF INSERT
AS
BEGIN
    -- Проверка на наличие дубликатов по intFlatId + datOperationDate
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN tblOperation o 
          ON i.intFlatId = o.intFlatId 
          AND CAST(i.datOperationDate AS DATE) = CAST(o.datOperationDate AS DATE)
    )
    BEGIN
        RAISERROR('Нельзя добавлять более одной работы в день для одной квартиры.', 16, 1);
        RETURN;
    END

    -- Если всё в порядке — вставляем данные
    INSERT INTO tblOperation (
        intFlatId,
        intOperationTypeId,
        datOperationDate,
        intWorkerId,
        txtOperationDescription
    )
    SELECT 
        intFlatId,
        intOperationTypeId,
        datOperationDate,
        intWorkerId,
        txtOperationDescription
    FROM inserted;
END