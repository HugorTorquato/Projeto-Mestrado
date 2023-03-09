-----------------------------------------------------------------------------
-- spBatterySummary definition 
--		This table aims to agregate all battery informatios, we are not
--  defining the battery type here, just providing informations for the
--  user to do so. 
--  This table will aggregate informations for both cases, VW and VW-VV,
--  VW (only) is represented by 5-3 and VV with VW by 7-6
--  I need to find a better way to do this but lets keep it for now
--
--			MAX_Pot_Diff_5_4_W	  -> Dif da max pot entre Simulação 5 e 4 ( S/VW e C/VW )
--			MAX_Pot_Diff_7_6_W	  -> Dif da max pot entre Simulação 7 e 6 ( S/VW e C/VW - C/VV) ? CONFERIR CASO 7 PARA VER SE TEM VV
--			MAX_Eergy_Diff_5_4_Wh -> Dif da max ENEGY entre Simulação 5 e 4 ( S/VW e C/VW )
--			MAX_Eergy_Diff_7_6_Wh -> Dif da max ENEGY entre Simulação 7 e 6 ( S/VW e C/VW - C/VV) ? CONFERIR CASO 7 PARA VER SE TEM VV
--			SUM_Eergy_Diff_5_4_Wh -> Dif da SUM ENEGY entre Simulação 5 e 4 ( S/VW e C/VW ) 
--			SUM_Eergy_Diff_7_6_Wh -> Dif da SUM ENEGY entre Simulação 7 e 6 ( S/VW e C/VW - C/VV) ? CONFERIR CASO 7 PARA VER SE TEM VV 

--         considerando uma bateria de 48V
--			MAX_CUR_Diff_5_4_Ah   -> Dif da max CURR entre Simulação 5 e 4 ( S/VW e C/VW ) 
--			MAX_CUR_Diff_7_6_Ah   -> Dif da max CURR entre Simulação 7 e 6 ( S/VW e C/VW - C/VV) ? CONFERIR CASO 7 PARA VER SE TEM VV 
--			SUM_CUR_Diff_5_4_Ah   -> Dif da SUM CURR entre Simulação 5 e 4 ( S/VW e C/VW )  
--			SUM_CUR_Diff_7_6_Ah   -> Dif da SUM CURR entre Simulação 7 e 6 ( S/VW e C/VW - C/VV) ? CONFERIR CASO 7 PARA VER SE TEM VV  

--			ADJ_Battery_Capacity  -> Capacidade já ajustada da bateria em Wh, com os devidos fatores já aplicados
--												( Sem considerar nenhum tipo de bateria). Para ambos os casos
-----------------------------------------------------------------------------
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
			WHERE TABLE_NAME IN ('spBatterySummary')
			)
	)
	BEGIN
		-- Daria para colocar corrente máxima tbm... ponto a se pensar
		CREATE TABLE spBatterySummary (
			id int PRIMARY KEY IDENTITY(1,1),
			[Case] int,
			Elemento nvarchar(50),
			MAX_Pot_Diff_5_4_W float,
			MAX_Pot_Diff_7_6_W float,
			MAX_Eergy_Diff_5_4_Wh float,
			MAX_Eergy_Diff_7_6_Wh float,
			SUM_Eergy_Diff_5_4_Wh float,
			SUM_Eergy_Diff_7_6_Wh float,
			MAX_CUR_Diff_5_4_Ah float,
			MAX_CUR_Diff_7_6_Ah float,
			SUM_CUR_Diff_5_4_Ah float,
			SUM_CUR_Diff_7_6_Ah float,
			ADJ_Battery_Capacity_5_4 float,
			ADJ_Battery_Capacity_7_6 float,
			-- Adicionar aqui
		);
	END