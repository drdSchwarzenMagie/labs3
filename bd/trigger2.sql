CREATE TRIGGER trg_UpdateSumOnInsert
ON tblOperation
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Обновляем fltSum для работников по вставленным операциям
    UPDATE w
    SET w.fltSum = w.fltSum + op.fltOperationPrice
    FROM tblWorker w
    INNER JOIN inserted i ON w.intWorkerId = i.intWorkerId
    INNER JOIN tblOperationType op ON i.intOperationTypeId = op.intOperationTypeId;
END;

CREATE TRIGGER trg_UpdateSumOnDelete
ON tblOperation
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Уменьшаем fltSum для работников по удалённым операциям
    UPDATE w
    SET w.fltSum = w.fltSum - op.fltOperationPrice
    FROM tblWorker w
    INNER JOIN deleted d ON w.intWorkerId = d.intWorkerId
    INNER JOIN tblOperationType op ON d.intOperationTypeId = op.intOperationTypeId;
END;