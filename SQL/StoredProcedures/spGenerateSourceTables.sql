

CREATE OR ALTER   PROCEDURE [dbo].[spGenerateSourceTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('Summary_Source', 'Source')
				)
		)
	BEGIN
		DELETE FROM Source
		DBCC CHECKIDENT('Source', RESEED, 0)
		DELETE FROM Summary_Source
		DBCC CHECKIDENT('Summary_Source', RESEED, 0)
	END
	ELSE
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE Summary_Source (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50)
			-- Adicionar aqui
		);
	END

	IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME = 'Source')
		)
	BEGIN
		CREATE TABLE Source (
			id int PRIMARY KEY IDENTITY(1,1),
			id_Summary int,
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);

		ALTER TABLE Source
		ADD CONSTRAINT fk_SourceSummarySource FOREIGN KEY (id_Summary) REFERENCES Summary_Source (id)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO Summary_Source
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
	INSERT INTO Source
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SI.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM Summary_Source AS SI WITH (NOLOCK)
	join MonitoresData_2 AS MD2 WITH (NOLOCK)
		ON SI.[Case] = MD2.[Case]
		   and SI.Simulation = MD2.Simulation
		   and SI.Elemento = MD2.Elemento
		   and SI.Monitor = MD2.Monitor
	WHERE Measurement in (' vars', ' watts',
	' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)')
	ORDER BY Measurement, id_Summary, TimeStep

END

