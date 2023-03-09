
-- SP responsable for populate ative and reactive power to tblPVSystems table
EXEC spPVPowerData_Populate
-- SP responsable for calculate the KVA power from each PV unit based on KW and KVAR
EXEC spPVPowerData_Populate_KVA
-- Process to populate spTimeStempOvrViewData table, This value will be used to calculate HC
EXEC spCreateSum_Pot_P_GDs
-- Calculates HC bases of agregated powers from all phases
EXEC spCalc_HC
-- Calculates HC AVERAGE resoults from all simulations, save data in spStatisticalResults ( Discarting discrepances )
-- It also populates spStatisticalData tble with Case, Simulation and HC ( Idea here is to create a simple table with values - But looks unecessary to me )
EXEC spAVGResoults
-- SPs responsable for sizing baterry capacity
EXEC spCreateProcessedPVPowerDataDiffTable    -- Process 1F poer data (Populate table spProcessedPVPowerDataDiff)
EXEC spSUMCreateProcessedPVPowerDataDiffTable -- Process 3F poer data (Populate table spSUMProcessedPVPowerDataDiff)
EXEC spSUMCreateProcessedPVEergyDataDiff      -- Conver the power data to energy (Populate table spSUMProcessedPVEergyDataDiff)
EXEC spGenerateBatterySummary                 -- Generate general baterry data (Populate table spBatterySummary)
-- Generate Losses table (I used to generate graphcs at some point)  - EXPLORAR MAIS ESSES RESULTADOS 
-- Populate spSummary_Losses table with general loss informations for each element ( sum(W)/1000 )
-- Populate spLossesData tbae with detailed information from each spSummary_Losses record
EXEC spGenerateLossesTables
-- Generate InvControl table (I used to generate graphcs at some point)
-- Populate spSummary_InvControl table with general loss informations
-- Populate spInvControlData tbae with detailed information from each spSummary_InvControl record
	-- ('Vreg', 'volt-var', 'volt-watt', ' vars', ' watts', ' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)')
EXEC spGenerateInvControlTables
-- Generate Source table (I used to generate graphcs at some point)
-- Populate spSummary_Source table with general loss informations
-- Populate spSourceData tbae with detailed information from each spSummary_Source record
	-- (' vars', ' watts', ' P1 (kW)', ' P2 (kW)', ' P3 (kW)', ' Q1 (kvar)', ' Q2 (kvar)', ' Q3 (kvar)')
EXEC spGenerateSourceTables

-- JUST EXECUTE IF you want to conver Vreg values from PU to V
--EXEC spConvertVregMeasurament 




--THIS TABLE IS BROKEN -- VERIFY
--EXEC spRemoveDuplicatesCheckReport