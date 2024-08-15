



CREATE OR ALTER PROCEDURE  spHC_Violation_Report_For_Simulation 
	@simulation int,
	@percentage int
AS
	SELECT
	power_percentage
    ,overvoltage_count
    ,undervoltage_count
    ,overcurrent_count
    ,unbalance_count
    ,(SELECT overvoltage_count + undervoltage_count + overcurrent_count + unbalance_count) as total_count
	FROM (
		SELECT TOP(1)
		(@percentage) as power_percentage
		,(select ISNULL(sum(CR.overvoltage), 0) from tblCheck_Report CR
			where CR.overvoltage = 1 and CR.simulation = @simulation) as overvoltage_count
		,(select ISNULL(sum(CR.undervoltage), 0) from tblCheck_Report CR 
			where CR.undervoltage = 1 and CR.simulation = @simulation) as undervoltage_count
		,(select ISNULL(sum(CR.overcurrent), 0) from tblCheck_Report CR 
			where CR.overcurrent = 1 and CR.simulation = @simulation) as overcurrent_count
		,(select ISNULL(sum(CR.unbalance), 0) from tblCheck_Report CR 
			where CR.unbalance = 1 and CR.simulation = @simulation) as unbalance_count
		) AS counts;
