EXEC spPVPowerData_Populate
GO
EXEC spPVPowerData_Populate_KVA
GO
EXEC spCalc_HC
GO
EXEC spGenerateLossesTables
EXEC spGenerateInvControlTables
EXEC spGenerateSourceTables
EXEC spAVGResoults
GO
-- S� podem ser chamados uma vez!!!!!!! Causam altera��es nos dados
EXEC spConvertVregMeasurament
EXEC spRemoveDuplicatesCheckReport
GO