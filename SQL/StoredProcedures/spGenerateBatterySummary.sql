
CREATE OR ALTER PROCEDURE spGenerateBatterySummary
AS
BEGIN
	-----------------------------------------------------------------------------
	------------------------- CREATE OR DELETE DATA -----------------------------
	-----------------------------------------------------------------------------
	IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME IN ('spBatterySummary')
				)
		)
	BEGIN
		DELETE FROM spBatterySummary
		DBCC CHECKIDENT('spBatterySummary', RESEED, 0)
	END

	-----------------------------------------------------------------------------
	------------------------------ POPULATE DATA --------------------------------
	-----------------------------------------------------------------------------

	-- Create a temp table to avoid unecessary processing
	CREATE TABLE #tmpEnergytable
	(
		[Case] int
		, Elemento NVARCHAR(50)
		, MAX_Pot_Diff_5_4 float
		, MAX_Pot_Diff_7_6 float
		, MAX_Eergy_Diff_5_4 float
		, MAX_Eergy_Diff_7_6 float
		, SUM_Eergy_Diff_5_4 float
		, SUM_Eergy_Diff_7_6 float
		, MAX_CUR_Diff_5_4 float
		, MAX_CUR_Diff_7_6 float
		, SUM_CUR_Diff_5_4 float
		, SUM_CUR_Diff_7_6 float
	)

	-- Declare all variables we will use
	DECLARE @TensaoNomBat INT;
	DECLARE @TensaoNomBatMAX FLOAT;
	DECLARE @TensaoNomBatMIN FLOAT;
	DECLARE @TensaoSoC FLOAT;
	DECLARE @DiasAuto INT;
	DECLARE @FatorEOL FLOAT;
	DECLARE @FatorEFF FLOAT;
	DECLARE @CargaIndividual INT;

	SET @TensaoNomBat = 48;      --V
	SET @TensaoNomBatMAX = 54;   --V
	SET @TensaoNomBatMIN = 52.5; --V
	SET @TensaoSoC = 40.5;       --V
	SET @DiasAuto = 1;
	SET @FatorEOL = 0.8;
	SET @FatorEFF = 1/0.98; 
	SET @CargaIndividual = 50;   -- Ah

	-- Insert power and energ data into temp table
	INSERT INTO #tmpEnergytable
		SELECT
			 DISTINCT(SPPPDD.[Case])
			 , SPPPDD.Elemento
			-- Max POWER demand PV system is injecting into the system
			, ( SELECT MAX(SPPPDD2.Sum_Pot_Diff_5_4) FROM spSUMProcessedPVPowerDataDiff AS SPPPDD2 WHERE SPPPDD2.Elemento = SPPPDD.Elemento AND SPPPDD2.[Case] = SPPPDD.[Case] ) AS MAX_Pot_Diff_5_4
			, ( SELECT MAX(SPPPDD2.Sum_Pot_Diff_7_6) FROM spSUMProcessedPVPowerDataDiff AS SPPPDD2 WHERE SPPPDD2.Elemento = SPPPDD.Elemento AND SPPPDD2.[Case] = SPPPDD.[Case] ) AS MAX_Pot_Diff_7_6
			-- Max ENERGY demand PV system is injecting into the system
			, ( SELECT MAX(SPPEDD2.Sum_Eergy_Diff_5_4) FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS MAX_Eergy_Diff_5_4
			, ( SELECT MAX(SPPEDD2.Sum_Eergy_Diff_7_6) FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS MAX_Eergy_Diff_7_6

			-- SUM energy demand PV system is injecting into the system
			, ( SELECT SUM(SPPEDD2.Sum_Eergy_Diff_5_4) FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS SUM_Eergy_Diff_5_4
			, ( SELECT SUM(SPPEDD2.Sum_Eergy_Diff_7_6) FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS SUM_Eergy_Diff_7_6

			-- Max CURRENT demand PV system is injecting into the system
			, ( SELECT MAX(SPPPDD2.Sum_Pot_Diff_5_4) / @TensaoNomBat FROM spSUMProcessedPVPowerDataDiff AS SPPPDD2 WHERE SPPPDD2.Elemento = SPPPDD.Elemento AND SPPPDD2.[Case] = SPPPDD.[Case] ) AS MAX_CUR_Diff_5_4
			, ( SELECT MAX(SPPPDD2.Sum_Pot_Diff_7_6) / @TensaoNomBat FROM spSUMProcessedPVPowerDataDiff AS SPPPDD2 WHERE SPPPDD2.Elemento = SPPPDD.Elemento AND SPPPDD2.[Case] = SPPPDD.[Case] ) AS MAX_CUR_Diff_7_6

			-- SUM CURRENT demand PV system is injecting into the system
			, ( SELECT SUM(SPPEDD2.Sum_Eergy_Diff_5_4) / @TensaoNomBat FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS SUM_CUR_Diff_5_4
			, ( SELECT SUM(SPPEDD2.Sum_Eergy_Diff_7_6) / @TensaoNomBat FROM spSUMProcessedPVEergyDataDiff AS SPPEDD2 WHERE SPPEDD2.Elemento = SPPPDD.Elemento AND SPPEDD2.[Case] = SPPPDD.[Case] ) AS SUM_CUR_Diff_7_6


		FROM spSUMProcessedPVPowerDataDiff AS SPPPDD

	--SELECT * FROM #tmpEnergytable -- Query somente para verificar a tabela temp que foi criada

	INSERT INTO spBatterySummary
		SELECT
			DISTINCT(tmp.[Case])
			, tmp.Elemento
			, ROUND(tmp.MAX_Pot_Diff_5_4  , 4)*1000 AS MAX_Pot_Diff_5_4_W
			, ROUND(tmp.MAX_Pot_Diff_7_6  , 4)*1000 AS MAX_Pot_Diff_7_6_W
			, ROUND(tmp.MAX_Eergy_Diff_5_4, 4)*1000 AS MAX_Eergy_Diff_5_4_Wh
			, ROUND(tmp.MAX_Eergy_Diff_7_6, 4)*1000 AS MAX_Eergy_Diff_7_6_Wh
			, ROUND(tmp.SUM_Eergy_Diff_5_4, 4)*1000 AS SUM_Eergy_Diff_5_4_Wh
			, ROUND(tmp.SUM_Eergy_Diff_7_6, 4)*1000 AS SUM_Eergy_Diff_7_6_Wh
			, ROUND(tmp.MAX_CUR_Diff_5_4  , 4)*1000 AS MAX_CUR_Diff_5_4_Ah
			, ROUND(tmp.MAX_CUR_Diff_7_6  , 4)*1000 AS MAX_CUR_Diff_7_6_Ah
			, ROUND(tmp.SUM_CUR_Diff_5_4  , 4)*1000 AS SUM_CUR_Diff_5_4_Ah
			, ROUND(tmp.SUM_CUR_Diff_7_6  , 4)*1000 AS SUM_CUR_Diff_7_6_Ah
			, ROUND(ISNULL(MAX_Eergy_Diff_7_6, 0) * 1000 / @FatorEOL / @FatorEFF , 4) AS ADJ_Battery_Capacity --Wh

			-- Calculate batery variables ( I removed this part because i'll not set a default baterry type in here, just give the parameters for the user to do so )
			--
			--, ROUND(ISNULL(MAX_Eergy_Diff_7_6, 0) * 1000 / @TensaoNomBat / @FatorEOL / @FatorEFF , 4) AS Battery_Capacity --Ah
			--, FLOOR(@TensaoNomBat / @TensaoNomBat)                                                   AS N_celulas_serie
			--, CEILING((ISNULL(MAX_Eergy_Diff_7_6, 0) / @TensaoNomBat / @FatorEOL / @FatorEFF)
			--	 / (@CargaIndividual * FLOOR(@TensaoNomBat / @TensaoNomBat)))                        AS N_celulas_paral
		FROM #tmpEnergytable tmp

	-- Remember to drop this table or it will cause problems in next execution
	DROP TABLE #tmpEnergytable
END
