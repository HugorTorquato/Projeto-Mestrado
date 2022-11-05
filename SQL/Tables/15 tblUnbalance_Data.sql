-----------------------------------------------------------------------------
-- tblUnbalance_Data definition 
--		This table aims to store data used in violation check, actually
-- one step before it.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblUnbalance_Data')
				)
		)
		BEGIN
			CREATE TABLE tblUnbalance_Data (
				Nome_ID int PRIMARY KEY IDENTITY(1,1),
				[Case] int,
				Simulation int,
				Barras varchar(50),
				Descr varchar(50)
			);
		
		ALTER TABLE tblUnbalance_Data
			ADD CONSTRAINT fk_tblGeneral_tblUnbalance_Data FOREIGN KEY (Simulation) 
				REFERENCES tblGeneral (Simulation)
		END