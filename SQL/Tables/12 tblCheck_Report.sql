-----------------------------------------------------------------------------
-- tblCheck_Report definition 
--		This table aims to store violation ocurrency over simulations
-- Each column will have 1 if violation happened and 0 if NOT
-- TODO: It could be a bool instead of int
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblCheck_Report')
				)
		)
	BEGIN
		CREATE TABLE tblCheck_Report (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			overvoltage int,
			undervoltage int,
			overcurrent int,
			unbalance int
			
		);
	
	ALTER TABLE tblCheck_Report
		ADD CONSTRAINT fk_tblGeneral_tblCheck_Report FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END