



CREATE TABLE #PVP1(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);
CREATE TABLE #PVP2(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);
CREATE TABLE #PVP3(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);
CREATE TABLE #PVQ1(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);
CREATE TABLE #PVQ2(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);

CREATE TABLE #PVQ3(
	   [Nome_ID] INT
      ,[Case] INT
      ,[Simulation] INT 
      ,[Monitor] NVARCHAR (50)
      ,[Elemento]  NVARCHAR (50)
      ,[TimeStep] INT
      ,[Measurement]  NVARCHAR (50)
      ,[Value] FLOAT
);



DECLARE @Simulation INT;
SET @Simulation = 6;

SELECT @Simulation

INSERT INTO #PVP1
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%' AND Measurement LIKE ' P1 (kW)' AND Simulation = @Simulation



INSERT INTO #PVP2
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%' AND Measurement LIKE ' P2 (kW)' AND Simulation = @Simulation



INSERT INTO #PVP3
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%' AND Measurement LIKE ' P3 (kW)' AND Simulation = @Simulation



INSERT INTO #PVQ1
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%' AND Measurement LIKE ' Q1 (kvar)' AND Simulation = @Simulation



INSERT INTO #PVQ2
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%'AND Measurement LIKE ' Q2 (kvar)' AND Simulation = @Simulation




INSERT INTO #PVQ3
		SELECT
			* 
		FROM tblMonitoresData
		WHERE Elemento like 'pvsystem_pv%' AND Measurement LIKE ' Q3 (kvar)' AND Simulation = @Simulation



DELETE #PVP1
DELETE #PVP2
DELETE #PVP3
DELETE #PVQ1
DELETE #PVQ2
DELETE #PVQ3



;WITH 
	AllDataPV AS (	
		SELECT -- * 
			#PVP1.[Case]
			, #PVP1.Simulation
			, #PVP1.Elemento
			, #PVP1.TimeStep
			, #PVP1.[Value] AS LP1_VALUE
			, #PVP2.[Value] AS LP2_VALUE
			, #PVP3.[Value] AS LP3_VALUE
			, #PVQ1.[Value] AS LQ1_VALUE
			, #PVQ2.[Value] AS LQ2_VALUE
			, #PVQ3.[Value] AS LQ3_VALUE

		FROM #PVP1
		FULL JOIN #PVP2 ON
			#PVP1.[Case] = #PVP2.[Case] AND #PVP1.Elemento = #PVP2.Elemento AND #PVP1.Monitor = #PVP2.Monitor AND #PVP1.TimeStep = #PVP2.TimeStep
		FULL JOIN #PVP3 ON
			#PVP1.[Case] = #PVP3.[Case] AND #PVP1.Elemento = #PVP3.Elemento AND #PVP1.Monitor = #PVP3.Monitor AND #PVP1.TimeStep = #PVP3.TimeStep
		FULL JOIN #PVQ1 ON
			#PVP1.[Case] = #PVQ1.[Case] AND #PVP1.Elemento = #PVQ1.Elemento AND #PVP1.Monitor = #PVQ1.Monitor AND #PVP1.TimeStep = #PVQ1.TimeStep
		FULL JOIN #PVQ2 ON
			#PVP1.[Case] = #PVQ2.[Case] AND #PVP1.Elemento = #PVQ2.Elemento AND #PVP1.Monitor = #PVQ2.Monitor AND #PVP1.TimeStep = #PVQ2.TimeStep
		FULL JOIN #PVQ3 ON
			#PVP1.[Case] = #PVQ3.[Case] AND #PVP1.Elemento = #PVQ3.Elemento AND #PVP1.Monitor = #PVQ3.Monitor AND #PVP1.TimeStep = #PVQ3.TimeStep
	),
	calc_loas_s_PV AS (
		SELECT 
			AllDataPV.[Case]
			, AllDataPV.Simulation
			, AllDataPV.Elemento
			, AllDataPV.TimeStep
			, ( ISNULL(AllDataPV.LP1_VALUE, 0) + ISNULL(AllDataPV.LP2_VALUE, 0) + ISNULL(AllDataPV.LP3_VALUE, 0)) AS Sum_P
			, ( ISNULL(AllDataPV.LQ1_VALUE, 0) + ISNULL(AllDataPV.LQ2_VALUE, 0) + ISNULL(AllDataPV.LQ3_VALUE, 0)) AS Sum_Q
			, SQRT( POWER((ISNULL(AllDataPV.LP1_VALUE, 0) + ISNULL(AllDataPV.LP2_VALUE, 0) + ISNULL(AllDataPV.LP3_VALUE, 0)), 2) 
				+ POWER((ISNULL(AllDataPV.LQ1_VALUE, 0) + ISNULL(AllDataPV.LQ2_VALUE, 0) + ISNULL(AllDataPV.LQ3_VALUE, 0)), 2) ) AS sum_S
		FROM AllDataPV
	),
	GroupDATA AS (

		SELECT 
			[Case]
			, MAX(Sum_S) AS MAX_SUM
			, SUM(Sum_S)/4 AS ENERGY
		FROM calc_loas_s_PV
		GROUP BY [Case]
		--ORDER BY [Case]
	)

	SELECT
		--*
		AVG(MAX_SUM), AVG(ENERGY)
	FROM GroupDATA