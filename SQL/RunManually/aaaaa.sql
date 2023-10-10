



select * from vwGetVVVWControlActivation

CREATE OR ALTER VIEW vwFindBusMostCommonActivations
AS
	SELECT
		VVVWC.[id],
		VVVWC.[Case],
		VVVWC.Simulation,
		VVVWC.Elemento
		--PVS.Bus
	FROM vwGetVVVWControlActivation VVVWC with (nolock) 
	LEFT JOIN tblPVSystems PVS with (nolock) 
		ON 
			PVS.[Case] = VVVWC.[Case]
			AND PVS.Simulation = VVVWC.Simulation
			AND PVS.[Name] = VVVWC.Elemento



			select * from vwGetVVVWControlActivation WHERE [CASE] = 45





select
	DISTINCT(Bus)
from 
	(SELECT
	VVVWC.[id],
	VVVWC.[Case],
	VVVWC.Simulation,
	VVVWC.Elemento,
	PVS.Bus
FROM vwGetVVVWControlActivation VVVWC
LEFT JOIN tblPVSystems PVS 
	ON 
		PVS.[Case] = VVVWC.[Case]
		AND PVS.Simulation = VVVWC.Simulation
	AND PVS.[Name] = VVVWC.Elemento ) as a



SELECT Bus, COUNT(*) AS Count
FROM 

	(SELECT
	VVVWC.[id],
	VVVWC.[Case],
	VVVWC.Simulation,
	VVVWC.Elemento,
	PVS.Bus
FROM vwGetVWControlActivation VVVWC
LEFT JOIN tblPVSystems PVS 
	ON 
		PVS.[Case] = VVVWC.[Case]
		AND PVS.Simulation = VVVWC.Simulation
	    AND PVS.[Name] = VVVWC.Elemento ) as a


GROUP BY Bus
Order by Count