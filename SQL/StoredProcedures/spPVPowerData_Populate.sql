
CREATE OR ALTER   PROCEDURE [dbo].[spPVPowerData_Populate]

AS
BEGIN

	SET NOCOUNT ON;
		-- Não está considerando o tempo, pega o valor minimo, mas esse pode acontecer em qualquer momento
		-- sorte que não precisa rodar toda a simulação para ter esse resultado mudado, só alterar essa SP e EXECUTE
		
		-- Tem de identificar o timestep de maior geração e depois pegar os valores de pot, de cada GD, para ele
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