
CREATE OR ALTER PROCEDURE spAVGResoults
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------
	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spStatisticalData', 'spStatisticalResults')
				)
		)
		BEGIN
			DELETE FROM spStatisticalData
			DBCC CHECKIDENT('spStatisticalData', RESEED, 0)
			DELETE FROM spStatisticalResults
			DBCC CHECKIDENT('spStatisticalResults', RESEED, 0)
		END
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	INSERT INTO spStatisticalResults
		(Simulation, Average, StandardDeviation)
	SELECT 
		DISTINCT G.SimulationCount AS Simulation,
		(SELECT AVG(HC) FROM tblGeneral G2 WITH (NOLOCK) 
			WHERE G2.SimulationCount = G.SimulationCount AND HC < 2 AND HC > 0) AS Average,
		(SELECT STDEVP(HC) FROM tblGeneral G2 WITH (NOLOCK)
			WHERE G2.SimulationCount = G.SimulationCount AND HC < 2 AND HC > 0) AS StandardDeviation
		-- PARA ADICIONAR MAIS TEM DE LISTAR AS CONSULTAS AQUI
	FROM tblGeneral G WITH (NOLOCK) 
	WHERE G.SimulationCount > 1

	-----------------------------------------------------------------------------
	-- Já tenho essa informação em outro canto mas esse insert está com erro

	--INSERT INTO spStatisticalData
	--	([Case], id_Results, HC)
	--SELECT
	--	G2.[Case]
	--	,G2.SimulationCount AS Simulation
	--	,G2.HC AS HC
	--FROM spStatisticalResults SR WITH (NOLOCK)
	--JOIN tblGeneral G2 WITH (NOLOCK) ON G2.SimulationCount = SR.Simulation
	--ORDER BY G2.[Case], G2.SimulationCount
END
