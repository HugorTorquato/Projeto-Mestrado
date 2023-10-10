import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the desired plots to run
    DO_FirstPlot = 0
    DO_BatBySize = 0  # Devide batery sizing by range and put them together
    DO_VWHCDiff = 0   # Plot the HC diference btween each simulation for diferente VW ranges
    DO_PowerLoss = 0   # Plot the power reduction caused by VW controls
    DO_StatHC = 0
    DO_PlotControl = 0
    DO_BESSAVGResults = 0
    DO_TripleHC = 0
    DO_TripleBESS = 0
    DO_Partialctivation = 0
    DO_ActivationCountByPVNumbers = 0
    DO_ActivationCountByPVNumbersPLOT = 0
    DO_a3dplot = 0
    DO_FindBusMostCommonActivations = 0
    DO_XR = 0
    DO_LoadPowerShape = 0
    DO_HCComparison = 1
    DO_LoadDemand = 0


    # Actually Plot call
    if DO_FirstPlot:
        import FirstPlot
    if DO_BatBySize:
        import BatBySize
    if DO_VWHCDiff:
        import VWHCDiff
    if DO_PowerLoss:
        import PowerLoss
    if DO_StatHC:
        import StatHC
    if DO_PlotControl:
        import PlotControl
    if DO_BESSAVGResults:
        import BESSAVGResults
    if DO_TripleHC:
        import TripleHC
    if DO_TripleBESS:
        import TripleBESS
    if DO_Partialctivation:
        import Partialctivation
    if DO_ActivationCountByPVNumbers:
        import ActivationCountByPVNumbers
    if DO_ActivationCountByPVNumbersPLOT:
        import DO_ActivationCountByPVNumbersPLOT
    if DO_a3dplot:
        import a3dplot
    if DO_FindBusMostCommonActivations:
        import FindBusMostCommonActivations
    if DO_XR:
        import XR
    if DO_LoadPowerShape:
        import LoadPowerShape
    if DO_HCComparison:
        import HCComparison
    if DO_LoadDemand:
        import LoadDemand




    plt.show()
