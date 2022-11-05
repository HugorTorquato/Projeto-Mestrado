-----------------------------------------------------------------------------
-- tblCurrent_Elemt_Data definition 
--		This table aims to store data used in violation check, actually
-- one step before it.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblCurrent_Elemt_Data')
				)
		)
	BEGIN
		CREATE TABLE tblCurrent_Elemt_Data (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Elementos varchar(50),
			Fase varchar(50)
		);
	
	ALTER TABLE tblCurrent_Elemt_Data
		ADD CONSTRAINT fk_tblGeneral_tblCurrent_Elemt_Data FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END