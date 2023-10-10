





SELECT 
	TimeStep
	, AVG(PV_Power) AS AVG_PV_Power_By_TimeStep
	, AVG(BESS_Power) AS AVG_BESS_Power_By_TimeStep
	, AVG(Total_Power) AS AVG_Total_Power_By_TimeStep
FROM vwGetPowerToHCCalculation4
where TimeStep = 30
GROUP BY TimeStep
ORDER BY TimeStep





select 
--*
 AVG(PV_Power) AS AVG_PV_Power_By_TimeStep
, AVG(BESS_Power) AS AVG_BESS_Power_By_TimeStep
, AVG(Total_Power) AS AVG_Total_Power_By_TimeStep
from vwGetPowerToHCCalculation4
where TimeStep = 30