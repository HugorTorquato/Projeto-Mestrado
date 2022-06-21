


CREATE OR ALTER VIEW vwOvervoltageViolations
AS
	SELECT
		* 
	FROM MonitoresData_2
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] > 220/SQRT(3) * 1.05

GO

CREATE OR ALTER VIEW vwUndervoltageViolations
AS
	SELECT
		* 
	FROM MonitoresData_2
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] < 220/SQRT(3) * 0.93

GO

CREATE OR ALTER VIEW vwCurrentViolations
AS
	-- Preciso de uma violação de corrente para testar
	SELECT
		MD2.Nome_ID
		,MD2.[Case]
		,MD2.Simulation
		,MD2.Monitor
		,MD2.Elemento
		,MD2.TimeStep
		,MD2.Measurement
		,MD2.[Value]
		,ED.[Value] AS 'Current_Limit'
	FROM MonitoresData_2 MD2
	JOIN Elements_Data ED ON MD2.Elemento = ED.Element
	WHERE 
		MD2.Elemento LIKE 'line.%'
		AND MD2.Measurement IN (' I1', ' I2', ' I3')
		AND MD2.[Value] > ED.[Value]
GO

--CREATE OR ALTER VIEW vwUnbalanceViolations
--AS 
--	PRINT('Sei o que fazer não, espero não precisar kkk')
--GO
