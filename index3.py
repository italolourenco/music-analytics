import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import syllables
from wordcloud import WordCloud


from operator import itemgetter


s60DataSetClear = 'data/clearData/musicReport-ClearData-60.csv'
s60DataSetStemming = 'data/stemmingData/musicReport-StemmingData-60.csv'
s60DataSetRaw = 'data/rawData/musicReport-60.csv'

s70DataSetClear = 'data/clearData/musicReport-ClearData-70.csv'
s70DataSetStemming = 'data/stemmingData/musicReport-StemmingData-70.csv'
s70DataSetRaw = 'data/rawData/musicReport-70.csv'

s80DataSetClear = 'data/clearData/musicReport-ClearData-80.csv'
s80DataSetStemming = 'data/stemmingData/musicReport-StemmingData-80.csv'
s80DataSetRaw = 'data/rawData/musicReport-80.csv'

s90DataSetClear = 'data/clearData/musicReport-ClearData-90.csv'
s90DataSetStemming = 'data/stemmingData/musicReport-StemmingData-90.csv'
s90DataSetRaw = 'data/rawData/musicReport-90.csv'

s2000DataSetClear = 'data/clearData/musicReport-ClearData-2000.csv'
s2000DataSetStemming = 'data/stemmingData/musicReport-StemmingData-2000.csv'
s2000DataSetRaw = 'data/rawData/musicReport-2000.csv'

s2010DataSetClear = 'data/clearData/musicReport-ClearData-2010.csv'
s2010DataSetStemming = 'data/stemmingData/musicReport-StemmingData-2010.csv'
s2010DataSetRaw = 'data/rawData/musicReport-2010.csv'

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

listPathRawData = [
    s60DataSetRaw, s70DataSetRaw,
    s80DataSetRaw, s90DataSetRaw,
    s2000DataSetRaw, s2010DataSetRaw
]

def readCSV(path):
    return pd.read_csv(path)

def loadDataFrames(listToReady):

    dataFramesByStemmingData = []

    for path in listToReady:
        df = readCSV(path)
        dataFramesByStemmingData.append(df)
    
    return dataFramesByStemmingData


def loadingAllDataByName(dataName):

    listToReady = []

    if(dataName == 'clear'):
        print('Ready Clear Data')
        listToReady = listPathClearData

    elif(dataName == 'stem'):
        print('Ready Clear Data')
        listToReady = listPathStemmingData

    else:
        print('Ready Raw Data')
        listToReady = listPathRawData
    
    print(listToReady)
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

def makeMusicInfo(musicData, decade):

    musicInfo = []

    # data = musicData.values[0]

    data = musicData

    musicName = data[0]
    artist = data[1]
    processedText = data[2]
    # processedText = processingText(data[2])
    qtyWordsByLenOfText = len(processedText)
    qtyWordsByFrequence = getQtdWordsByFrequence(processedText)

    calculedWords = countWords(processedText)

    calculedSyllables = calcSyllables(processedText)

    calculedChars = calcCharacters(processedText)

    musicInfo.extend([musicName, artist, 
                      processedText, qtyWordsByLenOfText, 
                      qtyWordsByFrequence, len(calculedWords[0]), 
                      len(calculedWords[1]), calculedWords[2], 
                      calculedSyllables[0], calculedSyllables[1],
                      calculedChars[0], calculedChars[1],
                      decade])

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
            #musicInfo[8] = Qty Syllables
            #musicInfo[9] = Average Syllables per word
            #musicInfo[10] = Qty Chars
            #musicInfo[11] = Average Chars per word
            #musicInfo[12] = Decade

            musicInfo = makeMusicInfo(musicData, decades[indexOfDecade]) 

            musicsForDecade.append(musicInfo)


        musicDataStruct[decades[indexOfDecade]] = musicsForDecade
        indexOfDecade += 1

    print(musicDataStruct)
    return musicDataStruct

def calculePercentile(values):
    return np.percentile(values, [25, 50, 75])

def calcInferiorLimite(values):
    return values[0] - (1.5 * (values[2] - values[0]))

def calcUpperLimite(values):
    return values[2] + (1.5 * (values[2] - values[0]))

def printGraphicSubtitle(values, percentiles, decade, text):

    inferiorLimite = calcInferiorLimite(percentiles)
    upperLimite = calcUpperLimite(percentiles)

    print(text + ' - ' + decade)
    # print('Inferior Limite : ' , inferiorLimite )
    # print(percentiles)
    print('Upper Limite : ' , upperLimite )
    print('Qty Out-of-limit elements :' , len(list(filter(lambda x: x > upperLimite, values))))

def generateBoxPlotQtyWordsByRawData(structBySteam):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Stem Data.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = structBySteam[decade]
        valuesToCalcPercentile = []
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[3])
            valuesToCalcPercentile.append(musicInfo[3])

        percentiles = calculePercentile(valuesToCalcPercentile)
        printGraphicSubtitle(valuesToCalcPercentile, percentiles, decade, 'Qty Words by Raw Data')
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])
    dfData.to_csv('outputRawData.csv')

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/quantidadeDePalavrasRAW.png', transparent = True)

    print(dfData.groupby(['decade'])['len'].describe())

def generateBoxPlotQtyWordsByStemData(structBySteam):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Stem Data.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = structBySteam[decade]
        valuesToCalcPercentile = []
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[4])
            valuesToCalcPercentile.append(musicInfo[4])

        percentiles = calculePercentile(valuesToCalcPercentile)
        printGraphicSubtitle(valuesToCalcPercentile, percentiles, decade, 'Qty Words by Stem Data')
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])
    dfData.to_csv('outputSteamData.csv')

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/quantidadeDePalavrasSTEM.png', transparent = True)

    print(dfData.groupby(['decade'])['len'].describe())

def generateBoxPlotQtyWordsRepeatedByStemData(structBySteam):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Stem Data.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = structBySteam[decade]
        valuesToCalcPercentile = []
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[6])
            valuesToCalcPercentile.append(musicInfo[6])

        percentiles = calculePercentile(valuesToCalcPercentile)
        printGraphicSubtitle(valuesToCalcPercentile, percentiles, decade, 'Qty Words Repeated by Stem Data')
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    plt.savefig('output/quantidadeDePalavrasRepetidasPorMusicaSTEM.png', transparent = True)

    print(dfData.groupby(['decade'])['len'].describe())


def generateBoxPlotQtyWordsByClearData(struct):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Clear.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = struct[decade]
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[4])
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])

    dfData.to_csv('outputClearData.csv')

    ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    plt.xlabel("Década")
    plt.ylabel("Quantidade")
    # plt.savefig('output/quantidadeDePalavrasClear.png', transparent = True)

    print(dfData.groupby(['decade'])['len'].describe())


def generateBoxPlotQtyWordsUniqueBySteamData(struct):
    #incluir gráfico do tipo boxplot com a quantidade de palavras por música (eixo y) por década (eixo x) da BASE Clear.

    qtyWords = []
    decadesF = []

    for decade in decades:
        listMusics = struct[decade]
        valuesToCalcPercentile = []
        for musicInfo in listMusics:
            decadesF.append(decade)
            qtyWords.append(musicInfo[5])
            valuesToCalcPercentile.append(musicInfo[5])

        percentiles = calculePercentile(valuesToCalcPercentile)
        printGraphicSubtitle(valuesToCalcPercentile, percentiles, decade, 'Qty Words Uniques by Stem Data')
    
    data = {'decade': decadesF, 'len': qtyWords}
    dfData = pd.DataFrame(data, columns=['decade', 'len'])

    # ax = sns.boxplot(x="decade", y="len", data=dfData, order=decades)
    # ax = sns.swarmplot(x="decade", y="len", data=dfData, order=decades, color=".35")
    # plt.xlabel("Década")
    # plt.ylabel("Quantidade")
    # plt.savefig('output/quantidadeDePalavrasUnicasSteam.png', transparent = True)

    print(dfData.groupby(['decade'])['len'].describe())



def generateGraphs(structBySteam, structByClear, structByRaw):
    # generateBoxPlotQtyWordsByClearData(structByClear)
    # generateBoxPlotQtyWordsByStemData(structBySteam)
    # generateBoxPlotQtyWordsRepeatedByStemData(structBySteam)
    generateBoxPlotQtyWordsUniqueBySteamData(structBySteam)

    # generateBoxPlotQtyWordsByRawData(structByRaw)

def printMusicList(musics, orderBy, type):
    
    print(orderBy)
    if(type == 'general'):
        for music in musics:
            print(music[0], music[1], music[12], music[4], music[9], music[11] )
    else:
        for music in musics:
            print(music[0], music[1], music[4])

def generateTablesByDecade(structBySteam):
    for decade in decades:
        print(decade)
        orderedList = sorted(structBySteam[decade], key=itemgetter(4))
        printMusicList(orderedList[:11], "first", "decade")
        printMusicList(orderedList[-11:], "last", "decade")

def gerenateTableGeneral(struct):
    allMusics = []

    for decade in decades:
        musicsByDecade = struct[decade]
        allMusics.extend(musicsByDecade)

    orderedList = sorted(allMusics, key=itemgetter(4))
    printMusicList(orderedList[:12], "first", "general")
    printMusicList(orderedList[-12:], "last", "general")


def calcSyllables(text):

    qtyWords = getQtdWordsByFrequence(text)
    
    fdist = nltk.FreqDist(text)

    countSyllables = 0

    for word, qtd in fdist.items():
        countSyllables = syllables.estimate(word) + countSyllables
    
    averageSyllables = countSyllables / qtyWords
    return (countSyllables, averageSyllables)

def calcCharacters(text):

    qtyWords = getQtdWordsByFrequence(text)

    qtyChars = 0

    fdist = nltk.FreqDist(text)
    for word, qtd in fdist.items():
       qtyChars = len(word) + qtyChars

    averageChars = qtyChars / qtyWords

    return (qtyChars, averageChars)

def gerenateWordCloud(struct):
    allMusicsForDataSets = []

    x = 0
    for decade in decades:
        allMusicsForDecade = []
        musicsByDecade = struct[decade]
        for musicInfo in musicsByDecade:
            allMusicsForDecade.extend(musicInfo[2])
            allMusicsForDataSets.extend(musicInfo[2])
        
        fdist = nltk.FreqDist(allMusicsForDecade)
        d = {}
        for word, qtd in fdist.items():
            d[word] = qtd
        wordcloud = WordCloud()
        wordcloud.generate_from_frequencies(frequencies=d)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('output/wordcloud-' + decades[x] +'.png', transparent = True)
        x = x + 1

    
    fdist = nltk.FreqDist(allMusicsForDataSets)
    c = {}
    for word, qtd in fdist.items():
            c[word] = qtd
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=c)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('output/wordcloud-All.png', transparent = True)
    allMusicsForDataSets




            
        # allMusics.extend(musicsByDecade)



def main():

    # structBySteam = createMusicDataStruct('stem')
    # structByClear = createMusicDataStruct('clear')
    # structByRaw = createMusicDataStruct('raw')

    # structBySteam = []
    # structByClear = []
    # structByRaw = []

    # generateGraphs(structBySteam, structByClear, structByRaw)
    # generateTablesByDecade(structBySteam)
    # gerenateTableGeneral(structBySteam)
    # gerenateWordCloud(structByRaw)

    test = ["CabeçaDino", "Titas", ['cabeç', 'dinossaur', 'cabeç', 'dinossaur', 'cabeç', 'cabeç', 'cabeç', 'dinossaur', 'panç', 'mamut', 'panç', 'mamut', 'panç', 'panç', 'panç', 'mamut', 'espírit', 'porc', 'espírit', 'porc', 'espírit', 'porc']]

    musicInfo = makeMusicInfo(test, 60) 

    print(musicInfo)



if __name__ == '__main__':
	main()