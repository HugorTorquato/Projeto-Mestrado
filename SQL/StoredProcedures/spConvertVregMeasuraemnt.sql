

CREATE OR ALTER PROCEDURE spConvertVregMeasurament
AS
BEGIN
	update MonitoresData_2
		set [Value] = [Value]*(220/sqrt(3))
	where [Value] != 9999 AND Measurement like 'Vreg'
END
