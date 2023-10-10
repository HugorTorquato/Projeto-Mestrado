---------------------------------------------------------
-- This view aims to generate compare data between
-- Baterry sizing and PV elements for the same case and
-- Simulation.
---------------------------------------------------------



CREATE OR ALTER VIEW vwCompareBatSizingWithPV76
AS
	WITH 
	GROUPPVANDBAT_7_6 AS (
		SELECT
			PV.[Case],
			PV.Simulation,
			PV.kva,
			PV.Phases,
			PV.[Name],
			BS.MAX_Pot_Diff_7_6_W,
			BS.ADJ_Battery_Capacity_7_6
		FROM tblPVSystems PV
		INNER JOIN spBatterySummary BS 
			ON PV.[Name] = BS.Elemento
				AND PV.[Case] = BS.[Case]
		WHERE PV.Simulation = 6 -- vw
	)

	SELECT 
		[Case],
		Simulation,
		kva,
		Phases,
		[Name],
		MAX_Pot_Diff_7_6_W,
		ADJ_Battery_Capacity_7_6,
		CASE WHEN MAX_Pot_Diff_7_6_W > 0 THEN ROUND( 100 * ADJ_Battery_Capacity_7_6 / MAX_Pot_Diff_7_6_W ,2) ELSE 0 END AS EnergByPot,
		CASE WHEN kva > 0 THEN ROUND( 100 * MAX_Pot_Diff_7_6_W / kva , 2) ELSE 0 END AS MaxPotByPVSize
	FROM GROUPPVANDBAT_7_6
	WHERE
		ADJ_Battery_Capacity_7_6 > 10
		AND MAX_Pot_Diff_7_6_W > 10