import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the desired plots to run
    DO_FirstPlot = 0
    DO_BatBySize = 1  # Devide batery sizing by range and put them together
    DO_VWHCDiff = 1   # Plot the HC diference btween each simulation for diferente VW ranges


    # Actually Plot call
    if DO_FirstPlot:
        import FirstPlot
    if DO_BatBySize:
        import BatBySize
    if DO_VWHCDiff:
        import VWHCDiff


    plt.show()
