-----------------------------------------------------------------------------
-- spSUMProcessedPVEergyDataDiff definition (Energy)
--		Define a table to store the difference between VW cases and without 
-- VW control. Simulations 4 and 6 are the control ones, 5 and 7 are with
-- VW control active and VV + VW control active. There is a collumn to 
-- measure the difference between them here. ( 3-Phase in this case )
--
-- Energy was calculated dividint max power by 4.My timestemp is 15min
-- and if we convert 15*Pkwmin/60min we have 1/4 as result.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spSUMProcessedPVEergyDataDiff')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spSUMProcessedPVEergyDataDiff (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Elemento nvarchar(50),
			TimeStep int,
			Sum_Eergy_2 float,
			Sum_Eergy_5 float,
			Sum_Eergy_4 float,
			Sum_Eergy_Diff_5_4 float,
			Sum_Eergy_7 float,
			Sum_Eergy_6 float,
			Sum_Eergy_Diff_7_6 float
			-- Adicionar aqui
		);
	END