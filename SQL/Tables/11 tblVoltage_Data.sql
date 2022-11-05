-----------------------------------------------------------------------------
-- tblVoltage_Data definition 
--		This table aims to store data used in violation check, actually
-- one step before it.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblVoltage_Data')
				)
		)
	BEGIN
		CREATE TABLE tblVoltage_Data (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Barras varchar(50),
			Fase varchar(50),
			TimeMaxPU varchar(50),
			ValueMaxPU float,
			TimeMinPU varchar(50),
			ValueMinPU float
		);
	
	ALTER TABLE tblVoltage_Data
		ADD CONSTRAINT fk_tblGeneral_tblVoltage_Data FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END