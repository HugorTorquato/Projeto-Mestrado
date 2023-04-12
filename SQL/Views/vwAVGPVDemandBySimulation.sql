---------------------------------------------------------
-- This view creates a summay demand table for LOADS,
-- each element's power are group togheter devided by
-- Case, Simulation and TimeStep. The second group by
-- aims to onsolidate the average value for each demand 
-- in a diferent TimStep byt for all 50 Cases simulated
---------------------------------------------------------
CREATE OR ALTER VIEW vwAVGPVDemandBySimulation
AS
	WITH 
		KW_BY_CASE AS (
			SELECT 
				[Case]
				, Simulation
				, TimeStep
				-- Sum all loads power measures ( All phases ) from each TimeStep, Simulation and Case
				, -SUM([Value]) as SUM_ALL_KW
			FROM ( SELECT *
					FROM tblMonitoresData WITH(NOLOCK)
					WHERE Elemento like 'pvsystem.%'
							AND Measurement LIKE '%(kW)'
				) AS KW_Loads 
			GROUP BY [Case], Simulation, TimeStep
		)

	SELECT 
		Simulation
		, TimeStep
		-- Sum all loads power measures ( All phases ) from each TimeStep, Simulation
		, AVG(SUM_ALL_KW) as AVG_ALL_PV_KW
	FROM KW_BY_CASE
	GROUP BY Simulation, TimeStep
	--ORDER BY Simulation, TimeStep