
CREATE OR ALTER VIEW vwCreateSUMProcessedPVPowerDataDiffTable
AS
	WITH
	P1 AS (
		SELECT * 
		FROM spProcessedPVPowerDataDiff
		WHERE Measurement like ' P1 (kW)'
	),

	P2 AS (
		SELECT * 
		FROM spProcessedPVPowerDataDiff
		WHERE Measurement like ' P2 (kW)'
	),

	P3 AS (
		SELECT * 
		FROM spProcessedPVPowerDataDiff
		WHERE Measurement like ' P3 (kW)'
	)

	SELECT 
		DISTINCT(P1.[Case])
		, P1.Elemento
		, P1.TimeStep
		, (ISNULL(P1.Value_S5,0)  + ISNULL(P2.Value_S5,0) + ISNULL(P3.Value_S5,0)) AS Sum_Pot_5
		, (ISNULL(P1.Value_S4,0)  + ISNULL(P2.Value_S4,0) + ISNULL(P3.Value_S4,0)) AS Sum_Pot_4
		, (ISNULL(P1.Value_diff_5to4,0)  + ISNULL(P2.Value_diff_5to4,0) + ISNULL(P3.Value_diff_5to4,0)) AS Sum_Pot_Diff_5_4
		, (ISNULL(P1.Value_S7,0)  + ISNULL(P2.Value_S7,0) + ISNULL(P3.Value_S7,0)) AS Sum_Pot_7
		, (ISNULL(P1.Value_S6,0)  + ISNULL(P2.Value_S6,0) + ISNULL(P3.Value_S6,0)) AS Sum_Pot_6
		, (ISNULL(P1.Value_diff_7to6,0)  + ISNULL(P2.Value_diff_7to6,0) + ISNULL(P3.Value_diff_7to6,0)) AS Sum_Pot_Diff_7_6
	FROM P1
	FULL JOIN P2
		ON P1.[Case] = P2.[Case]
			AND P1.Elemento = P2.Elemento
			AND P1.TimeStep = P2.TimeStep
	FULL JOIN P3
		ON P1.[Case] = P3.[Case]
			AND P1.Elemento = P3.Elemento
			AND P1.TimeStep = P3.TimeStep

	--where P1.Elemento = 'pvsystem.pv_0' and p1.TimeStep = 24
