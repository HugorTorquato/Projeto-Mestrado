






WITH VoltageMeasurements AS (
	SELECT
		*
	FROM [DB_Rede_3].[dbo].[tblMonitoresData]
	WHERE 
		Elemento like 'load.fakeload_bus_%'
		AND Measurement IN (' V3',' V2',' V1')
)

SELECT 
	 _001.[Value] AS bus_001
    ,_002.[Value] AS bus_002
    ,_003.[Value] AS bus_003
    ,_004.[Value] AS bus_004
    ,_005.[Value] AS bus_005
    ,_006.[Value] AS bus_006
    ,_007.[Value] AS bus_007
    ,_008.[Value] AS bus_008
    ,_009.[Value] AS bus_009
    ,_010.[Value] AS bus_010
    ,_011.[Value] AS bus_011
    ,_012.[Value] AS bus_012
    ,_013.[Value] AS bus_013
    ,_014.[Value] AS bus_014
    ,_015.[Value] AS bus_015
    ,_016.[Value] AS bus_016
    ,_017.[Value] AS bus_017
    ,_018.[Value] AS bus_018
    ,_019.[Value] AS bus_019
    ,_020.[Value] AS bus_020
    ,_021.[Value] AS bus_021
    ,_022.[Value] AS bus_022
    ,_023.[Value] AS bus_023
    ,_024.[Value] AS bus_024
    ,_025.[Value] AS bus_025
    ,_026.[Value] AS bus_026
    ,_027.[Value] AS bus_027
    ,_028.[Value] AS bus_028
    ,_029.[Value] AS bus_029
    ,_030.[Value] AS bus_030
    ,_031.[Value] AS bus_031
    ,_032.[Value] AS bus_032
    ,_033.[Value] AS bus_033
    ,_034.[Value] AS bus_034
    ,_035.[Value] AS bus_035
    ,_036.[Value] AS bus_036
    ,_037.[Value] AS bus_037
    ,_038.[Value] AS bus_038
    ,_039.[Value] AS bus_039
    ,_pri.[Value] AS bus_xfmr_pri
    ,_sec.[Value] AS bus_xfmr_sec
FROM (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_001' AND VM.[Case] = 1 AND VM.Simulation = 1 AND VM.Measurement = ' V1') AS _001
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_002') AS _002 ON _001.[Case] = _002.[Case] AND _001.Simulation = _002.Simulation AND _001.Measurement = _002.Measurement AND _001.TimeStep = _002.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_003') AS _003 ON _001.[Case] = _003.[Case] AND _001.Simulation = _003.Simulation AND _001.Measurement = _003.Measurement AND _001.TimeStep = _003.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_004') AS _004 ON _001.[Case] = _004.[Case] AND _001.Simulation = _004.Simulation AND _001.Measurement = _004.Measurement AND _001.TimeStep = _004.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_005') AS _005 ON _001.[Case] = _005.[Case] AND _001.Simulation = _005.Simulation AND _001.Measurement = _005.Measurement AND _001.TimeStep = _005.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_006') AS _006 ON _001.[Case] = _006.[Case] AND _001.Simulation = _006.Simulation AND _001.Measurement = _006.Measurement AND _001.TimeStep = _006.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_007') AS _007 ON _001.[Case] = _007.[Case] AND _001.Simulation = _007.Simulation AND _001.Measurement = _007.Measurement AND _001.TimeStep = _007.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_008') AS _008 ON _001.[Case] = _008.[Case] AND _001.Simulation = _008.Simulation AND _001.Measurement = _008.Measurement AND _001.TimeStep = _008.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_009') AS _009 ON _001.[Case] = _009.[Case] AND _001.Simulation = _009.Simulation AND _001.Measurement = _009.Measurement AND _001.TimeStep = _009.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_010') AS _010 ON _001.[Case] = _010.[Case] AND _001.Simulation = _010.Simulation AND _001.Measurement = _010.Measurement AND _001.TimeStep = _010.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_011') AS _011 ON _001.[Case] = _011.[Case] AND _001.Simulation = _011.Simulation AND _001.Measurement = _011.Measurement AND _001.TimeStep = _011.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_012') AS _012 ON _001.[Case] = _012.[Case] AND _001.Simulation = _012.Simulation AND _001.Measurement = _012.Measurement AND _001.TimeStep = _012.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_013') AS _013 ON _001.[Case] = _013.[Case] AND _001.Simulation = _013.Simulation AND _001.Measurement = _013.Measurement AND _001.TimeStep = _013.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_014') AS _014 ON _001.[Case] = _014.[Case] AND _001.Simulation = _014.Simulation AND _001.Measurement = _014.Measurement AND _001.TimeStep = _014.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_015') AS _015 ON _001.[Case] = _015.[Case] AND _001.Simulation = _015.Simulation AND _001.Measurement = _015.Measurement AND _001.TimeStep = _015.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_016') AS _016 ON _001.[Case] = _016.[Case] AND _001.Simulation = _016.Simulation AND _001.Measurement = _016.Measurement AND _001.TimeStep = _016.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_017') AS _017 ON _001.[Case] = _017.[Case] AND _001.Simulation = _017.Simulation AND _001.Measurement = _017.Measurement AND _001.TimeStep = _017.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_018') AS _018 ON _001.[Case] = _018.[Case] AND _001.Simulation = _018.Simulation AND _001.Measurement = _018.Measurement AND _001.TimeStep = _018.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_019') AS _019 ON _001.[Case] = _019.[Case] AND _001.Simulation = _019.Simulation AND _001.Measurement = _019.Measurement AND _001.TimeStep = _019.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_020') AS _020 ON _001.[Case] = _020.[Case] AND _001.Simulation = _020.Simulation AND _001.Measurement = _020.Measurement AND _001.TimeStep = _020.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_021') AS _021 ON _001.[Case] = _021.[Case] AND _001.Simulation = _021.Simulation AND _001.Measurement = _021.Measurement AND _001.TimeStep = _021.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_022') AS _022 ON _001.[Case] = _022.[Case] AND _001.Simulation = _022.Simulation AND _001.Measurement = _022.Measurement AND _001.TimeStep = _022.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_023') AS _023 ON _001.[Case] = _023.[Case] AND _001.Simulation = _023.Simulation AND _001.Measurement = _023.Measurement AND _001.TimeStep = _023.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_024') AS _024 ON _001.[Case] = _024.[Case] AND _001.Simulation = _024.Simulation AND _001.Measurement = _024.Measurement AND _001.TimeStep = _024.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_025') AS _025 ON _001.[Case] = _025.[Case] AND _001.Simulation = _025.Simulation AND _001.Measurement = _025.Measurement AND _001.TimeStep = _025.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_026') AS _026 ON _001.[Case] = _026.[Case] AND _001.Simulation = _026.Simulation AND _001.Measurement = _026.Measurement AND _001.TimeStep = _026.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_027') AS _027 ON _001.[Case] = _027.[Case] AND _001.Simulation = _027.Simulation AND _001.Measurement = _027.Measurement AND _001.TimeStep = _027.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_028') AS _028 ON _001.[Case] = _028.[Case] AND _001.Simulation = _028.Simulation AND _001.Measurement = _028.Measurement AND _001.TimeStep = _028.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_029') AS _029 ON _001.[Case] = _029.[Case] AND _001.Simulation = _029.Simulation AND _001.Measurement = _029.Measurement AND _001.TimeStep = _029.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_030') AS _030 ON _001.[Case] = _030.[Case] AND _001.Simulation = _030.Simulation AND _001.Measurement = _030.Measurement AND _001.TimeStep = _030.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_031') AS _031 ON _001.[Case] = _031.[Case] AND _001.Simulation = _031.Simulation AND _001.Measurement = _031.Measurement AND _001.TimeStep = _031.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_032') AS _032 ON _001.[Case] = _032.[Case] AND _001.Simulation = _032.Simulation AND _001.Measurement = _032.Measurement AND _001.TimeStep = _032.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_033') AS _033 ON _001.[Case] = _033.[Case] AND _001.Simulation = _033.Simulation AND _001.Measurement = _033.Measurement AND _001.TimeStep = _033.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_034') AS _034 ON _001.[Case] = _034.[Case] AND _001.Simulation = _034.Simulation AND _001.Measurement = _034.Measurement AND _001.TimeStep = _034.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_035') AS _035 ON _001.[Case] = _035.[Case] AND _001.Simulation = _035.Simulation AND _001.Measurement = _035.Measurement AND _001.TimeStep = _035.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_036') AS _036 ON _001.[Case] = _036.[Case] AND _001.Simulation = _036.Simulation AND _001.Measurement = _036.Measurement AND _001.TimeStep = _036.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_037') AS _037 ON _001.[Case] = _037.[Case] AND _001.Simulation = _037.Simulation AND _001.Measurement = _037.Measurement AND _001.TimeStep = _037.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_038') AS _038 ON _001.[Case] = _038.[Case] AND _001.Simulation = _038.Simulation AND _001.Measurement = _038.Measurement AND _001.TimeStep = _038.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_33998182_039') AS _039 ON _001.[Case] = _039.[Case] AND _001.Simulation = _039.Simulation AND _001.Measurement = _039.Measurement AND _001.TimeStep = _039.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_xfmr_pri_33998182') AS _pri ON _001.[Case] = _pri.[Case] AND _001.Simulation = _pri.Simulation AND _001.Measurement = _pri.Measurement AND _001.TimeStep = _pri.TimeStep
JOIN (SELECT * FROM VoltageMeasurements VM WHERE Elemento like 'load.fakeload_bus_xfmr_sec_33998182') AS _sec ON _001.[Case] = _sec.[Case] AND _001.Simulation = _sec.Simulation AND _001.Measurement = _sec.Measurement AND _001.TimeStep = _sec.TimeStep
