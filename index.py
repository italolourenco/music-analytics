import pandas as pd
import matplotlib.pylab as plt

s60DataSetClear = 'data/clearData/musicReport-ClearData-60.csv'
s60DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s70DataSetClear = 'data/clearData/musicReport-ClearData-70.csv'
s70DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s80DataSetClear = 'data/clearData/musicReport-ClearData-80.csv'
s80DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s90DataSetClear = 'data/clearData/musicReport-ClearData-90.csv'
s90DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s2000DataSetClear = 'data/clearData/musicReport-ClearData-2000.csv'
s2000DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s2010DataSetClear = 'data/clearData/musicReport-ClearData-2010.csv'
s2010DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

def generateGraphOfNumberOfSongsPerDecade(decades, qtyPerDecade):
    plt.bar(decades, qtyPerDecade)
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/graphNumberOfSongPerDecade.png', transparent = True)


def main():

    decades = ['60', '70', '80', '90', '2000', '2010']
    qtyPerDecade = []

    listPathClearData = [s60DataSetClear, s70DataSetClear, s80DataSetClear, s90DataSetClear, s2000DataSetClear, s2010DataSetClear]

    listPathStemmingData = [s60DataSetStemming, s70DataSetStemming, s80DataSetStemming, s90DataSetStemming, s2000DataSetStemming, s2010DataSetStemming]

    for path in listPathClearData:
        df = pd.read_csv(path, sep = ';')
        length = df.size
        qtyPerDecade.append(length)

    generateGraphOfNumberOfSongsPerDecade(decades, qtyPerDecade)


if __name__ == '__main__':
	main()