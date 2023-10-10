






--- a POT DAS CARGAR SERIA A MEDIÇÃO DE POT NO TRAFO... JÁ SOMA TUDO  BOAS

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
								AND Simulation = 1
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
								AND Simulation = 1
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
								AND Simulation = 1
								AND Measurement = ' P3 (kW)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),

-------------------------------------------------------------------------
	TPData6_Q1 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_Q1_TPD
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
								AND Simulation = 1
								AND Measurement = ' Q1 (kvar)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),
	TPData6_Q2 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_Q2_TPD
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
								AND Simulation = 1
								AND Measurement = ' Q2 (kvar)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),
	TPData6_Q3 AS (
		
		SELECT
			AUXILIAR_TPData6.TimeStep
			, AVG(AUXILIAR_TPData6.[Value]) AS AVG_Q3_TPD
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
								AND Simulation = 1
								AND Measurement = ' Q3 (kvar)'
							)
			) AS AUXILIAR_TPData6
		GROUP BY AUXILIAR_TPData6.TimeStep
		--ORDER BY AUXILIAR_TPData6.TimeStep
	),

-------------------------------------------------------------------------		
	GROUP_LOAD AS (
		SELECT
			TPData6_P1.TimeStep
			, TPData6_Q1.AVG_Q1_TPD
			, TPData6_Q2.AVG_Q2_TPD
			, TPData6_Q3.AVG_Q3_TPD
			-- Não entrei nesse merito no texto
			, (TPData6_P1.AVG_P1_TPD + TPData6_P2.AVG_P2_TPD + TPData6_P3.AVG_P3_TPD) AS SUM_P_TPD
			, (TPData6_Q1.AVG_Q1_TPD + TPData6_Q2.AVG_Q2_TPD + TPData6_Q3.AVG_Q3_TPD) AS SUM_Q_TPD
			, SQRT(
				POWER((TPData6_P1.AVG_P1_TPD + TPData6_P2.AVG_P2_TPD + TPData6_P3.AVG_P3_TPD), 2)
					+ POWER((TPData6_Q1.AVG_Q1_TPD + TPData6_Q2.AVG_Q2_TPD + TPData6_Q3.AVG_Q3_TPD), 2)
			) AS Aparant_ower_Load
		FROM TPData6_P1
		JOIN TPData6_P2 ON TPData6_P1.TimeStep = TPData6_P2.TimeStep
		JOIN TPData6_P3 ON TPData6_P1.TimeStep = TPData6_P3.TimeStep
		JOIN TPData6_Q1 ON TPData6_P1.TimeStep = TPData6_Q1.TimeStep
		JOIN TPData6_Q2 ON TPData6_P1.TimeStep = TPData6_Q2.TimeStep
		JOIN TPData6_Q3 ON TPData6_P1.TimeStep = TPData6_Q3.TimeStep

	)

	SELECT 
		*
	FROM GROUP_LOAD
	ORDER BY GROUP_LOAD.TimeStep