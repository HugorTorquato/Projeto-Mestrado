-----------------------------------------------------------------------------
-- tblGD definition 
--		This table aims to store GD data, I'm not currently using it but
-- i may need it. That is why i decided to keep it
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblGD')
				)
		)
	BEGIN
		CREATE TABLE tblGD (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Name varchar(50),
			Bus varchar(50),
			kW float,
			kvar float,
			Phases varchar(50),
			LoadShape varchar(50),
		);
	
	ALTER TABLE tblGD
		ADD CONSTRAINT fk_tblGeneral_tblGD FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END