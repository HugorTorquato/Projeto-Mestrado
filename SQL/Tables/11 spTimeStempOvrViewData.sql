-----------------------------------------------------------------------------
-- spTimeStempOvrViewData definition
--		Define a table to store all timestemp overvew values. At this
-- moment i'm only using it to sum active power from pv systems. But
-- it can grow to any desired value that can be summarised here.
-- IT WILL BE IMPORTANT TO GENERATE RESULTS LATTER
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spTimeStempOvrViewData')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spTimeStempOvrViewData (
			id int PRIMARY KEY IDENTITY(1,1),
			TimeStep int,
			[Case] int,
			Simulation int,
			Sum_Pot_W float
			-- Adicionar aqui
		);
	END