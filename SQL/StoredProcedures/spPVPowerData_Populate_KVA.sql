CREATE OR ALTER   PROCEDURE [dbo].[spPVPowerData_Populate_KVA]

AS
BEGIN

	SET NOCOUNT ON;

		UPDATE 
			tblPVSystems
		SET
			kva = POWER(POWER(PV.kW, 2) + POWER(PV.kvar,2), 0.5)

		FROM tblPVSystems PV WITH (NOLOCK)

END