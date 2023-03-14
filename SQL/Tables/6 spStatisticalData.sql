-----------------------------------------------------------------------------
-- spStatisticalData definition
--		Define a statistical results table to centralize this kind of results
-- Idea here is to create an overview for each case in each simulation
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spStatisticalData')
			)
	)
	BEGIN
		CREATE TABLE spStatisticalData (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			id_Results int,
			HC float
		)

		ALTER TABLE spStatisticalData
			ADD CONSTRAINT fk_spStatisticalResults_spStatisticalData 
			FOREIGN KEY (id_Results) REFERENCES spStatisticalResults (id)
	END