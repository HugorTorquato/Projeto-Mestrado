
CREATE OR ALTER PROCEDURE spSUMCreateProcessedPVEergyDataDiff
AS
BEGIN

	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSUMProcessedPVEergyDataDiff')
				)
		)
	BEGIN
		DELETE FROM spSUMProcessedPVEergyDataDiff
		DBCC CHECKIDENT('spSUMProcessedPVEergyDataDiff', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO spSUMProcessedPVEergyDataDiff 
		([Case], Elemento, TimeStep, Sum_Eergy_5, Sum_Eergy_4, Sum_Eergy_Diff_5_4, 
		Sum_Eergy_7, Sum_Eergy_6, Sum_Eergy_Diff_7_6)
	
		SELECT
			[Case]
			,[Elemento]
			,[TimeStep]
			,([Sum_Pot_5] / 4) AS [Sum_Eergy_5]
			,([Sum_Pot_4] / 4 ) AS [Sum_Eergy_4]
			,([Sum_Pot_Diff_5_4] / 4 ) AS [Sum_Eergy_Diff_5_4]
			,([Sum_Pot_7] / 4 ) AS [Sum_Eergy_7]
			,([Sum_Pot_6] / 4 ) AS [Sum_Eergy_6]
			,([Sum_Pot_Diff_7_6] / 4 ) AS [Sum_Eergy_Diff_7_6]
		FROM [DB_Rede_3].[dbo].spSUMProcessedPVPowerDataDiff
END