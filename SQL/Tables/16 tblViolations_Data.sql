-----------------------------------------------------------------------------
-- tblViolations_Data definition 
--		This table aims to store each violation data from simulation. The
-- value presented in here is the last sample of steps without violations,
-- (i.e: We need to violate the limits 4 times to count as a violation,
-- the fourth value wil be stored in this table )
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblViolations_Data')
				)
		)
		BEGIN
			CREATE TABLE tblViolations_Data (
				Nome_ID int PRIMARY KEY IDENTITY(1,1),
				[Case] int,
				Simulation int,
				Element varchar(50),
				Fase int,
				ViolationType int,
				TimeStep int,
				[Value] float
			);
		
		ALTER TABLE tblViolations_Data
			ADD CONSTRAINT fk_tblGeneral_tblViolations_Data FOREIGN KEY (Simulation) 
				REFERENCES tblGeneral (Simulation)
		END