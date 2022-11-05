-----------------------------------------------------------------------------
-- tblMonitoresData definition 
--		This table aims to store ALL data from monitors. Every measurament
-- is stored here. This table is huge, but the process is latter on WITH
-- store procedures new tables and organization of data
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblMonitoresData')
				)
		)
	BEGIN
		CREATE TABLE tblMonitoresData (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50),
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);
	
	ALTER TABLE tblMonitoresData
		ADD CONSTRAINT fk_tblGeneral_tblMonitoresData FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END