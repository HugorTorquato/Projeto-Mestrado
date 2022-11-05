-----------------------------------------------------------------------------
-- spInvControlData definition
--		This table contain all measurements for each monitor defined in 
-- spSummary_InvControl.
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spInvControlData')
				)
		)
	BEGIN
		CREATE TABLE spInvControlData (
			id int PRIMARY KEY IDENTITY(1,1),
			id_Summary int,
			TimeStep int,
			Measurement varchar(50),
			[Value] float
		);

		ALTER TABLE spInvControlData
		ADD CONSTRAINT FK_spInvControlSummary_spInvControlData
			FOREIGN KEY (id_Summary) REFERENCES spSummary_InvControl (id)
	END