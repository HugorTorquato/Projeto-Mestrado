

CREATE OR ALTER   VIEW [dbo].[vwVoltageMonitors]
AS
	select * from MonitoresData_2
	where
		Elemento like 'pvsystem%' and
		Measurement in ('Vreg', ' V1', ' V2', ' V3') and
		Simulation > 2
GO


