
--DROP TABLE spSummary_Losses
--DROP TABLE spLossesData
CREATE OR ALTER   PROCEDURE [dbo].[spGenerateLossesTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSummary_Losses', 'spLossesData')
				)
		)
	BEGIN
		DELETE FROM spLossesData
		DBCC CHECKIDENT('spLossesData', RESEED, 0)
		DELETE FROM spSummary_Losses
		DBCC CHECKIDENT('spSummary_Losses', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Sumarry_Losses table
	-----------------------------------------------------------------------------
	INSERT INTO spSummary_Losses
		([Case], Simulation, Monitor, Elemento, Loss)
	SELECT DISTINCT
		[Case],
		Simulation,
		Monitor,
		Elemento,
		(SELECT sum([VALUE])/1000 FROM MonitoresData_2 MD
			WHERE Measurement like ' watts' 
				  and MD.Elemento = MD2.Elemento 
				  and MD.Simulation = MD2.Simulation 
				  and MD.[Case]= MD2.[Case] 
				  and MD.Monitor = MD2.Monitor) AS Loss
	FROM MonitoresData_2 MD2 WITH (NOLOCK)
		WHERE Elemento like 'line%' 
			  and Monitor like '%loss' 
		ORDER BY Simulation, [Case]
	-----------------------------------------------------------------------------
	-- Query para conferir os resultados, basta alterar os valores do filtro 

	--  select sum([VALUE])/1000 from MonitoresData_2 MD
	--	WHERE Measurement like ' watts' and 
	--	MD.Elemento = 'line._abcn_l03-sec'
	--	AND Simulation=1
	-----------------------------------------------------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the spLossesData table
	-----------------------------------------------------------------------------

	INSERT INTO spLossesData
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SL.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM spSummary_Losses AS SL WITH (NOLOCK)
	join MonitoresData_2 AS MD2  WITH (NOLOCK)
		ON SL.[Case] = MD2.[Case]
		   and SL.Simulation = MD2.Simulation
		   and SL.Monitor = MD2.Monitor
		   and SL.Elemento = MD2.Elemento
	WHERE Measurement LIKE ' watts'
	ORDER BY Measurement, id_Summary, TimeStep
END
