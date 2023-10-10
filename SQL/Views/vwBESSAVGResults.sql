------------------------------------------------------------------------------------------------------------------------------------
-- This VIEW aims to aggregate base BESS sizing results to be presented in a boxplot.
-- It contains:
-- -Average Max Active power diference ( 5 -> 4 and 7 -> 6 ) 
-- -Average Max Energy diference       ( 5 -> 4 and 7 -> 6 ) 
-- -Average Sum Energy diference       ( 5 -> 4 and 7 -> 6 ) 
------------------------------------------------------------------------------------------------------------------------------------
CREATE OR ALTER VIEW vwBESSAVGResults
AS
	SELECT 
		DISTINCT [CASE],
		(SELECT AVG(SBS2.MAX_Pot_Diff_5_4_W)    FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS AVG_MAX_Pot_Diff_5_4,
		(SELECT AVG(SBS2.MAX_Pot_Diff_7_6_W)    FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS AVG_MAX_Pot_Diff_7_6,
		(SELECT AVG(SBS2.MAX_Eergy_Diff_5_4_Wh) FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS AVG_MAX_Eergy_Diff_5_4,
		(SELECT AVG(SBS2.MAX_Eergy_Diff_7_6_Wh) FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS AVG_MAX_Eergy_Diff_7_6,
		(SELECT AVG(SBS2.ADJ_Battery_Capacity_5_4) FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS ADJ_Battery_Capacity_5_4,
		(SELECT AVG(SBS2.ADJ_Battery_Capacity_7_6) FROM spBatterySummary SBS2 WHERE SBS.[CASE] = SBS2.[CASE]) AS ADJ_Battery_Capacity_7_6
	FROM spBatterySummary SBS