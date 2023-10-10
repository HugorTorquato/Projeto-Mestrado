---------------------------------------------------------
-- This view returns all the cases that a VV+VW control
-- were activated with its resective element and id. 
-- THe ID can be used to query spSummary_InvControlData
-- table and get detailed results reguarding control
-- activation for this specific situation
---------------------------------------------------------

CREATE OR ALTER VIEW vwGetVVVWControlActivation
AS
	-- Caso para identificar o VV+VW atuando só
	WITH 
	voltavar AS (
		SELECT 
				*--DISTINCT(id_Summary)
			FROM spSummary_InvControlData 
			WHERE 
				( Measurement like 'volt-var' AND [Value] <> 0 AND [Value] <> 9999)

	),
	voltawatt AS (
		SELECT 
			*--DISTINCT(id_Summary)
		FROM spSummary_InvControlData 
		WHERE 
			( Measurement like 'volt-watt' AND [Value] <> 0 AND [Value] <> 9999 )
	)

	-- Test the results and compare if they make sense
	--SELECT * 
	--		FROM voltavar AS VV
	--		JOIN voltawatt AS VW 
	--			ON 
	--				VV.id_Summary = VW.id_Summary
	--				AND VV.TimeStep = VW.TimeStep

	SELECT
		*
	FROM dbo.spSummary_InvControl SI
	WHERE Monitor LIKE 'invcontrol_pv_%'
		AND Simulation <> 5 and Simulation <> 7
		AND id in (
			SELECT DISTINCT(VV.id_Summary)--* 
			FROM voltavar AS VV
			JOIN voltawatt AS VW 
				ON 
					VV.id_Summary = VW.id_Summary
					AND VV.TimeStep = VW.TimeStep
			)