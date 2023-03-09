

CREATE OR ALTER PROCEDURE spConvertVregMeasurament
AS
BEGIN
	update tblMonitoresData
		set [Value] = [Value]*(220/sqrt(3))
	where [Value] != 9999 AND Measurement like 'Vreg' AND [Value] < 2
END
