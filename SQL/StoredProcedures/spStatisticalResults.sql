
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
	ELSE
		BEGIN
			CREATE TABLE spStatisticalResults (
				id int PRIMARY KEY IDENTITY(1,1),
				Simulation int,
				Average float,
				StandardDeviation float
				-- PARA ADICIONAR MAIS TEM DE LISTAR AS COLUNAS AQUI
			)
		END
	-----------------------------------------------------------------------------
	IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spStatisticalData')
				)
		)
		BEGIN
			CREATE TABLE spStatisticalData (
				id int PRIMARY KEY IDENTITY(1,1),
				id_Results int,
				HC float
			)

			ALTER TABLE spStatisticalData
				ADD CONSTRAINT fk_spStatisticalResoultsspStatisticalData FOREIGN KEY (id_Results) 
					REFERENCES spStatisticalResoults (id)
		END
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	INSERT INTO spStatisticalResults
		(Simulation, Average, StandardDeviation)
	SELECT 
		DISTINCT G.SimulationCount AS Simulation,
		(SELECT AVG(HC) FROM General G2 WHERE G2.SimulationCount = G.SimulationCount) AS Average,
		(SELECT STDEVP(HC) FROM General G2 WHERE G2.SimulationCount = G.SimulationCount) AS StandardDeviation
		-- PARA ADICIONAR MAIS TEM DE LISTAR AS CONSULTAS AQUI
	FROM General G WHERE G.SimulationCount > 1

	-----------------------------------------------------------------------------

	INSERT INTO spStatisticalData
		(id_Results, HC)
	SELECT
		SR.Simulation AS Simulation,
		G2.HC AS HC
	FROM spStatisticalResults SR
	JOIN General G2 ON G2.SimulationCount = SR.Simulation
	ORDER BY SR.Simulation
END
