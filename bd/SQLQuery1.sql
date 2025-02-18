CREATE TABLE tblOwner (
    intOwnerId INTEGER IDENTITY(1,1) PRIMARY KEY,           -- Идентификатор владельца квартиры
    txtOwnerSurname CHAR(30),                 -- Фамилия владельца
    txtOwnerName CHAR(25),                    -- Имя владельца
    txtOwnerSecondName CHAR(30),              -- Отчество владельца
    txtAddress CHAR(100)                      -- Адрес фактического проживания владельца
);


CREATE TABLE tblFlat (
    intFlatId INTEGER IDENTITY(1,1) PRIMARY KEY,          -- Идентификатор квартиры
    txtFlatAddress CHAR(100),               -- Адрес квартиры
    intOwnerId INTEGER NOT NULL,            -- Владелец квартиры
    fltArea DECIMAL,                        -- Площадь квартиры
    intCount INTEGER,                       -- Количество проживающих
    intStorey INTEGER,                      -- Этаж
	-- FOREIGN KEY (intOwnerId) REFERENCES tblOwner(intOwnerId)
);

CREATE TABLE tblWorker (
    intWorkerId INTEGER PRIMARY KEY,            -- Идентификатор рабочего
    txtWorkerSurname CHAR(30),                   -- Фамилия рабочего
    txtWorkerName CHAR(25),                      -- Имя рабочего
    txtWorkerSecondName CHAR(30),                -- Отчество рабочего
    txtWorkerSpecialist CHAR(50),                -- Специальность рабочего
    fltSum DECIMAL                               -- Сумма за выполненные работы
);

CREATE TABLE tblOperationType (
    intOperationTypeId INTEGER PRIMARY KEY,       -- Идентификатор типа работ
    txtOperationTypeName CHAR(100),                -- Наименование типа работ
    fltOperationPrice DECIMAL                      -- Стоимость проведения работы
);
CREATE TABLE tblOperation (
    intOperationId INTEGER PRIMARY KEY,  -- Идентификатор проведенной работы
    intFlatId INTEGER NOT NULL,          -- Квартира
    intOperationTypeId INTEGER NOT NULL, -- Тип работ
    datOperationDate DATE NOT NULL,      -- Дата проведения работ
    intWorkerId INTEGER NOT NULL,        -- Рабочий
    txtOperationDescription CHAR(255),   -- Описание работ
    
    -- FOREIGN KEY (intFlatId) REFERENCES tblFlat(intFlatId),
    -- FOREIGN KEY (intOperationTypeId) REFERENCES tblOperationType(intOperationTypeId),
   -- FOREIGN KEY (intWorkerId) REFERENCES tblWorker(intWorkerId)
);