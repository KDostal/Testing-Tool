import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, data):
        self.data = data
    
    def visualize(self):
        # loop over the data and create a subplot for each dictionary
        for i, d in enumerate(self.data):
            plt.subplot(1, 3, i+1)
            plt.title(d["date"])
            # create two bars for dbTime and esTime
            plt.bar(["Database", "Elastic"], [d["dbTime"], d["esTime"]], color=["firebrick", "lightseagreen"])
            # add descriptions diffIndex, diffDbValue and diffEsValue
            offset = 0.05
            for j in range(len(d["diffIndex"])):
                plt.text(0, d["dbTime"] - offset, f"{d['diffIndex'][j]}: {d['diffDbValue'][j]}", ha="center", va="top")
                plt.text(1, d["esTime"] - offset, f"{d['diffIndex'][j]}: {d['diffEsValue'][j]}", ha="center", va="top")
                offset += 0.05
     
        plt.tight_layout()
        plt.show()