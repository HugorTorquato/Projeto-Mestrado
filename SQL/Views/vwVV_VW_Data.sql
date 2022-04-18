CREATE OR ALTER VIEW vwVV_VW_Data
AS
	select * from MonitoresData_2
	where
		Elemento like 'pvsystem%' and
		Measurement in ('Vreg', 'volt-var', 'volt-watt', ' watts', ' vars')
