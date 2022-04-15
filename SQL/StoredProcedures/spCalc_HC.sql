CREATE OR ALTER PROCEDURE [dbo].[spCalc_HC]

AS
BEGIN
	-- Do not return the number of collumns affected
	SET NOCOUNT ON;

		UPDATE 
			General
		SET
			-- Remover o 45000, ele é a pot do trafo de entrada
			HC = (select SUM(kva)/45000 from PVSystems PV
						where 
							PV.[Case] = G.[Case] and
							PV.Simulation = G.SimulationCount)

		FROM General G

END