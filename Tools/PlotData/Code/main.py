import pythonsql
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the desired plots to run
    DO_FirstPlot = 0
    DO_BatBySize = 1  # Devide batery sizing by range and put them together

    # Actually Plot call
    if DO_FirstPlot:
        import FirstPlot
    if DO_BatBySize:
        import BatBySize

    plt.show()
