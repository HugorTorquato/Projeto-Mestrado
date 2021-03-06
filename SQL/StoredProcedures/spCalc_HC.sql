CREATE OR ALTER PROCEDURE [dbo].[spCalc_HC]

AS
BEGIN
		UPDATE 
			General
		SET
			HC = (select
						-min(SPPGD.Sum_Pot_W)/45000
					from spSum_Pot_P_GDs SPPGD
						where 
							SPPGD.[Case] = G.[Case] and
							SPPGD.Simulation = G.SimulationCount)
		FROM General G
END