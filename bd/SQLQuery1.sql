CREATE TABLE tblOwner (
    intOwnerId INTEGER IDENTITY(1,1) PRIMARY KEY,           -- ������������� ��������� ��������
    txtOwnerSurname CHAR(30),                 -- ������� ���������
    txtOwnerName CHAR(25),                    -- ��� ���������
    txtOwnerSecondName CHAR(30),              -- �������� ���������
    txtAddress CHAR(100)                      -- ����� ������������ ���������� ���������
);


CREATE TABLE tblFlat (
    intFlatId INTEGER IDENTITY(1,1) PRIMARY KEY,          -- ������������� ��������
    txtFlatAddress CHAR(100),               -- ����� ��������
    intOwnerId INTEGER NOT NULL,            -- �������� ��������
    fltArea DECIMAL,                        -- ������� ��������
    intCount INTEGER,                       -- ���������� �����������
    intStorey INTEGER,                      -- ����
	-- FOREIGN KEY (intOwnerId) REFERENCES tblOwner(intOwnerId)
);

CREATE TABLE tblWorker (
    intWorkerId INTEGER PRIMARY KEY,            -- ������������� ��������
    txtWorkerSurname CHAR(30),                   -- ������� ��������
    txtWorkerName CHAR(25),                      -- ��� ��������
    txtWorkerSecondName CHAR(30),                -- �������� ��������
    txtWorkerSpecialist CHAR(50),                -- ������������� ��������
    fltSum DECIMAL                               -- ����� �� ����������� ������
);

CREATE TABLE tblOperationType (
    intOperationTypeId INTEGER PRIMARY KEY,       -- ������������� ���� �����
    txtOperationTypeName CHAR(100),                -- ������������ ���� �����
    fltOperationPrice DECIMAL                      -- ��������� ���������� ������
);
CREATE TABLE tblOperation (
    intOperationId INTEGER PRIMARY KEY,  -- ������������� ����������� ������
    intFlatId INTEGER NOT NULL,          -- ��������
    intOperationTypeId INTEGER NOT NULL, -- ��� �����
    datOperationDate DATE NOT NULL,      -- ���� ���������� �����
    intWorkerId INTEGER NOT NULL,        -- �������
    txtOperationDescription CHAR(255),   -- �������� �����
    
    -- FOREIGN KEY (intFlatId) REFERENCES tblFlat(intFlatId),
    -- FOREIGN KEY (intOperationTypeId) REFERENCES tblOperationType(intOperationTypeId),
   -- FOREIGN KEY (intWorkerId) REFERENCES tblWorker(intWorkerId)
);