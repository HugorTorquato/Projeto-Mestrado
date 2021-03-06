

CREATE OR ALTER PROCEDURE spCreateSum_Pot_P_GDs
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------

	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spSum_Pot_P_GDs')
				)
		)
	BEGIN
		DELETE FROM spSum_Pot_P_GDs
		DBCC CHECKIDENT('spSum_Pot_P_GDs', RESEED, 0)
	END
	ELSE
	BEGIN
		-- Daria para colocar corrente m?xima tbm... ponto a se pensar
		CREATE TABLE spSum_Pot_P_GDs (
			id int PRIMARY KEY IDENTITY(1,1),
			TimeStep int,
			[Case] int,
			Simulation int,
			Sum_Pot_W float
			-- Adicionar aqui
		);
	END
	
	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------
	INSERT INTO spSum_Pot_P_GDs
		(TimeStep, [Case], Simulation, Sum_Pot_W)
	select
		distinct MD2.TimeStep
		, MD2.[Case]
		, MD2.Simulation
		, (select sum(MD22.[Value]) from MonitoresData_2 MD22
			where MD22.[Case] = MD2.[Case]
				and MD22.Elemento like 'pvsystem.pv_%'
				and MD22.Measurement like ' watts'
				and MD22.TimeStep = MD2.TimeStep
				and MD22.Simulation = MD2.Simulation) AS Sum_Pot_W
	from MonitoresData_2 MD2
		order by MD2.[Case], MD2.Simulation, MD2.TimeStep

	
	-----------------------------------------------------------------------------
	------------------------------ Test Logic    --------------------------------
	-----------------------------------------------------------------------------
	-- Just need to set the case / Simulation / TimeStep e comparar os dados
	--select * from PVSystems where [Case] = 7 and Simulation=4

	--select * from MonitoresData_2 md22
	--	where MD22.[Case] = 7 and md22.Simulation = 4 and MD22.Elemento like 'pvsystem.pv_%'
	--			and MD22.Measurement like ' watts'AND MD22.TimeStep = 42

	--select sum(MD22.[Value]) from MonitoresData_2 md22
	--	where MD22.[Case] = 7 and md22.Simulation = 4 and MD22.Elemento like 'pvsystem.pv_%'
	--			and MD22.Measurement like ' watts'AND MD22.TimeStep = 42
END