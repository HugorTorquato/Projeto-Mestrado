


WITH 
	LP1 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' P1 (kW)' AND Simulation = 1
	),
	LP2 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' P2 (kW)' AND Simulation = 1
	),
	LP3 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' P3 (kW)' AND Simulation = 1
	),
	LQ1 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' Q1 (kvar)' AND Simulation = 1
	),
	LQ2 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' Q2 (kvar)' AND Simulation = 1
	),
	LQ3 AS (
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'load.c%' AND Measurement LIKE ' Q3 (kvar)' AND Simulation = 1
	),
	AllData AS (	
		SELECT -- * 
			LP1.[Case]
			, LP1.Simulation
			, LP1.Elemento
			, LP1.TimeStep
			, LP1.[Value] AS LP1_VALUE
			, LP2.[Value] AS LP2_VALUE
			, LP3.[Value] AS LP3_VALUE
			, LQ1.[Value] AS LQ1_VALUE
			, LQ2.[Value] AS LQ2_VALUE
			, LQ3.[Value] AS LQ3_VALUE

		FROM LP1
		FULL JOIN LP2 ON
			LP1.[Case] = LP2.[Case] AND LP1.Elemento = LP2.Elemento AND LP1.Monitor = LP2.Monitor AND LP1.TimeStep = LP2.TimeStep
		FULL JOIN LP3 ON
			LP1.[Case] = LP3.[Case] AND LP1.Elemento = LP3.Elemento AND LP1.Monitor = LP3.Monitor AND LP1.TimeStep = LP3.TimeStep
		FULL JOIN LQ1 ON
			LP1.[Case] = LQ1.[Case] AND LP1.Elemento = LQ1.Elemento AND LP1.Monitor = LQ1.Monitor AND LP1.TimeStep = LQ1.TimeStep
		FULL JOIN LQ2 ON
			LP1.[Case] = LQ2.[Case] AND LP1.Elemento = LQ2.Elemento AND LP1.Monitor = LQ2.Monitor AND LP1.TimeStep = LQ2.TimeStep
		FULL JOIN LQ3 ON
			LP1.[Case] = LQ3.[Case] AND LP1.Elemento = LQ3.Elemento AND LP1.Monitor = LQ3.Monitor AND LP1.TimeStep = LQ3.TimeStep
	),
	calc_loas_s AS (
		SELECT 
			AllData.[Case]
			, AllData.Simulation
			, AllData.Elemento
			, AllData.TimeStep
			, ( ISNULL(AllData.LP1_VALUE, 0) + ISNULL(AllData.LP2_VALUE, 0) + ISNULL(AllData.LP3_VALUE, 0)) AS Sum_P
			, ( ISNULL(AllData.LQ1_VALUE, 0) + ISNULL(AllData.LQ2_VALUE, 0) + ISNULL(AllData.LQ3_VALUE, 0)) AS Sum_Q
			, SQRT( POWER((ISNULL(AllData.LP1_VALUE, 0) + ISNULL(AllData.LP2_VALUE, 0) + ISNULL(AllData.LP3_VALUE, 0)), 2) + POWER((ISNULL(AllData.LQ1_VALUE, 0) + ISNULL(AllData.LQ2_VALUE, 0) + ISNULL(AllData.LQ3_VALUE, 0)), 2) ) AS sum_S
		FROM AllData
	),
	GroupDATA AS (


	SELECT 
		calc_loas_s.[Case]
		, MAX(calc_loas_s.Sum_S) AS Loas_S
		, sum(calc_loas_s.Sum_S) /4 AS Loas_S_energy
	FROM calc_loas_s

	GROUP BY calc_loas_s.[Case]
	--ORDER BY calc_loas_s.[Case]
	)

	SELECT 
		--* 
		AVG(Loas_S), AVG(Loas_S_energy)
	FROM GroupDATA
