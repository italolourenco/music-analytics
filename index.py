import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns
import nltk
import numpy as np
import syllables



from nltk.tokenize import sent_tokenize, word_tokenize

from operator import itemgetter


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

decades = ['60', '70', '80', '90', '2000', '2010']

listPathClearData = [
    s60DataSetClear, s70DataSetClear, 
    s80DataSetClear, s90DataSetClear, 
    s2000DataSetClear, s2010DataSetClear
]

listPathStemmingData = [
    s60DataSetStemming, s70DataSetStemming, 
    s80DataSetStemming, s90DataSetStemming, 
    s2000DataSetStemming, s2010DataSetStemming
]

def readCSV(path):
    return pd.read_csv(path)


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
    dfData.to_csv('output.csv')
    # ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    # ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".15")
    # plt.xlabel("Década")
    # plt.ylabel("Quantidade")
    # plt.savefig('output/quantidadeDePalavrasPorMusicaSTEM.png', transparent = True)
    plt.show()


def processingCSV(path):
    df = pd.read_csv(path, sep = ';')


def musicRemoveSpecialCharacter(text):

    regex = re.compile(r'[-./?!,":;()```\']')
    filtered = [i for i in text if not regex.match(i)]
    return filtered


def processingText(text):
    
    tokens = word_tokenize(text.values[0])

    listClear = []

    for token in tokens:
        if(token != '[' and token != ']' and token != "'" and token != ","):
            listClear.append(token.replace("'", ""))

    return listClear

def getQtdWords(text):
    dist = nltk.FreqDist(text)

    return len(dist.items())

def countWords(text):

    wordUniques =[]
    wordRepeated = []

    fdist = nltk.FreqDist(text)

    for word, qtd in fdist.items():
        if(qtd == 1):
            wordUniques.append(word)
        else:
            wordRepeated.append(word)

    return (wordRepeated, wordUniques)
            
def tableCap4():
    baseStemming = {}
        
    dataFramesByStemmingData = []

    bd = []

    qtyWords = []
    decade = []

    for path in listPathStemmingData:
        df = readCSV(path)
        dataFramesByStemmingData.append(df)

    i = 0
    for df in dataFramesByStemmingData:
        baseStemming[decades[i]] = {}
        musicNames = list(df['Music'])
        count = []
        for name in musicNames:
            data = []
            data2 = []
            musicData = df[df['Music'] == name]

            artist = musicData['Artist'].values[0]

            data.append(artist)

            text = processingText(musicData['Text'])

            totalWords = getQtdWords(text)

            data.append(totalWords)

            wordCount = countWords(text)

            data.append(len(wordCount[0]))
            data.append(len(wordCount[1]))

            baseStemming[decades[i]][name] = data

            decade.append(decades[i])
            qtyWords.append(len(wordCount[0]))

            data2.append(name)
            data2.append(artist)
            data2.append(totalWords)
            data2.append(len(text))

            count.append(data2)
        
        bd.append(count)
        i = i + 1
    
    # data = {'decade': decade, 'len': qtyWords}

    # dfData = pd.DataFrame(data, columns=['decade', 'len'])

    # ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    # plt.xlabel("Década")
    # plt.ylabel("Quantidade")
    # plt.savefig('output/quantidadeDePalavrasRepetidasPorMusicaSTEM.png', transparent = True)
    # plt.show()

    x = 0
    for dataDecade in bd:
        print(decades[x])
        print(sorted(dataDecade, key=itemgetter(2)))
        x = x + 1

def plot_stacked_bar(data, series_labels, category_labels=None, 
                     show_values=False, value_format="{}", y_label=None, 
                     colors=None, grid=True, reverse=False):

    ny = len(data[0])
    ind = list(range(ny))

    axes = []
    cum_size = np.zeros(ny)

    data = np.array(data)

    print(data)

    if reverse:
        data = np.flip(data, axis=1)
        category_labels = reversed(category_labels)

    for i, row_data in enumerate(data):
        color = colors[i] if colors is not None else None
        axes.append(plt.bar(ind, row_data, bottom=cum_size, 
                            label=series_labels[i], color=color))
        cum_size += row_data

    if category_labels:
        plt.xticks(ind, category_labels)

    if y_label:
        plt.ylabel(y_label)

    plt.legend()

    if grid:
        plt.grid(b=None)


def generateGraphDataLoss():

    series_labels = ['Salvo', 'Outro Idioma', 'Não Encontrado']

    data = [
    [58, 51, 62, 44, 54, 72],
    [28, 35, 36, 47, 32, 17],
    [14, 14, 2, 9, 14, 11]
    ]

    category_labels = ['60', '70', '80', '90', '2000', '2010']

    plot_stacked_bar(
        data, 
        series_labels, 
        category_labels=category_labels, 
        show_values=True, 
        value_format="{:.1f}",
        colors=['tab:orange', 'tab:green', 'tab:blue'],
        y_label="Quantity (units)"
    )
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/loss.png', transparent = True)
    plt.show()

def main():


    dataMusicStruct = {}

    tableCap4()


    # generateGraphDataLoss()

    # print(baseStemming)


    #Gerar Graficos 

    # qtyPerDecade = []

    # for path in listPathClearData:
    #     df = pd.read_csv(path, sep = ';')
    #     length = df.size
    #     qtyPerDecade.append(length)

    # generateGraphOfNumberOfSongsPerDecade(decades, qtyPerDecade)


    # generateBoxPlotQtyWordsClearData(decades, listPathClearData, qtyPerDecade)
    # generateBoxPlotQtyWordsStemmingData(decades, listPathStemmingData, qtyPerDecade)


if __name__ == '__main__':
	main()