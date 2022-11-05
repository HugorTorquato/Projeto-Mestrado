-----------------------------------------------------------------------------
-- tblVoltage_Data_Ang definition 
--		This table aims to store data used in violation check, actually
-- one step before it.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblVoltage_Data_Ang')
				)
		)
	BEGIN
		CREATE TABLE tblVoltage_Data_Ang (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Barras varchar(50),
			Fase varchar(50)
		);
	
	ALTER TABLE tblVoltage_Data_Ang
		ADD CONSTRAINT fk_tblGeneral_tblVoltage_Data_Ang FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END