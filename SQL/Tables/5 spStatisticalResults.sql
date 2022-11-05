-----------------------------------------------------------------------------
-- spStatisticalResults definition
--		Define a statistical results table to centralize this kind of results
-- Idea here is to create an overview for the full simulation
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spStatisticalResults')
				)
		)
		BEGIN
			CREATE TABLE spStatisticalResults (
				id int PRIMARY KEY IDENTITY(1,1),
				Simulation int,
				Average float,
				StandardDeviation float
				-- PARA ADICIONAR MAIS TEM DE LISTAR AS COLUNAS AQUI
			)
		END