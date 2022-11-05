-----------------------------------------------------------------------------
-- spLossesData definition
--		Define a data table to track all losses values, based ON
-- simulation, case, monitor and element. Each grou of data is associated
-- with a monitor for one element for one case in one simulation FROM
-- spSummary_Table
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spLossesData')
			)
	)
	BEGIN
		CREATE TABLE spLossesData (
			id int PRIMARY KEY IDENTITY(1,1),
			id_Summary int,
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);

		ALTER TABLE spLossesData
		ADD CONSTRAINT fk_spSummary_Losses_spLossesData FOREIGN KEY (id_Summary) REFERENCES spSummary_Losses (id)
	END