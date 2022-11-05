CREATE OR ALTER VIEW vwOvervoltageViolations
AS
	SELECT
		* 
	FROM tblMonitoresData
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] > 220/SQRT(3) * 1.05

