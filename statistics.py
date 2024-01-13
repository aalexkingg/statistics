import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def std(data):
    return np.sqrt(1/(len(data)-1) * np.sum(np.square(data - mean(data))))

def variance(data):
    return np.square(std(data))

def mean(data):
    return np.sum(data) / len(data)

def standard_dist(data):
    return (1 / (2 * np.pi)) * np.exp(-1/2 * np.square(data))

def norm_dist(data, std):
    return (1 / (std * np.sqrt(2*np.pi))) * np.exp(-(np.square(data-mean(data)))/(2*std**2))

def parent_dist(data):
    return np.sqrt(np.sum(np.unique(data) - mean(data)) / len(data))

def sample_dist(data):
    return np.sqrt(np.sum(np.square(data - mean(data))) / (len(data)-1))


if __name__ == "__main__":
    numOfDice = 4
    numOfRolls = 100000
    rolls = np.array([])

    for i in range(numOfRolls):
        rolls = np.append(rolls, np.sum(np.random.randint(low=0, high=7, size=numOfDice)))

    unique, count = np.unique(rolls, return_counts=True)
    count_prob = count / numOfRolls

    norm_parent = norm_dist(unique, sample_dist(rolls))
    print(norm_parent)

    plt.figure()
    plt.plot(unique, norm_parent)
    plt.show()

    plt.figure()
    plt.bar(unique, count_prob)

    norm = norm_dist(unique, std(rolls))
    plt.plot(unique, norm, '-', color='green', label='norm')

    norm_3 = norm_dist(unique, 5)
    plt.plot(unique, norm_3, '--', label='norm=5', color='orange')

    norm_2 = norm_dist(unique, 2)
    #plt.plot(unique, norm_2, '--', label='norm=2')

    norm_4 = norm_dist(unique, 4)
    plt.plot(unique, norm_4, '--', label='norm=4', color='red')

    plt.grid(True)
    plt.text(0, 0.095, "Num of dice: {0}".format(numOfDice))
    plt.text(0, 0.085, "Num of rolls: {0}".format(numOfRolls))
    plt.xlabel("Sum of Dice")
    plt.ylabel("Probability")
    plt.legend()
    plt.show()























