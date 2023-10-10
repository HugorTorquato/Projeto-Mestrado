---------------------------------------------------------
-- This view creates a summay Hosting Capacity table
-- with average HC and standard deviation by simulation.
-- Conservative_value collumn represents the HC value
-- minus standard deviation. I had to create this vew
-- because max SQL storage for a free version is 10GB 
-- and simuation reached that limit for 82 cases. Therefore,
-- each database listed in this JOIN conteins 50 
-- diferent cases.
---------------------------------------------------------
CREATE OR ALTER VIEW vwHCSummaryForAllDB
AS
	WITH
		V1 AS (
			SELECT 
				db1403.Simulation
				, (db1403.Average + db2303.Average) / 2 AS Average
				, (db1403.StandardDeviation +
					db2303.StandardDeviation +
					db2303.StandardDeviation) / 3 AS StandardDeviation
			FROM DB_Rede_3_50_1403.dbo.spStatisticalResults db1403 
			JOIN DB_Rede_3_50_2303.dbo.spStatisticalResults db2303 ON db1403.id = db2303.id
			JOIN DB_Rede_3_50_2403.dbo.spStatisticalResults db2403 ON db1403.id = db2403.id
			)
		SELECT Simulation
			, ROUND(Average * 100, 2) AS HC
			, ROUND(StandardDeviation * 100, 2) AS StaDev
			, ROUND((Average - StandardDeviation) * 100, 2) AS Conservative_value
		FROM V1
