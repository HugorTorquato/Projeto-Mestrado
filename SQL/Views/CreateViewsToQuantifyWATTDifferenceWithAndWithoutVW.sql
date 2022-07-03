
CREATE OR ALTER VIEW vwWattDiffControllVWOnly
AS
	SELECT 
		MD2_1.[Case]
		,MD2_1.TimeStep
		--,MD2_2.TimeStep
		,MD2_1.Elemento
		--,MD2_2.Elemento
		,MD2_1.Measurement
		--,MD2_2.Measurement
		,MD2_1.Simulation AS Simulation_With_VW
		,MD2_1.[Value]  AS Value_With_VW
		,MD2_2.Simulation  AS Simulation_Without_VW
		,MD2_2.[Value]  AS Value_Without_VW
		, (SELECT MD2_1.[Value] - MD2_2.[Value]) AS Diff
	FROM MonitoresData_2 MD2_1
	INNER JOIN MonitoresData_2 MD2_2 
		ON 
			MD2_1.Elemento = MD2_2.Elemento 
			AND MD2_1.TimeStep = MD2_2.TimeStep
			AND MD2_1.Measurement = MD2_2.Measurement
	WHERE 
		MD2_1.Measurement LIKE ' watts'
		AND MD2_1.Elemento LIKE 'pvsystem.%'
		AND MD2_1.Simulation = 4
		AND MD2_2.Simulation = 5
GO

CREATE OR ALTER VIEW vwWattDiffControll_VVandVW
AS
	SELECT 
		MD2_1.[Case]
		,MD2_1.TimeStep
		--,MD2_2.TimeStep
		,MD2_1.Elemento
		--,MD2_2.Elemento
		,MD2_1.Measurement
		--,MD2_2.Measurement
		,MD2_1.Simulation AS Simulation_With_VW
		,MD2_1.[Value]  AS Value_With_VW
		,MD2_2.Simulation  AS Simulation_Without_VW
		,MD2_2.[Value]  AS Value_Without_VW
		, (SELECT MD2_1.[Value] - MD2_2.[Value]) AS Diff
	FROM MonitoresData_2 MD2_1
	INNER JOIN MonitoresData_2 MD2_2 
		ON 
			MD2_1.Elemento = MD2_2.Elemento 
			AND MD2_1.TimeStep = MD2_2.TimeStep
			AND MD2_1.Measurement = MD2_2.Measurement
	WHERE 
		MD2_1.Measurement LIKE ' watts'
		AND MD2_1.Elemento LIKE 'pvsystem.%'
		AND MD2_1.Simulation = 6
		AND MD2_2.Simulation = 7
GO