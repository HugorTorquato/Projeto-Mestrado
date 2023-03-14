
--DROP TABLE spSummary_InvControl
--DROP TABLE spInvControlData
CREATE OR ALTER   PROCEDURE [dbo].[spGenerateInvControlTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSummary_InvControl', 'spSummary_InvControlData')
				)
		)
	BEGIN
		DELETE FROM spSummary_InvControlData
		DBCC CHECKIDENT('spSummary_InvControlData', RESEED, 0)
		DELETE FROM spSummary_InvControl
		DBCC CHECKIDENT('spSummary_InvControl', RESEED, 0)
	END
	
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Sumarry_InvControl table
	-- TODO: Daria para colocar informações aqui, que não depende do Timestemp
	-----------------------------------------------------------------------------
	INSERT INTO spSummary_InvControl
		([Case], Simulation, Monitor, Elemento)
	SELECT DISTINCT
		[Case],
		Simulation,
		Monitor,
		Elemento
		-- Adicionar aqui
	FROM tblMonitoresData MD2 WITH (NOLOCK)
		WHERE Elemento like 'pvsystem%' 
		ORDER BY Simulation, [Case]

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Losses table
	-----------------------------------------------------------------------------
	INSERT INTO spSummary_InvControlData
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SI.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM spSummary_InvControl AS SI WITH (NOLOCK)
	join tblMonitoresData AS MD2 WITH (NOLOCK)
		ON SI.[Case] = MD2.[Case]
		   and SI.Simulation = MD2.Simulation
		   and SI.Elemento = MD2.Elemento
		   and SI.Monitor = MD2.Monitor
	WHERE Measurement in ('Vreg', 'volt-var', 'volt-watt', ' vars', ' watts',
	' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)')
	ORDER BY Measurement, id_Summary, TimeStep
	
	-----------------------------------------------------------------------------
	------------------------------ Validade DATA --------------------------------
	-----------------------------------------------------------------------------	
	--select * from MonitoresData_2
	--where Elemento like 'pvsystem.pv_8' and
	--	Measurement in ('Vreg', ' v1', ' v2', ' v3') and
	--	Simulation = 3 and TimeStep=50
	--
	--SELECT * FROM MonitoresData_2
	--where Elemento like 'pvsystem.pv_3' and
	--		Measurement in ('Vreg', 'volt-var', 'volt-watt') and
	--		Simulation = 5
END
