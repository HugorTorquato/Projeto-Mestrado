
CREATE OR ALTER PROCEDURE spSUMCreateProcessedPVPowerDataDiffTable
AS
BEGIN

	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSUMProcessedPVPowerDataDiff')
				)
		)
	BEGIN
		DELETE FROM spSUMProcessedPVPowerDataDiff
		DBCC CHECKIDENT('spSUMProcessedPVPowerDataDiff', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO spSUMProcessedPVPowerDataDiff 
		([Case], Elemento, TimeStep, Sum_Pot_2, Sum_Pot_5, Sum_Pot_4, Sum_Pot_Diff_5_4, 
		Sum_Pot_7, Sum_Pot_6, Sum_Pot_Diff_7_6)
	
		select * from vwCreateSUMProcessedPVPowerDataDiffTable  WITH (NOLOCK)
END