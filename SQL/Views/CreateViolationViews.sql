


CREATE OR ALTER VIEW vwOvervoltageViolations
AS
	SELECT
		* 
	FROM MonitoresData_2
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] > 220/SQRT(3) * 1.05

GO

CREATE OR ALTER VIEW vwUndervoltageViolations
AS
	SELECT
		* 
	FROM MonitoresData_2
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] < 220/SQRT(3) * 0.93

GO

CREATE OR ALTER VIEW vwUnbalanceViolations
AS
	SELECT
		* 
	FROM MonitoresData_2
	WHERE 
		Elemento LIKE 'line.%'
		AND Measurement IN (' V1', ' V2', ' V3')
		AND [Value] > 100
		AND [Value] < 220/SQRT(3) * 0.93

GO











SELECT * FROM  vwOvervoltageViolations
select vwVV_VW_Data
select 220/SQRT(3) * 0.92
