
--DROP TABLE Summary_Losses
--DROP TABLE Losses
CREATE OR ALTER   PROCEDURE [dbo].[spGenerateLossesTables]
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('Summary_Losses', 'Losses')
				)
		)
	BEGIN
		DELETE FROM Losses
		DBCC CHECKIDENT('Losses', RESEED, 0)
		DELETE FROM Summary_Losses
		DBCC CHECKIDENT('Summary_Losses', RESEED, 0)
	END
	ELSE
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE Summary_Losses (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Simulation int,
			Monitor varchar(50),
			Elemento varchar(50),
			Loss float
		);
	END

	IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME = 'Losses')
		)
	BEGIN
		CREATE TABLE Losses (
			id int PRIMARY KEY IDENTITY(1,1),
			id_Summary int,
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);

		ALTER TABLE Losses
		ADD CONSTRAINT fk_LossesSummaryLosses FOREIGN KEY (id_Summary) REFERENCES Summary_Losses (id)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the Sumarry_Losses table
	-----------------------------------------------------------------------------
	INSERT INTO Summary_Losses
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
	-- DESCRIPTION: This query will populate the Losses table
	-----------------------------------------------------------------------------

	INSERT INTO Losses
		(id_Summary, TimeStep, Measurement, [Value])
	SELECT
		SL.id AS id_Summary,
		MD2.TimeStep AS TimeStep,
		MD2.Measurement AS Measurement,
		MD2.[Value] AS [Value]

	FROM Summary_Losses AS SL WITH (NOLOCK)
	join MonitoresData_2 AS MD2  WITH (NOLOCK)
		ON SL.[Case] = MD2.[Case]
		   and SL.Simulation = MD2.Simulation
		   and SL.Monitor = MD2.Monitor
		   and SL.Elemento = MD2.Elemento
	WHERE Measurement LIKE ' watts'
	ORDER BY Measurement, id_Summary, TimeStep
END
