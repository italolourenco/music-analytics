import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns

s60DataSetClear = 'data/clearData/musicReport-ClearData-60.csv'
s60DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'

s70DataSetClear = 'data/clearData/musicReport-ClearData-70.csv'
s70DataSetStemming = 'data/stemmingData/musicReport-StemmingData-70.csv'

s80DataSetClear = 'data/clearData/musicReport-ClearData-80.csv'
s80DataSetStemming = 'data/stemmingData/musicReport-StemmingData-80.csv'

s90DataSetClear = 'data/clearData/musicReport-ClearData-90.csv'
s90DataSetStemming = 'data/stemmingData/musicReport-StemmingData-90.csv'

s2000DataSetClear = 'data/clearData/musicReport-ClearData-2000.csv'
s2000DataSetStemming = 'data/stemmingData/musicReport-StemmingData-2000.csv'

s2010DataSetClear = 'data/clearData/musicReport-ClearData-2010.csv'
s2010DataSetStemming = 'data/stemmingData/musicReport-StemmingData-2010.csv'


def readCSV(path):
    return pd.read_csv(path, sep = ';')


def generateGraphOfNumberOfSongsPerDecade(decades, qtyPerDecade):
    plt.bar(decades, qtyPerDecade)
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/graphNumberOfSongPerDecade.png', transparent = True)


def generateBoxPlotQtyWordsClearData(decades, listPathClearData, qtyPerDecade):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE LIMPA.

    qtyWords = []
    decade = []

    i = 0
    for path in listPathClearData:
        df = pd.read_csv(path)
        totalWords = 0
        texts = list(df['Text'])
        for text in texts:
            words = text.split(",")
            decade.append(decades[i])
            qtyWords.append(len(words))
        i = i + 1
    
    data = {'decade': decade, 'len': qtyWords}

    dfData = pd.DataFrame(data, columns=['decade', 'len'])
    dfData.boxplot(column='len', by='decade', showfliers=False)
    plt.show()


def generateBoxPlotQtyWordsStemmingData(decades, listPathStemmingData, qtyPerDecade):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE LEMATIZADA

    qtyWords = []
    decade = []

    i = 0
    for path in listPathStemmingData:
        df = pd.read_csv(path)
        totalWords = 0
        texts = list(df['Text'])
        for text in texts:
            words = text.split(",")
            decade.append(decades[i])
            qtyWords.append(len(words))
        i = i + 1
    
    data = {'decade': decade, 'len': qtyWords}

    dfData = pd.DataFrame(data, columns=['decade', 'len'])
    dfData.boxplot(column='len', by='decade', showfliers=False)
    plt.show()


def processingDF(path):
    df = pd.read_csv(path, sep = ';')




    return True

def main():

    decades = ['60', '70', '80', '90', '2000', '2010']
    qtyPerDecade = []

    listPathClearData = [s60DataSetClear, s70DataSetClear, s80DataSetClear, s90DataSetClear, s2000DataSetClear, s2010DataSetClear]

    listPathStemmingData = [s60DataSetStemming, s70DataSetStemming, s80DataSetStemming, s90DataSetStemming, s2000DataSetStemming, s2010DataSetStemming]

    for path in listPathClearData:
        df = pd.read_csv(path, sep = ';')
        length = df.size
        qtyPerDecade.append(length)

    # generateGraphOfNumberOfSongsPerDecade(decades, qtyPerDecade)


    # generateBoxPlotQtyWordsClearData(decades, listPathClearData, qtyPerDecade)
    # generateBoxPlotQtyWordsStemmingData(decades, listPathStemmingData, qtyPerDecade)


if __name__ == '__main__':
	main()