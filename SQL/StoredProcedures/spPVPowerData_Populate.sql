
CREATE OR ALTER   PROCEDURE [dbo].[spPVPowerData_Populate]

AS
BEGIN

	SET NOCOUNT ON;
		-- Não está considerando o tempo, pega o valor minimo, mas esse pode acontecer em qualquer momento
		-- sorte que não precisa rodar toda a simulação para ter esse resultado mudado, só alterar essa SP e EXECUTE
		
		-- Tem de identificar o timestep de maior geração e depois pegar os valores de pot, de cada GD, para ele
		UPDATE 
			tblPVSystems
		SET
			kW = (select min(MD2.[Value]) from tblMonitoresData MD2 WITH (NOLOCK)
					where
						MD2.[Case] = PV.[Case] AND
						MD2.Simulation = PV.Simulation AND
						MD2.Elemento =  PV.[Name] AND
						MD2.Measurement like ' watts'),
			kvar = (select MAX(MD2.[Value]) from tblMonitoresData MD2 WITH (NOLOCK)
					 where 
						MD2.[Case] = PV.[Case] AND
						MD2.Simulation = PV.Simulation AND
						MD2.Elemento =  PV.[Name] AND
						MD2.Measurement like ' vars')

		FROM tblPVSystems PV WITH (NOLOCK)

END