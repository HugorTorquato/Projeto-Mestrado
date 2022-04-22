
--DROP TABLE Summary_InvControl
--DROP TABLE InvControl
CREATE OR ALTER   PROCEDURE [dbo].[spGenerateInvControlTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('Summary_InvControl', 'InvControl')
				)
		)
	BEGIN
		DELETE FROM InvControl
		DBCC CHECKIDENT('InvControl', RESEED, 0)
		DELETE FROM Summary_InvControl
		DBCC CHECKIDENT('Summary_InvControl', RESEED, 0)
	END
	ELSE
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE Summary_InvControl (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50)
		);
	END

	IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME = 'InvControl')
		)
	BEGIN
		CREATE TABLE InvControl (
			id int PRIMARY KEY IDENTITY(1,1),
			id_Summary int,
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);

		ALTER TABLE InvControl
		ADD CONSTRAINT fk_InvControlSummaryInvControl FOREIGN KEY (id_Summary) REFERENCES Summary_InvControl (id)
	END
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Sumarry_InvControl table
	-- TODO: Daria para colocar informações aqui, que não depende do Timestemp
	-----------------------------------------------------------------------------
	INSERT INTO Summary_InvControl
		([Case], Simulation, Monitor, Elemento)
	SELECT DISTINCT
		[Case],
		Simulation,
		Monitor,
		Elemento
		-- Adicionar aqui
	FROM MonitoresData_2 MD2 WITH (NOLOCK)
		WHERE Elemento like 'pvsystem%' 
			  and Monitor like 'invcontrol%' 
		ORDER BY Simulation, [Case]

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Losses table
	-----------------------------------------------------------------------------
	INSERT INTO InvControl
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SI.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM Summary_InvControl AS SI WITH (NOLOCK)
	join MonitoresData_2 AS MD2 WITH (NOLOCK)
		ON SI.[Case] = MD2.[Case]
		   and SI.Simulation = MD2.Simulation
		   and SI.Monitor = MD2.Monitor
		   and SI.Elemento = MD2.Elemento
	WHERE Measurement in ('Vreg', 'volt-var', 'volt-watt')
	ORDER BY Measurement, id_Summary, TimeStep
END
