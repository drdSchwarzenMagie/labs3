-- Создание таблицы владельцев квартир
CREATE TABLE tblOwner (
    intOwnerId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    txtOwnerSurname NVARCHAR(30) NOT NULL,
    txtOwnerName NVARCHAR(25) NOT NULL,
    txtOwnerSecondName NVARCHAR(30),
    txtAddress NVARCHAR(100) NOT NULL
);

-- Создание таблицы квартир
CREATE TABLE tblFlat (
    intFlatId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    txtFlatAddress NVARCHAR(100) NOT NULL,
    intOwnerId INT NOT NULL,
    fltArea DECIMAL(10,2) NOT NULL CHECK (fltArea > 0),
    intCount INT NOT NULL CHECK (intCount >= 0),
    intStorey INT NOT NULL CHECK (intStorey > 0),
    CONSTRAINT FK_Flat_Owner FOREIGN KEY (intOwnerId)
        REFERENCES tblOwner(intOwnerId)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

-- Создание таблицы рабочих
CREATE TABLE tblWorker (
    intWorkerId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    txtWorkerSurname NVARCHAR(30) NOT NULL,
    txtWorkerName NVARCHAR(25) NOT NULL,
    txtWorkerSecondName NVARCHAR(30),
    txtWorkerSpecialist NVARCHAR(50) NOT NULL,
    fltSum DECIMAL(10,2) NOT NULL CHECK (fltSum >= 0)
);

-- Создание таблицы типов работ
CREATE TABLE tblOperationType (
    intOperationTypeId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    txtOperationTypeName NVARCHAR(100) NOT NULL,
    fltOperationPrice DECIMAL(10,2) NOT NULL CHECK (fltOperationPrice >= 0)
);

-- Создание таблицы проведенных работ
CREATE TABLE tblOperation (
    intOperationId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    intFlatId INT NOT NULL,
    intOperationTypeId INT NOT NULL,
    datOperationDate DATE NOT NULL,
    intWorkerId INT NOT NULL,
    txtOperationDescription NVARCHAR(255),
    CONSTRAINT FK_Operation_Flat FOREIGN KEY (intFlatId)
        REFERENCES tblFlat(intFlatId)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT FK_Operation_OperationType FOREIGN KEY (intOperationTypeId)
        REFERENCES tblOperationType(intOperationTypeId)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT FK_Operation_Worker FOREIGN KEY (intWorkerId)
        REFERENCES tblWorker(intWorkerId)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);