--------------------------------------------------------------------------------------
-- This view aims to group all active power values related to the data source
-- during NO PV operation. This will deliver the maximum power and daily energy 
-- consumed by the loads.
--
-- Use the following query to obtain the results after define the view
--
--SELECT 
--	MIN(SumOfPowerValues),
--	SUM(SumOfEnergyValues)
--FROM vwSourcePowerDataMeasurements
--
-------------------------------------------------------------------------------------
CREATE OR ALTER VIEW vwSourceActivePowerDataMeasurements AS
	WITH 
	P1 AS (
		SELECT 
			*
		FROM tblMonitoresData
		WHERE
			[Case] = 1 AND Simulation = 1
			AND Elemento = 'vsource.source'
			AND Measurement = ' P1 (kW)'
		),
	P2 AS (
		SELECT 
			*
		FROM tblMonitoresData
		WHERE
			[Case] = 1 AND Simulation = 1
			AND Elemento = 'vsource.source'
			AND Measurement = ' P2 (kW)'
		),
	P3 AS (
		SELECT 
			*
		FROM tblMonitoresData
		WHERE
			[Case] = 1 AND Simulation = 1
			AND Elemento = 'vsource.source'
			AND Measurement = ' P3 (kW)'
		)


	SELECT
		PP1, PP2, PP3,
		(PP1 + PP2 + PP3) AS SumOfPowerValues,
		(PP1 + PP2 + PP3) / 4 AS SumOfEnergyValues
	FROM (
		SELECT
			P1.[Value] AS PP1, P2.[Value] AS PP2, P3.[Value] AS PP3
		FROM P1 
		JOIN P2 ON P1.[Case] = P2.[Case] AND P1.Simulation = P2.Simulation AND P1.Monitor = P2.Monitor AND P1.Elemento = P2.Elemento AND P1.TimeStep = P2.TimeStep
		JOIN P3 ON P1.[Case] = P3.[Case] AND P1.Simulation = P3.Simulation AND P1.Monitor = P3.Monitor AND P1.Elemento = P3.Elemento AND P1.TimeStep = P3.TimeStep
	) AS SubqueryAlias;

