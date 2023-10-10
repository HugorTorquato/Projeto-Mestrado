


--- Searar em duas views antes de salvar



CREATE OR ALTER VIEW vwGetPowerToHCCalculation4
AS
	WITH 
		GroupPowerDiff AS (
			SELECT 
				[Case],
				TimeStep,
				SUM(Sum_Pot_Diff_5_4) AS Diff_Pot_4_All_PVs
			FROM spSUMProcessedPVPowerDataDiff
			GROUP BY TimeStep, [Case]
		),
		GroupPVPowerPower AS (
			SELECT
				*
			FROM spTimeStempOvrViewData SPPGD  WITH (NOLOCK)
			WHERE Simulation = 4
		)
		--OverallPower AS (
			SELECT
				GPVPP.[Case],
				GPVPP.Simulation,
				GPVPP.TimeStep,
				- GPVPP.Sum_Pot_W / 1000 AS PV_Power,
				GPD.Diff_Pot_4_All_PVs AS BESS_Power,
				( - GPVPP.Sum_Pot_W / 1000 + GPD.Diff_Pot_4_All_PVs) AS Total_Power
			FROM GroupPVPowerPower AS GPVPP
			JOIN GroupPowerDiff AS GPD 
				ON GPVPP.[Case] = GPD.[Case] AND GPVPP.TimeStep = GPD.TimeStep

GO

CREATE OR ALTER VIEW vwGetPowerToHCCalculation6
AS
	WITH 
		GroupPowerDiff AS (
			SELECT 
				[Case],
				TimeStep,
				SUM(Sum_Pot_Diff_7_6) AS Diff_Pot_6_All_PVs
			FROM spSUMProcessedPVPowerDataDiff
			GROUP BY TimeStep, [Case]
		),
		GroupPVPowerPower AS (
			SELECT
				*
			FROM spTimeStempOvrViewData SPPGD  WITH (NOLOCK)
			WHERE Simulation = 6
		)
		--OverallPower AS (
			SELECT
				GPVPP.[Case],
				GPVPP.Simulation,
				GPVPP.TimeStep,
				- GPVPP.Sum_Pot_W / 1000 AS PV_Power,
				GPD.Diff_Pot_6_All_PVs AS BESS_Power,
				( - GPVPP.Sum_Pot_W / 1000 + GPD.Diff_Pot_6_All_PVs) AS Total_Power
			FROM GroupPVPowerPower AS GPVPP
			JOIN GroupPowerDiff AS GPD 
				ON GPVPP.[Case] = GPD.[Case] AND GPVPP.TimeStep = GPD.TimeStep