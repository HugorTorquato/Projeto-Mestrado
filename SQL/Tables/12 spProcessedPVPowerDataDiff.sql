-----------------------------------------------------------------------------
-- spProcessedPVPowerDataDiff definition
--		Define a table to store the difference between VW cases and without 
-- VW control. Simulations 4 and 6 are the control ones, 5 and 7 are with
-- VW control active and VV + VW control active. There is a collumn to 
-- measure the difference between them here.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spProcessedPVPowerDataDiff')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spProcessedPVPowerDataDiff (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Elemento nvarchar(50),
			Measurement nvarchar(50),
			TimeStep int,
			Value_S2 float,
			Value_S5 float,
			Value_S4 float,
			Value_diff_5to4 float,
			Value_S7 float,
			Value_S6 float,
			Value_diff_7to6 float
			-- Adicionar aqui
		);
	END