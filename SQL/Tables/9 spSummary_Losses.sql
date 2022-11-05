-----------------------------------------------------------------------------
-- spSummary_Losses definition
--		Define a Summary table to track all losses values, in this CASE
-- just point the current monitor the the right element. But it can grow
-- to evaluate max values, avg values and so on
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spSummary_Losses')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spSummary_Losses (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50),
			Loss float
		);
	END