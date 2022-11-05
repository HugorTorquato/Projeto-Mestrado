CREATE OR ALTER VIEW vwHC_VIOLATION_REPORT
AS
	SELECT
        overvoltage_count
        ,undervoltage_count
        ,overcurrent_count
        ,unbalance_count
        ,(SELECT overvoltage_count + undervoltage_count + overcurrent_count + unbalance_count) as total_count
        FROM (
            SELECT TOP(1)
            (select ISNULL(sum(CR.overvoltage), 0) from tblCheck_Report CR where CR.overvoltage = 1) as overvoltage_count
            ,(select ISNULL(sum(CR.undervoltage), 0) from tblCheck_Report CR where CR.undervoltage = 1) as undervoltage_count
            ,(select ISNULL(sum(CR.overcurrent), 0) from tblCheck_Report CR where CR.overcurrent = 1) as overcurrent_count
            ,(select ISNULL(sum(CR.unbalance), 0) from tblCheck_Report CR where CR.unbalance = 1) as unbalance_count
            ) AS counts
