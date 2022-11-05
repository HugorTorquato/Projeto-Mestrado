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
-- Só podem ser chamados uma vez!!!!!!! Causam alterações nos dados
EXEC spConvertVregMeasurament
EXEC spRemoveDuplicatesCheckReport
GO