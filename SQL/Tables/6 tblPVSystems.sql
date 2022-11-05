-----------------------------------------------------------------------------
-- tblPVSystems definition 
--		This table aims to store PV data. Very important to calculate
-- HC latter on and also track pv positions across the network
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblPVSystems')
				)
		)
	BEGIN
		CREATE TABLE tblPVSystems (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Name varchar(50),
			Bus varchar(50),
			Pmp float,
			kW float,
			kvar float,
			kva float,
			FP float,
			Phases varchar(50),
			Irrad varchar(50),
			Temp varchar(50)
		);
	
	ALTER TABLE tblPVSystems
		ADD CONSTRAINT fk_tblGeneral_tblPVSystems FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END