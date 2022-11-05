-----------------------------------------------------------------------------
-- Evaluate Watt difference caused by VW cotrol
-- 		Comparing only VW control with the control case. Using the same 
-- amount of power in each PV
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spWattDiffControllVWOnly')
				)
		)
	BEGIN
		CREATE TABLE spWattDiffControllVWOnly (
					id int PRIMARY KEY IDENTITY(1,1),
					[Case] int,
					TimeStep int,
					Elemento varchar(50),
					Measurement varchar(50),
					Simulation_With_VW int,
					Value_With_VW float,
					Simulation_Without_VW int,
					Value_Without_VW float,
					Power_Diff float,
					Power_Diff_per_cent float
				);
		--SET IDENTITY_INSERT dbo.spWattDiffControllVWOnly ON;
	END