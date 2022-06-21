
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('Elements_Data')
				)
		)
	BEGIN
		CREATE TABLE Elements_Data (
			ID int PRIMARY KEY IDENTITY(1,1),
			Element varchar(50),
			Measurement varchar(50),
			[Value] float
			-- Adicionar aqui
		);
	END

GO