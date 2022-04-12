USE [DB_Rede_3]
GO

CREATE OR ALTER   PROCEDURE [dbo].[spPVPowerData_Populate]

AS
BEGIN

	SET NOCOUNT ON;

		UPDATE 
			PVSystems
		SET
			kW = (select min(MD2.[Value]) from MonitoresData_2 MD2
					where
						MD2.[Case] = PV.[Case] AND
						MD2.Simulation = PV.Simulation AND
						MD2.Elemento =  PV.[Name] AND
						MD2.Measurement like ' watts'),
			kvar = (select min(MD2.[Value]) from MonitoresData_2 MD2
					 where 
						MD2.[Case] = PV.[Case] AND
						MD2.Simulation = PV.Simulation AND
						MD2.Elemento =  PV.[Name] AND
						MD2.Measurement like ' vars'),
			kva = POWER(POWER(PV.kW, 2) + POWER(PV.kvar,2), 0.5)

		FROM PVSystems PV

END