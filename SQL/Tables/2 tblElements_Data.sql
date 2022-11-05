-----------------------------------------------------------------------------
-- Element_Data definition 
--		Store all elements current limit data, super important to 
-- evaluate overcurrent events. The current value is compared WITH
-- the base current value for this element, if grather than that
-- for more than 5% off simulation time, an event happens.
-- 		Feature element nominal data should be added here AS
-- columns.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('tblElements_Data')
				)
		)
	BEGIN
		CREATE TABLE tblElements_Data (
					ID int PRIMARY KEY IDENTITY(1,1),
					Element varchar(50),
					Measurement varchar(50),
					[Value] float
		);
	END