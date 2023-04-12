---------------------------------------------------------
-- This view creates overview demand table,
-- it is based on Simulations as we already have the 
-- AVG resut using vwAVGDemandBySimulation view for all
-- cases. In this case we have the daily average demand
-- from loads, pv and the diference between them.
---------------------------------------------------------
CREATE OR ALTER VIEW vwSumarryDemandBySimulation
AS
	select 
		Simulation
		, ROUND(SUM(AVG_ALL_LOAD_KW) / 4, 2) AS Daily_Load_Demand
		, ROUND(SUM(AVG_ALL_PV_KW) / 4, 2) AS Daily_PV_Demand
		, ROUND(SUM(DIFF_AVG_LOAD_MINUS_PV) / 4, 2) AS Daily_Diff_Demand
	from vwAVGDemandBySimulation
	group by Simulation