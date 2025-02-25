SELECT 
    o.txtOperationDescription AS "Описание работы",
    w.txtWorkerSurname AS "Фамилия рабочего",
    o.datOperationDate AS "Дата проведения работы"
FROM tblOperation o
JOIN tblWorker w ON o.intWorkerId = w.intWorkerId
WHERE 
    (o.datOperationDate BETWEEN '2014-01-01' AND '2014-02-01'
     OR o.datOperationDate BETWEEN '2014-05-01' AND '2014-06-01')
    AND w.txtWorkerSurname IN ('Петров', 'Иванов')
ORDER BY o.datOperationDate ASC;
