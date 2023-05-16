import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the desired plots to run
    DO_FirstPlot = 0
    DO_BatBySize = 0  # Devide batery sizing by range and put them together
    DO_VWHCDiff = 0   # Plot the HC diference btween each simulation for diferente VW ranges
    DO_PowerLoss = 0   # Plot the power reduction caused by VW controls
    DO_StatHC = 1

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


    plt.show()
