

CREATE OR ALTER   PROCEDURE [dbo].[spGenerateSourceTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSummary_Source', 'spSourceData')
				)
		)
	BEGIN
		DELETE FROM spSourceData
		DBCC CHECKIDENT('spSourceData', RESEED, 0)
		DELETE FROM spSummary_Source
		DBCC CHECKIDENT('spSummary_Source', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO spSummary_Source
		([Case], Simulation, Monitor, Elemento)
	SELECT DISTINCT
			[Case],
			Simulation,
			Monitor,
			Elemento
			-- Adicionar aqui
		FROM MonitoresData_2 MD2 WITH (NOLOCK)
			WHERE Elemento in ('vsource.source', 'transformer.t1') 
			ORDER BY Simulation, [Case]

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Losses table
	-----------------------------------------------------------------------------
	INSERT INTO spSourceData
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SI.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM spSummary_Source AS SI WITH (NOLOCK)
	join MonitoresData_2 AS MD2 WITH (NOLOCK)
		ON SI.[Case] = MD2.[Case]
		   and SI.Simulation = MD2.Simulation
		   and SI.Elemento = MD2.Elemento
		   and SI.Monitor = MD2.Monitor
	WHERE Measurement in (' vars', ' watts',
	' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)')
	ORDER BY Measurement, id_Summary, TimeStep

END

