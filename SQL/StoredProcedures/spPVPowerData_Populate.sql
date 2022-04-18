
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
			kvar = (select MAX(MD2.[Value]) from MonitoresData_2 MD2
					 where 
						MD2.[Case] = PV.[Case] AND
						MD2.Simulation = PV.Simulation AND
						MD2.Elemento =  PV.[Name] AND
						MD2.Measurement like ' vars')

		FROM PVSystems PV

END