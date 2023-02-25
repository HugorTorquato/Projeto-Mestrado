

CREATE OR ALTER VIEW vwCreateProcessedPVPowerDataDiffTable
AS

-- Returns power data for all 3 phases for simulation 5
		WITH 
		S5 AS (
			SELECT *
			FROM tblMonitoresData
			WHERE Elemento like 'pvsystem.pv%'
					AND Simulation = 5
					AND Measurement LIKE '%(kW)'
		),

		-- Returns power data for all 3 phases for simulation 4
		S4 AS (
			SELECT *
			FROM tblMonitoresData
			WHERE Elemento like 'pvsystem.pv%'
					AND Simulation = 4
					AND Measurement LIKE '%(kW)'
		),

		S7 AS (
			SELECT *
			FROM tblMonitoresData
			WHERE Elemento like 'pvsystem.pv%'
					AND Simulation = 7
					AND Measurement LIKE '%(kW)'
		),

		-- Returns power data for all 3 phases for simulation 4
		S6 AS (
			SELECT *
			FROM tblMonitoresData
			WHERE Elemento like 'pvsystem.pv%'
					AND Simulation = 6
					AND Measurement LIKE '%(kW)'
		),

		-- Create a temp table to store and combine values from simulation 4 and 5
		COMBDATA1 AS (
			SELECT 
				S5.[Case]
				, S5.Elemento 
				, S5.Measurement AS M5
				, S4.Measurement AS M4
				, S5.TimeStep
				, -S5.[Value] as Value_S5
				, -S4.[Value] as Value_S4
			FROM S5
			JOIN S4 ON 
				S5.[Case] = S4.[Case]
				AND S5.Elemento = S4.Elemento
				AND S5.Measurement = S4.Measurement
				AND S5.TimeStep = S4.TimeStep
		),

		COMBDATA2 AS (
			SELECT 
				S7.[Case]
				, S7.Elemento 
				, S7.Measurement AS M7
				, S6.Measurement AS M6
				, S7.TimeStep
				, -S7.[Value] as Value_S7
				, -S6.[Value] as Value_S6
			FROM S7
			JOIN S6 ON 
				S7.[Case] = S6.[Case]
				AND S7.Elemento = S6.Elemento
				AND S7.Measurement = S6.Measurement
				AND S7.TimeStep = S6.TimeStep
		)

		-- Actual calculation for those new tables, we have the difference here
		-- since we will use it for plot, i decided to create a table for that
		-- and this process time would only be needed once
		SELECT 
			DISTINCT(CD1.[Case])
			, CD1.Elemento
			, CD1.M5 AS Measurement
			--, CD1.M4
			, CD1.TimeStep
			, CD1.Value_S5
			, CD1.Value_S4
			, (CD1.Value_S5 - CD1.Value_S4) AS Value_diff_5to4
			, CD2.Value_S7
			, CD2.Value_S6
			, (CD2.Value_S7 - CD2.Value_S6) AS Value_diff_7to6
		FROM COMBDATA1 AS CD1
		JOIN COMBDATA2 AS CD2 ON
			CD1.[Case] = CD2.[Case]
			AND CD1.Elemento = CD2.Elemento
			AND CD1.TimeStep = CD2.TimeStep
			AND CD1.M4 = CD2.M6
			AND CD1.M5 = CD2.M7