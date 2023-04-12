---------------------------------------------------------
-- This view creates a summay demand table,
-- each element's power are group togheter devided by
-- Case, Simulation and TimeStep. The second group by
-- aims to onsolidate the average value for each demand 
-- in a diferent TimStep byt for all 50 Cases simulated
---------------------------------------------------------
CREATE OR ALTER VIEW vwAVGDemandBySimulation
AS
	WITH 
		KW_BY_CASE_Load AS (
			SELECT 
				[Case]
				, Simulation
				, TimeStep
				-- Sum all loads power measures ( All phases ) from each TimeStep, Simulation and Case
				, SUM([Value]) as SUM_ALL_KW
			FROM ( SELECT *
					FROM tblMonitoresData WITH(NOLOCK)
					WHERE Elemento like 'load.%'
							AND Measurement LIKE '%(kW)'
				) AS KW_Loads
			GROUP BY [Case], Simulation, TimeStep
		),
		KW_BY_CASE_pv AS (
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
		KBCPV.Simulation
		, KBCPV.TimeStep
		, AVG(KBCL.SUM_ALL_KW) as AVG_ALL_LOAD_KW
		, AVG(KBCPV.SUM_ALL_KW) as AVG_ALL_PV_KW
		, AVG(KBCL.SUM_ALL_KW) - AVG(KBCPV.SUM_ALL_KW) as DIFF_AVG_LOAD_MINUS_PV
	FROM KW_BY_CASE_Load KBCL
	JOIN KW_BY_CASE_pv KBCPV 
		ON KBCPV.Simulation = KBCL.Simulation 
			AND KBCPV.TimeStep = KBCL.TimeStep 
	GROUP BY KBCPV.Simulation, KBCPV.TimeStep
	--ORDER BY Simulation, TimeStep