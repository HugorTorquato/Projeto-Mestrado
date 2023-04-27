---------------------------------------------------------
-- This function aims to be used to plot power diferences in python plot tool,
-- It'll receiva two argumets, the element number to filter and the desired Case
-- simulated (1-50) in this case

-- Probably i'll add more stuffs here but let it be for now
---------------------------------------------------------
CREATE OR ALTER FUNCTION dbo.fnGetPotDataBasedOnElement (@element NVARCHAR(20), @case INT)
RETURNS TABLE
AS
RETURN 
(
	SELECT 
		*
	FROM vwCreateSUMProcessedPVPowerDataDiffTable
	WHERE 
		Elemento =	@element
		AND [Case] =  @case
)