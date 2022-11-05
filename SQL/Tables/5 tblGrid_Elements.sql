-----------------------------------------------------------------------------
-- tblGrid_Elements definition 
--		This table aims to store max values from elements, but it is storing
-- only current values
-- Could be improved to store the timestemp it happened:
-- 		-> Possibe aproach is to add a a column with this data for each data
--		-> Also more data could be added for elements
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblGrid_Elements')
				)
		)
	BEGIN
		CREATE TABLE tblGrid_Elements (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Elemento varchar(50),
			I_pu_max_a float,
			I_pu_max_b float,
			I_pu_max_c float,
			I_pu_min_a float,
			I_pu_min_b float,
			I_pu_min_c float
		);
	
	ALTER TABLE tblGrid_Elements
		ADD CONSTRAINT fk_tblGeneral_tblGrid_Elements FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END