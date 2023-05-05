





USE [DB_Rede_3_50_1904_50]

SELECT
	Simulation
	, COUNT( CASE WHEN ViolationType = 1 THEN ViolationType END) AS OverVoltage
	, COUNT( CASE WHEN ViolationType = 2 THEN ViolationType END) AS UnderVoltage
	, COUNT( CASE WHEN ViolationType = 3 THEN ViolationType END) AS Unbalance
	, COUNT( CASE WHEN ViolationType = 4 THEN ViolationType END) AS OverCurrent
FROM tblViolations_Data
WHERE Simulation not in (5, 7)
GROUP BY Simulation
ORDER BY Simulation

USE [DB_Rede_3_50_3103_30]

SELECT
	Simulation
	, COUNT( CASE WHEN ViolationType = 1 THEN ViolationType END) AS OverVoltage
	, COUNT( CASE WHEN ViolationType = 2 THEN ViolationType END) AS UnderVoltage
	, COUNT( CASE WHEN ViolationType = 3 THEN ViolationType END) AS Unbalance
	, COUNT( CASE WHEN ViolationType = 4 THEN ViolationType END) AS OverCurrent
FROM tblViolations_Data
WHERE Simulation not in (5, 7)
GROUP BY Simulation
ORDER BY Simulation

USE [DB_Rede_3_50_2403]

SELECT
	Simulation
	, COUNT( CASE WHEN ViolationType = 1 THEN ViolationType END) AS OverVoltage
	, COUNT( CASE WHEN ViolationType = 2 THEN ViolationType END) AS UnderVoltage
	, COUNT( CASE WHEN ViolationType = 3 THEN ViolationType END) AS Unbalance
	, COUNT( CASE WHEN ViolationType = 4 THEN ViolationType END) AS OverCurrent
FROM tblViolations_Data
WHERE Simulation not in (5, 7)
GROUP BY Simulation
ORDER BY Simulation












