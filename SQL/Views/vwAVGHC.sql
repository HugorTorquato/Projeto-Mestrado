CREATE OR ALTER VIEW vwAVGHC
AS
	select top 1
		(select AVG(HC) from General where SimulationCount = 1) AS Sim_1
		, (select AVG(HC) from General where SimulationCount = 2) AS Sim_2
		, (select AVG(HC) from General where SimulationCount = 3) AS Sim_3
		, (select AVG(HC) from General where SimulationCount = 4) AS Sim_4
		, (select AVG(HC) from General where SimulationCount = 5) AS Sim_5
	from General G