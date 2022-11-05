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
	FROM tblMonitoresData MD2
	JOIN tblElements_Data ED ON MD2.Elemento = ED.Element
	WHERE 
		MD2.Elemento LIKE 'line.%'
		AND MD2.Measurement IN (' I1', ' I2', ' I3')
		AND MD2.[Value] > ED.[Value]