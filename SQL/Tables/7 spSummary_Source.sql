-----------------------------------------------------------------------------
-- spSummary_Source definition
--		Define a summary table to track all soucer variables, in this CASE
-- just point the current monitor the the right element. But it can grow
-- to evaluate max values, avg values and so on
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spSummary_Source')
			)
	)
BEGIN
	-- Daria para colocar corrente máxima tbm... ponto a se pensar
	CREATE TABLE spSummary_Source (
		id int PRIMARY KEY IDENTITY(1,1),
		[Case] int,
		Simulation int,
		Monitor varchar(50),
		Elemento varchar(50)
		-- Adicionar aqui
	);
END