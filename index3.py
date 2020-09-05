import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns
import nltk
import numpy as np
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

def loadDataFrames(listToReady):

    dataFramesByStemmingData = []

    for path in listPathStemmingData:
        df = readCSV(path)
        dataFramesByStemmingData.append(df)
    
    return dataFramesByStemmingData


def loadingAllDataByName(dataName):

    listToReady = []

    if(dataName == 'clear'):
        listToReady = listPathClearData
    else:
        listToReady = listPathStemmingData
    
    return loadDataFrames(listToReady)

def countWords(text):

    wordUniques =[]
    wordRepeated = []

    fdist = nltk.FreqDist(text)
    countFrequenceWordsRepete = 0

    for word, qtd in fdist.items():
        if(qtd == 1):
            wordUniques.append(word)
        else:
            wordRepeated.append(word)
            countFrequenceWordsRepete = countFrequenceWordsRepete + qtd

    return (wordUniques, wordRepeated, countFrequenceWordsRepete)

def makeMusicInfo(musicData):

    musicInfo = []

    data = musicData.values[0]

    musicName = data[0]
    artist = data[1]
    processedText = processingText(data[2])
    qtyWordsByLenOfText = len(processedText)
    qtyWordsByFrequence = getQtdWordsByFrequence(processedText)

    calculedWords = countWords(processedText)

    musicInfo.extend([musicName, artist, processedText, qtyWordsByLenOfText, qtyWordsByFrequence, len(calculedWords[0]), len(calculedWords[1]), calculedWords[2]])

    return musicInfo

def processingText(text):
    
    tokens = word_tokenize(text)

    listClear = []

    for token in tokens:
        if(token != '[' and token != ']' and token != "'" and token != ","):
            listClear.append(token.replace("'", ""))

    return listClear

def getQtdWordsByFrequence(text):
    dist = nltk.FreqDist(text)

    return len(dist.items())


def createMusicDataStruct(name):

    musicDataStruct = {}

    allDataframes = loadingAllDataByName(name)

    indexOfDecade = 0
    for df in allDataframes:
        musicsForDecade = []
        musicNames = list(df['Music'])
        for music in musicNames:

            musicData = df[df['Music'] == music]

            #MusicInfo
            #musicInfo[0] = musicName
            #musicInfo[1] = artist
            #musicInfo[2] = text
            #musicInfo[3] = Qty Words by len of text
            #musicInfo[4] = Qty Words by Frequence
            #musicInfo[5] = Qty Words Unique
            #musicInfo[6] = Qty Repetitive Words
            #musicInfo[7] = Qty Frequence Repetitive Words  

            musicInfo = makeMusicInfo(musicData) 

            musicsForDecade.append(musicInfo)


        musicDataStruct[decades[indexOfDecade]] = musicsForDecade
        indexOfDecade += 1

    return musicDataStruct

def generateBoxPlotQtyWordsByStemData(structBySteam):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Stem Data.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = structBySteam[decade]
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[4])
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/quantidadeDePalavrasSTEM.png', transparent = True)


def generateBoxPlotQtyWordsRepeatedByStemData(structBySteam):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Stem Data.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = structBySteam[decade]
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[6])
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/quantidadeDePalavrasRepetidasPorMusicaSTEM.png', transparent = True)


def generateGraphs(structBySteam):
    generateBoxPlotQtyWordsByStemData(structBySteam)
    generateBoxPlotQtyWordsRepeatedByStemData(structBySteam)

def printMusicList(musics, orderBy):
    
    print(orderBy)
    for music in musics:
        print(music[0], music[1], music[4])

def generateTables(structBySteam):
    for decade in decades:
        print(decade)
        orderedList = sorted(structBySteam[decade], key=itemgetter(4))
        printMusicList(orderedList[:11], "first")
        printMusicList(orderedList[-11:], "last")


def main():

    structBySteam = createMusicDataStruct('stem')
    # generateGraphs(structBySteam)
    generateTables(structBySteam)


if __name__ == '__main__':
	main()