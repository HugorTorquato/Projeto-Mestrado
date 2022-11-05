-----------------------------------------------------------------------------
-- ClearAllTables definition
--		This Query aims to clear all tables if they are already defined,
-- there were a problem at if i let this at tables definitions. FK was
-- complaning.
-----------------------------------------------------------------------------
IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN (					
					'spTimeStempOvrViewData',
					'spLossesData',
					'spSummary_Losses',
					'spSourceData',
					'spSummary_Source',
					'spStatisticalData',
					'spStatisticalResults',
					'spWattDiffControllVWOnly',
					'spWattDiffControll_VVandVW',
					'spInvControlData',
					'spSummary_InvControl',					
					'tblUnbalance_Data',
					'tblCheck_Report',
					'tblVoltage_Data',
					'tblVoltage_Data_Ang',
					'tblCurrent_Elemt_Data',
					'tblCurrent_Elemt_Data_Ang',
					'tblMonitoresData',
					'tblPVSystems',
					'tblGrid_Elements',
					'tblBarras',
					'tblGD',
					'tblElements_Data',
					'tblGeneral'
					)
				)
		)
	BEGIN		
		DELETE FROM spTimeStempOvrViewData
		DBCC CHECKIDENT('spTimeStempOvrViewData', RESEED, 0)
		DELETE FROM spLossesData
		DBCC CHECKIDENT('spLossesData', RESEED, 0)
		DELETE FROM spSummary_Losses
		DBCC CHECKIDENT('spSummary_Losses', RESEED, 0)
		DELETE FROM spSourceData
		DBCC CHECKIDENT('spSourceData', RESEED, 0)
		DELETE FROM spSummary_Source
		DBCC CHECKIDENT('spSummary_Source', RESEED, 0)
		DELETE FROM spStatisticalResults
		DBCC CHECKIDENT('spStatisticalResults', RESEED, 0)
		DELETE FROM spWattDiffControllVWOnly
		DBCC CHECKIDENT('spWattDiffControllVWOnly', RESEED, 0)
		DELETE FROM spWattDiffControll_VVandVW
		DBCC CHECKIDENT('spWattDiffControll_VVandVW', RESEED, 0)
		DELETE FROM spInvControlData
		DBCC CHECKIDENT('spInvControlData', RESEED, 0)
		DELETE FROM spSummary_InvControl
		DBCC CHECKIDENT('spSummary_InvControl', RESEED, 0)		
		DELETE FROM tblUnbalance_Data
		DBCC CHECKIDENT('tblUnbalance_Data', RESEED, 0)
		DELETE FROM tblCheck_Report
		DBCC CHECKIDENT('tblCheck_Report', RESEED, 0)
		DELETE FROM tblVoltage_Data
		DBCC CHECKIDENT('tblVoltage_Data', RESEED, 0)
		DELETE FROM tblVoltage_Data_Ang
		DBCC CHECKIDENT('tblVoltage_Data_Ang', RESEED, 0)
		DELETE FROM tblCurrent_Elemt_Data
		DBCC CHECKIDENT('tblCurrent_Elemt_Data', RESEED, 0)
		DELETE FROM tblCurrent_Elemt_Data_Ang
		DBCC CHECKIDENT('tblCurrent_Elemt_Data_Ang', RESEED, 0)
		DELETE FROM tblMonitoresData
		DBCC CHECKIDENT('tblMonitoresData', RESEED, 0)
		DELETE FROM tblPVSystems
		DBCC CHECKIDENT('tblPVSystems', RESEED, 0)
		DELETE FROM tblGrid_Elements
		DBCC CHECKIDENT('tblGrid_Elements', RESEED, 0)
		DELETE FROM tblBarras
		DBCC CHECKIDENT('tblBarras', RESEED, 0)
		DELETE FROM tblGD
		DBCC CHECKIDENT('tblGD', RESEED, 0)
		DELETE FROM tblElements_Data
		DBCC CHECKIDENT('tblElements_Data', RESEED, 0)
		DELETE FROM tblGeneral
		DBCC CHECKIDENT('tblGeneral', RESEED, 0)
	END
