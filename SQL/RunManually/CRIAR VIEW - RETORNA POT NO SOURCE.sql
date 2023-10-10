









WITH
	TPData6_P1 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_P1_TPD
		FROM (
			SELECT
			*
			FROM spSourceData
			WHERE 
				id_Summary in (
							SELECT
								[id]
							FROM spSummary_Source
							WHERE 
								Monitor = 'transformer_t1_power'
								AND Simulation = 6
								AND Measurement = ' P1 (kW)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),
	TPData6_P2 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_P2_TPD
		FROM (
			SELECT
			*
			FROM spSourceData
			WHERE 
				id_Summary in (
							SELECT
								[id]
							FROM spSummary_Source
							WHERE 
								Monitor = 'transformer_t1_power'
								AND Simulation = 6
								AND Measurement = ' P2 (kW)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),
	TPData6_P3 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_P3_TPD
		FROM (
			SELECT
			*
			FROM spSourceData
			WHERE 
				id_Summary in (
							SELECT
								[id]
							FROM spSummary_Source
							WHERE 
								Monitor = 'transformer_t1_power'
								AND Simulation = 6
								AND Measurement = ' P3 (kW)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	)

		
		SELECT
			TPData6_P1.TimeStep
			, TPData6_P1.AVG_P1_TPD
			, TPData6_P2.AVG_P2_TPD
			, TPData6_P3.AVG_P3_TPD
			-- Não entrei nesse merito no texto
			, (TPData6_P1.AVG_P1_TPD + TPData6_P1.AVG_P1_TPD + TPData6_P1.AVG_P1_TPD) / 3 AS AVG_P_TPD
			, SQRT(
				   ((TPData6_P1.AVG_P1_TPD - AVG(TPData6_P1.AVG_P1_TPD) OVER()) * (TPData6_P1.AVG_P1_TPD - AVG(TPData6_P1.AVG_P1_TPD) OVER()) +
					(TPData6_P2.AVG_P2_TPD - AVG(TPData6_P2.AVG_P2_TPD) OVER()) * (TPData6_P2.AVG_P2_TPD - AVG(TPData6_P2.AVG_P2_TPD) OVER()) +
					(TPData6_P3.AVG_P3_TPD - AVG(TPData6_P3.AVG_P3_TPD) OVER()) * (TPData6_P3.AVG_P3_TPD - AVG(TPData6_P3.AVG_P3_TPD) OVER())) / 3
			   ) AS std_deviation
		FROM TPData6_P1
		JOIN TPData6_P2 ON TPData6_P1.TimeStep = TPData6_P2.TimeStep
		JOIN TPData6_P3 ON TPData6_P1.TimeStep = TPData6_P3.TimeStep

		ORDER BY TPData6_P1.TimeStep
	--)