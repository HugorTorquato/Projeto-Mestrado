
-- Retorna somente para o caso(simulation) 4 e 6 VW e VVVW
--SELECT * FROM spTimeStempOvrViewData
--WHERE 
--	Simulation != 1 and Simulation != 2
--	and Simulation != 3 and Simulation != 5
--	and Simulation != 7 and Simulation != 6





WITH 
	GroupResults AS (
		SELECT
			[Case],
			MAX(PV_Power)/45 AS HC_PV,
			MAX(Total_Power)/45  AS HC_PV_BESS
		FROM vwGetPowerToHCCalculation4
		GROUP BY [Case]
	)

	SELECT 
		AVG(HC_PV) AS AVG_HV_PV,
		STDEV(HC_PV) AS STDEV_HV_PV,
		AVG(HC_PV_BESS) AS AVG_HC_PV_BESS,
		STDEV(HC_PV_BESS) AS STDEV_HC_PV_BESS
	FROM GroupResults

;WITH 
	GroupResults AS (
		SELECT
			[Case],
			MAX(PV_Power)/45 AS HC_PV,
			MAX(Total_Power)/45  AS HC_PV_BESS
		FROM vwGetPowerToHCCalculation6
		GROUP BY [Case]
	)

	SELECT 
		AVG(HC_PV) AS AVG_HV_PV,
		AVG(HC_PV_BESS) AS AVG_HC_PV_BESS
	FROM GroupResults




