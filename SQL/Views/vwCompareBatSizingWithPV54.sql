---------------------------------------------------------
-- This view aims to generate compare data between
-- Baterry sizing and PV elements for the same case and
-- Simulation.
---------------------------------------------------------

CREATE OR ALTER VIEW vwCompareBatSizingWithPV54
AS
	WITH 
	GROUPPVANDBAT_5_4 AS (
		SELECT
			PV.[Case],
			PV.Simulation,
			PV.kva,
			PV.Phases,
			PV.[Name],
			BS.MAX_Pot_Diff_5_4_W,
			BS.ADJ_Battery_Capacity_5_4
		FROM tblPVSystems PV
		INNER JOIN spBatterySummary BS 
			ON PV.[Name] = BS.Elemento
				AND PV.[Case] = BS.[Case]
		WHERE PV.Simulation = 4 -- vw
	)

	SELECT 
		[Case],
		Simulation,
		kva,
		Phases,
		[Name],
		MAX_Pot_Diff_5_4_W,
		ADJ_Battery_Capacity_5_4,
		CASE WHEN MAX_Pot_Diff_5_4_W > 0 THEN ROUND( 100 * ADJ_Battery_Capacity_5_4 / MAX_Pot_Diff_5_4_W ,2) ELSE 0 END AS EnergByPot,
		CASE WHEN kva > 0 THEN ROUND( 100 * MAX_Pot_Diff_5_4_W / kva , 2) ELSE 0 END AS MaxPotByPVSize
	FROM GROUPPVANDBAT_5_4
	WHERE
		ADJ_Battery_Capacity_5_4 > 10
		AND MAX_Pot_Diff_5_4_W > 10;