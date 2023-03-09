--DROP TABLE Summary_InvControl
--DROP TABLE InvControl
CREATE OR ALTER   PROCEDURE [dbo].[spCreateViewsToQuantifyWATTDifferenceWithAndWithoutVW]
AS
BEGIN

	-----------------------------------------------------------------------------
	---------------------------- REMOVE OLD DATA --------------------------------
	-----------------------------------------------------------------------------
	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spWattDiffControllVWOnly', 'spWattDiffControll_VVandVW')
				)
		)
	BEGIN
		DELETE FROM spWattDiffControllVWOnly
		DBCC CHECKIDENT('spWattDiffControllVWOnly', RESEED, 0)
		DELETE FROM spWattDiffControll_VVandVW
		DBCC CHECKIDENT('spWattDiffControll_VVandVW', RESEED, 0)
	END
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the spWattDiffControllVWOnly table

	-- TODO: 
		-- 
	-----------------------------------------------------------------------------
	INSERT INTO spWattDiffControllVWOnly
	SELECT 
		MD2_1.[Case]
		, MD2_1.TimeStep
		--,MD2_2.TimeStep
		, MD2_1.Elemento
		--,MD2_2.Elemento
		, MD2_1.Measurement
		--,MD2_2.Measurement
		, MD2_1.Simulation AS Simulation_With_VW
		, MD2_1.[Value]  AS Value_With_VW
		, MD2_2.Simulation  AS Simulation_Without_VW
		, MD2_2.[Value]  AS Value_Without_VW
		, (SELECT MD2_1.[Value] - MD2_2.[Value]) AS Diff
		, (CASE
			WHEN MD2_2.[Value] < 0 THEN ROUND(ABS(MD2_1.[Value] - MD2_2.[Value]) * 100 / -MD2_2.[Value], 2)
			ELSE 0
		   END) AS 'Diff(%)' -- Porcentage from max active power generated
	FROM tblMonitoresData MD2_1 WITH (NOLOCK)
	INNER JOIN tblMonitoresData MD2_2 WITH (NOLOCK)
		ON 
			MD2_1.Elemento = MD2_2.Elemento 
			AND MD2_1.TimeStep = MD2_2.TimeStep
			AND MD2_1.[Case] = MD2_2.[Case]
			AND MD2_1.Measurement = MD2_2.Measurement
	WHERE 
		MD2_1.Measurement LIKE ' watts'
		AND MD2_1.Elemento LIKE 'pvsystem.%'
		AND MD2_1.Simulation = 4
		AND MD2_2.Simulation = 5
	ORDER BY
		MD2_1.[Case]

	-----------------------------------------------------------------------------
	-- DESCRIPTION: This query will populate the spWattDiffControll_VVandVW table

	-- TODO: 
		-- 
	-----------------------------------------------------------------------------
	INSERT INTO spWattDiffControll_VVandVW
	SELECT 
		MD2_1.[Case]
		, MD2_1.TimeStep
		--,MD2_2.TimeStep
		, MD2_1.Elemento
		--,MD2_2.Elemento
		, MD2_1.Measurement
		--,MD2_2.Measurement
		, MD2_1.Simulation AS Simulation_With_VW
		, MD2_1.[Value]  AS Value_With_VW
		, MD2_2.Simulation  AS Simulation_Without_VW
		, MD2_2.[Value]  AS Value_Without_VW
		, (SELECT MD2_1.[Value] - MD2_2.[Value]) AS Diff
		, (CASE
			WHEN MD2_2.[Value] < 0 THEN ROUND(ABS(MD2_1.[Value] - MD2_2.[Value]) * 100 / -MD2_2.[Value], 2)
			ELSE 0
		   END) AS 'Diff(%)' -- Porcentage from max active power generated
	FROM tblMonitoresData MD2_1 WITH (NOLOCK)
	INNER JOIN tblMonitoresData MD2_2 WITH (NOLOCK) 
		ON 
			MD2_1.Elemento = MD2_2.Elemento 
			AND MD2_1.TimeStep = MD2_2.TimeStep
			AND MD2_1.[Case] = MD2_2.[Case]
			AND MD2_1.Measurement = MD2_2.Measurement
	WHERE 
		MD2_1.Measurement LIKE ' watts'
		AND MD2_1.Elemento LIKE 'pvsystem.%'
		AND MD2_1.Simulation = 6
		AND MD2_2.Simulation = 7
	ORDER BY
		MD2_1.[Case]
END