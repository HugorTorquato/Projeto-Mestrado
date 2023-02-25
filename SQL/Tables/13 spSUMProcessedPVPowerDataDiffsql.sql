-----------------------------------------------------------------------------
-- spSUMProcessedPVPowerDataDiff definition
--		Define a table to store the difference between VW cases and without 
-- VW control. Simulations 4 and 6 are the control ones, 5 and 7 are with
-- VW control active and VV + VW control active. There is a collumn to 
-- measure the difference between them here. ( 3-Phase in this case )
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spSUMProcessedPVPowerDataDiff')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spSUMProcessedPVPowerDataDiff (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Elemento nvarchar(50),
			TimeStep int,
			Sum_Pot_5 float,
			Sum_Pot_4 float,
			Sum_Pot_Diff_5_4 float,
			Sum_Pot_7 float,
			Sum_Pot_6 float,
			Sum_Pot_Diff_7_6 float
			-- Adicionar aqui
		);
	END