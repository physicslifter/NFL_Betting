from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
import pandas as pd
from matplotlib import animation
import time

gameID = 401437871

fig = plt.figure()
axhome = fig.add_subplot(1,2,1)
axaway = fig.add_subplot(1, 2, 2)
def animate(i):
    axhome.clear()
    axaway.clear()
    axhome.set_title("Eagles")
    axaway.set_title("Packers")
    data = pd.read_csv(f"LiveData/{str(gameID)}.csv")
    corrected_odds_data = 1 - data.iloc[:,4].astype(float)
    axhome.scatter(data.iloc[:,6], 100*corrected_odds_data)
    axhome.plot(data.iloc[:, 6], data.iloc[:,2])
    axaway.scatter(data.iloc[:,6], 100*data.iloc[:,3].astype(float))
    axaway.plot(data.iloc[:, 6], data.iloc[:,1])

ani = animation.FuncAnimation(fig, animate, interval=10)

plt.draw()
plt.show()

