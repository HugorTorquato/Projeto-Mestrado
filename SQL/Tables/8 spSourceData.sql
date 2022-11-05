-----------------------------------------------------------------------------
-- spSourceData definition
--		Define a Data table to store all soucer variables, based ON
-- simulation, case, monitor and element. Each grou of data is associated
-- with a monitor for one element for one case in one simulation FROM
-- spSummary_Table
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spSourceData')
			)
	)
BEGIN
	CREATE TABLE spSourceData (
		id int PRIMARY KEY IDENTITY(1,1),
		id_Summary int,
		TimeStep int,
		Measurement varchar(50),
		[Value] float
	);

	ALTER TABLE spSourceData
	ADD CONSTRAINT fk_spSummary_Source_Source FOREIGN KEY (id_Summary) REFERENCES spSummary_Source (id)
END