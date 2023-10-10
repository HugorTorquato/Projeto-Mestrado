



CREATE OR ALTER VIEW vwHCCResultsTable
AS
	WITH

		BATSUM AS (
			SELECT
				[CASE]
				, [AVG_MAX_Eergy_Diff_5_4]
				, [AVG_MAX_Eergy_Diff_7_6]
			FROM vwBESSAVGResults
		),

		HC_CASE AS (
			SELECT
				[Case]
				,[Elemento]
				,[TimeStep]
				,([Sum_Pot_2] / 4) AS [Sum_Energy_2]
				,([Sum_Pot_4] / 4) AS [Sum_Energy_4]
				,([Sum_Pot_6] / 4) AS [Sum_Energy_6]
			FROM spSUMProcessedPVPowerDataDiff  
		
		),
		GroupHC AS (

			SELECT 
				HC_CASE.[Case] 
				, SUM(HC_CASE.Sum_Energy_2) AS Sum_Energy_Case_2
				, SUM(HC_CASE.Sum_Energy_4) AS Sum_Energy_Case_4
				, SUM(HC_CASE.Sum_Energy_6) AS Sum_Energy_Case_6
			FROM HC_CASE
			GROUP BY HC_CASE.[Case]

		),
		ByCase as (
			SELECT 
				BATSUM.[Case]
				, BATSUM.[AVG_MAX_Eergy_Diff_5_4]
				, BATSUM.[AVG_MAX_Eergy_Diff_7_6]
				, GroupHC.Sum_Energy_Case_2
				, GroupHC.Sum_Energy_Case_4
				, GroupHC.Sum_Energy_Case_6
				, ( BATSUM.[AVG_MAX_Eergy_Diff_5_4] / ( GroupHC.Sum_Energy_Case_4 - GroupHC.Sum_Energy_Case_2 ) ) AS HCC4
				, ( BATSUM.[AVG_MAX_Eergy_Diff_7_6] / ( GroupHC.Sum_Energy_Case_6 - GroupHC.Sum_Energy_Case_2 ) ) AS HCC6
			FROM BATSUM
			JOIN GroupHC ON BATSUM.[CASE] = GroupHC.[Case]
		)

		SELECT 
			*
			--AVG(HCC4) , AVG(HCC6)
		FROM ByCase