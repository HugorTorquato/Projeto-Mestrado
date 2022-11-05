-----------------------------------------------------------------------------
-- tblBarras definition 
--		This table aims to store max values from voltage and unbalances
-- Could be improved to store the timestemp it happened:
-- 		-> Possibe aproach is to add a a column with this data for each data
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblBarras')
				)
		)
	BEGIN
		CREATE TABLE tblBarras (
			Nome_ID int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Name varchar(50),
			V_pu_max_a float,
			V_pu_max_b float,
			V_pu_max_c float,
			V_pu_min_a float,
			V_pu_min_b float,
			V_pu_min_c float,
			Deseq_IEC float,
			Deseq_IEEE float,
			Deseq_NEMA float
		);
	
	ALTER TABLE tblBarras
		ADD CONSTRAINT fk_tblGeneral_tblBarras FOREIGN KEY (Simulation) 
			REFERENCES tblGeneral (Simulation)
END