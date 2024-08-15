
---------------------------------------------------------------------------------------------------------------------------

-- Get results from VW

---------------------------------------------------------------------------------------------------------------------------
CREATE TABLE #Violation_Report_With_All_DBs_VW (
    power_percentage INT,
	overvoltage_count INT,
    undervoltage_count INT,
	overcurrent_count INT,
	unbalance_count INT,
	total_count INT
);

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_3006_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 15;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_2806_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 15;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_2706_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 15;


INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0107_2_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 30;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0107_3_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 30;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0107_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 30;


INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0107_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 50;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0307_2_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 50;

INSERT INTO #Violation_Report_With_All_DBs_VW
EXEC [DB_Rede_3_50_0307_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 4, @percentage = 50;

---------------------------------------------------------------------------------------------------------------------------

-- Get results from VV + VW

---------------------------------------------------------------------------------------------------------------------------
CREATE TABLE #Violation_Report_With_All_DBs_VV_VW (
	power_percentage INT,
    overvoltage_count INT,
    undervoltage_count INT,
	overcurrent_count INT,
	unbalance_count INT,
	total_count INT
);

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_3006_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 15;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_2806_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 15;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_2706_15].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 15;


INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0107_2_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 30;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0107_3_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 30;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0107_30].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 30;


INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0107_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 50;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0307_2_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 50;

INSERT INTO #Violation_Report_With_All_DBs_VV_VW
EXEC [DB_Rede_3_50_0307_50].[dbo].[spHC_Violation_Report_For_Simulation] @simulation = 6, @percentage = 50;

---------------------------------------------------------------------------------------------------------------------------

-- Group and display tables

---------------------------------------------------------------------------------------------------------------------------
SELECT 
	DISTINCT(power_percentage)
	, SUM(overvoltage_count) as overvoltage_count
	, SUM(undervoltage_count) as undervoltage_count
	, SUM(overcurrent_count) as overcurrent_count
	, SUM(unbalance_count) as unbalance_count
	, SUM(total_count) as total_count
FROM #Violation_Report_With_All_DBs_VW
GROUP BY power_percentage;

SELECT 
	DISTINCT(power_percentage)
	, SUM(overvoltage_count) as overvoltage_count
	, SUM(undervoltage_count) as undervoltage_count
	, SUM(overcurrent_count) as overcurrent_count
	, SUM(unbalance_count) as unbalance_count
	, SUM(total_count) as total_count
FROM #Violation_Report_With_All_DBs_VV_VW
GROUP BY power_percentage;

---------------------------------------------------------------------------------------------------------------------------

-- Dispose temp tables

---------------------------------------------------------------------------------------------------------------------------

DROP TABLE #Violation_Report_With_All_DBs_VW;
DROP TABLE #Violation_Report_With_All_DBs_VV_VW;
