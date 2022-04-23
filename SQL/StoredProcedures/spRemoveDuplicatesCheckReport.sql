

CREATE OR ALTER PROCEDURE spRemoveDuplicatesCheckReport
AS
-- Só pode rodar uma vez, se não da ruim
-- A ideia é enumerar os casos e, como o  simulation 5 está duplicado, remove os indicadores pares.
BEGIN
	DELETE T
	FROM
	(
	SELECT *
	, DupRank = ROW_NUMBER() OVER (
				  PARTITION BY Simulation
				  ORDER BY ( Simulation))

	FROM Check_Report
	) AS T
	WHERE DupRank % 2 =0 
		and Simulation = 5
END
