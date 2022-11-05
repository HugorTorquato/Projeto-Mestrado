-----------------------------------------------------------------------------
-- spSummary_InvControl definition
--		Define a summary table to filter invcontrol monitors and elements
-- There is another table, with a FK link that has all measuraments related
-- to this monitor
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSummary_InvControl')
				)
		)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spSummary_InvControl (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50)
			-- Adicionar aqui
		);
	END