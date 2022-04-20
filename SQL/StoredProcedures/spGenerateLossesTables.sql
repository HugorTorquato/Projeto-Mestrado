select * from PVSystems
select  * from MonitoresData_2 where Simulation =1

SELECT * FROM Summary_Losses 
select * from Losses

EXEC spGenerateLossesTables
GO

select * from MonitoresData_2 MD
WHERE Measurement like ' watts' and 
MD.Elemento = 'line._abcn_l01-sec' and Monitor like 'line__abcn_l01-sec_loss'
AND Simulation=1