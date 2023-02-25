

CREATE OR ALTER VIEW vwCreateProcessedPVEnergyDataDiffTable
AS
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