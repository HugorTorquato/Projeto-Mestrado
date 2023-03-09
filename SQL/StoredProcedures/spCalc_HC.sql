CREATE OR ALTER PROCEDURE spCalc_HC
AS
BEGIN
		UPDATE 
			tblGeneral
		SET
			HC = (select
						-min(SPPGD.Sum_Pot_W)/45000
					from spTimeStempOvrViewData SPPGD  WITH (NOLOCK)
						where 
							SPPGD.[Case] = G.[Case] AND
							SPPGD.Simulation = G.SimulationCount)
		FROM tblGeneral G WITH (NOLOCK)
END