CREATE OR ALTER VIEW vwVV_VW_Data
AS
	select * from tblMonitoresData
	where
		Elemento like 'pvsystem%' and
		Measurement in ('Vreg', 'volt-var', 'volt-watt', ' watts', ' vars')
