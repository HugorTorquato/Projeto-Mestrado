-----------------------------------------------------------------------------
-- tblCurrent_Elemt_Data_Ang definition 
--		This table aims to store ALL data from monitors. Every measurament
-- is stored here. This table is huge, but the process is latter on WITH
-- store procedures new tables and organization of data
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblCurrent_Elemt_Data_Ang')
				)
		)
	BEGIN
		CREATE TABLE tblCurrent_Elemt_Data_Ang (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Elementos varchar(50),
			Fase varchar(50)
		);
	
	ALTER TABLE tblCurrent_Elemt_Data_Ang
		ADD CONSTRAINT fk_tblGeneral_tblCurrent_Elemt_Data_Ang FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END