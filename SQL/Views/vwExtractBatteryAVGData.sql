---------------------------------------------------------
-- This view creates a summay Baterry params. It will
-- return the average Pot, Energy and Energy loss for
-- VW and VV+VW controls. Average value from SUM of all
-- PV units for a case.
-- For now it is been used just to aggregate the plot
-- VWHCDiff.
---------------------------------------------------------

CREATE OR ALTER VIEW vwExtractBatteryAVGData
AS
	WITH TEMPWHTABLE_5_4 AS (
		SELECT 
			[Case],
			SUM(MAX_Pot_Diff_5_4_W) AS SUM_W_5_4,
			SUM(MAX_Eergy_Diff_5_4_Wh) AS SUM_WH_5_4,
			SUM(ADJ_Battery_Capacity_5_4) AS SUM_Cap_5_4
		FROM spBatterySummary GROUP BY [Case]
		),
		TEMPWHTABLE_7_6 AS (
		SELECT 
			[Case],
			SUM(MAX_Pot_Diff_7_6_W) AS SUM_W_7_6,
			SUM(MAX_Eergy_Diff_7_6_Wh) AS SUM_WH_7_6,
			SUM(ADJ_Battery_Capacity_7_6) AS SUM_Cap_7_6
		FROM spBatterySummary GROUP BY [Case]
		)

	SELECT 
		(SELECT AVG(SUM_WH_5_4) FROM TEMPWHTABLE_5_4) AS Avg_Energy_Loss_5_4,
		(SELECT AVG(SUM_WH_7_6) FROM TEMPWHTABLE_7_6) AS Avg_Energy_Loss_7_6,
		(SELECT AVG(SUM_Cap_5_4) FROM TEMPWHTABLE_5_4) AS Avg_Cap_Loss_5_4,
		(SELECT AVG(SUM_Cap_7_6) FROM TEMPWHTABLE_7_6) AS Avg_Cap_Loss_7_6,
		(SELECT AVG(SUM_W_5_4) FROM TEMPWHTABLE_5_4) AS Avg_Pot_Loss_5_4,
		(SELECT AVG(SUM_W_7_6) FROM TEMPWHTABLE_7_6) AS Avg_Pot_Loss_7_6
	