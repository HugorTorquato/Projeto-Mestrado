-----------------------------------------------------------------------------
-- General definition 
--		Parent table, all overview dta from each case in each simulation 
-- should be placed here.
-- There are more data to be added here
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblGeneral')
				)
		)
	BEGIN
		CREATE TABLE tblGeneral (
			Simulation int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			SimulationCount int,
			Voltage_Max float,
			Voltage_Min float,
			GD_Config varchar(50),
			HC float
			-- Adicionar aqui
		);
	END