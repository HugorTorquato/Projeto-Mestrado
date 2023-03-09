
CREATE OR ALTER PROCEDURE spCreateProcessedPVPowerDataDiffTable
AS
BEGIN

	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spProcessedPVPowerDataDiff')
				)
		)
	BEGIN
		DELETE FROM spProcessedPVPowerDataDiff
		DBCC CHECKIDENT('spProcessedPVPowerDataDiff', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO spProcessedPVPowerDataDiff 
		([Case], Elemento, Measurement, TimeStep, Value_S5, Value_S4, Value_diff_5to4, 
		Value_S7, Value_S6, Value_diff_7to6)
	
		select * from vwCreateProcessedPVPowerDataDiffTable  WITH (NOLOCK)
END