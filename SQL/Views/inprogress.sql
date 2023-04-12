

	CREATE TABLE #BAT_SUM
    (
		 [Case] int,
		 [Elemento] nvarchar(20),
		 [MAX_Pot_Diff_5_4_W] float,
		 [MAX_Pot_Diff_7_6_W] float,
		 [ADJ_Battery_Capacity_5_4] float,
		 [ADJ_Battery_Capacity_7_6] float
    )

	Insert into #BAT_SUM ( [Case],[Elemento]
			  ,[MAX_Pot_Diff_5_4_W] -- W
			  ,[MAX_Pot_Diff_7_6_W]
			  ,[ADJ_Battery_Capacity_5_4] -- Wh
			  ,[ADJ_Battery_Capacity_7_6])
	(
		SELECT [Case] ,[Elemento]
			  ,[MAX_Pot_Diff_5_4_W] -- W
			  ,[MAX_Pot_Diff_7_6_W]
			  ,[ADJ_Battery_Capacity_5_4] -- Wh
			  ,[ADJ_Battery_Capacity_7_6]
		FROM spBatterySummary
	)

	--- BY ELEMENT
	SELECT 
		Elemento
		, MAX([MAX_Pot_Diff_5_4_W])		  AS MAX_Pot_54_W
		, MAX([MAX_Pot_Diff_7_6_W])		  AS MAX_Pot_76_W
		, MAX([ADJ_Battery_Capacity_5_4]) AS MAX_Eng_54_Wh
		, MAX([ADJ_Battery_Capacity_7_6]) AS MAX_Eng_76_Wh

		--, MIN([MAX_Pot_Diff_5_4_W])		  AS MIN_Pot_54_W
		--, MIN([MAX_Pot_Diff_7_6_W])		  AS MIN_Pot_76_W
		--, MIN([ADJ_Battery_Capacity_5_4]) AS MIN_Eng_54_Wh
		--, MIN([ADJ_Battery_Capacity_7_6]) AS MIN_Eng_76_Wh

		, AVG([MAX_Pot_Diff_5_4_W])		  AS AVG_Pot_54_W
		, AVG([MAX_Pot_Diff_7_6_W])		  AS AVG_Pot_76_W
		, AVG([ADJ_Battery_Capacity_5_4]) AS AVG_Eng_54_Wh
		, AVG([ADJ_Battery_Capacity_7_6]) AS AVG_Eng_76_Wh
	FROM #BAT_SUM
	GROUP BY Elemento;

	--- BY CASE 
WITH
	BAT_SUM_BY_CASE AS (
		SELECT
			[Case]
			, SUM([MAX_Pot_Diff_5_4_W])		  AS SUM_Pot_54_W
			, SUM([MAX_Pot_Diff_7_6_W])		  AS SUM_Pot_76_W
			, SUM([ADJ_Battery_Capacity_5_4]) AS SUM_Eng_54_Wh
			, SUM([ADJ_Battery_Capacity_7_6]) AS SUM_Eng_76_Wh
		FROM #BAT_SUM
		GROUP BY [Case]
	)
	SELECT 
		MAX(SUM_Pot_54_W)  AS MAX_SUM_POT_54_W
		,MAX(SUM_Pot_76_W)  AS MAX_SUM_POT_76_W
		,MAX(SUM_Eng_54_Wh) AS MAX_SUM_Eng_54_Wh
		,MAX(SUM_Eng_76_Wh) AS MAX_SUM_Eng_76_Wh

		,AVG(SUM_Pot_54_W)  AS AVG_SUM_POT_54_W
		,AVG(SUM_Pot_76_W)  AS AVG_SUM_POT_76_W
		,AVG(SUM_Eng_54_Wh) AS AVG_SUM_Eng_54_Wh
		,AVG(SUM_Eng_76_Wh) AS AVG_SUM_Eng_76_Wh

	FROM BAT_SUM_BY_CASE;

	-- Need to drop this table to run the query again
	DROP TABLE #BAT_SUM

	


