EXEC spPVPowerData_Populate
GO
EXEC spPVPowerData_Populate_KVA
GO
EXEC spCalc_HC
GO
EXEC spGenerateLossesTables
EXEC spGenerateInvControlTables
GO
EXEC spConvertVregMeasurament
GO