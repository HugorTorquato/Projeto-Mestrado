---------------------------------------------------------
-- This view returns all the cases that a partial
-- activation happened for VV control. Duo the unit 
-- reached its limit and the priority is the active
-- power
---------------------------------------------------------

CREATE OR ALTER VIEW vwPartialVVActivation
AS
	SELECT
	*
	FROM dbo.spSummary_InvControl SI
	WHERE SI.id IN 
		(
		SELECT 
			DISTINCT(id_Summary)
		FROM spSummary_InvControlData 
		WHERE 
			(Measurement like 'volt-var')
			AND 
			([Value] > 0 AND [Value] < 1
			OR [Value] < 0 AND [Value] > -1)
		)
		AND SI.Simulation <> 5 AND SI.Simulation <> 7