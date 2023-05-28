

from matplotlib import pyplot as plt


def DrawF(people):
    y1 = [i[1] for i in people.record_fatigue ]
    x1 = [i[0] for i in people.record_fatigue ]

    plt.plot(x1, y1, label='fatigue', linewidth=1, color='r', marker='o',
             markerfacecolor='blue', markersize=2)

    plt.xlabel('time')
    plt.ylabel('fatigue')
    plt.legend()
    plt.show()
