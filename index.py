import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns

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
    dfData.boxplot(column='len', by='decade', showfliers=False)
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
    return len(text)

def countWords(text):

    wordUniques =[]
    wordRepits = []

    for word in text:
        if(text.count(word) == 1):
            wordUniques.append(word)
        else:
            wordRepits.append(word)

    return (wordRepits, wordUniques)
            


def main():

    baseStemming = {}

    #Mega Struct
    #baseStemming{
        # decade : {
        #   musicName : [artist, quantidade de palavras, quantidade de palavras repetidas, quantidade de palavras unicas, [textMusic]]
        # }
    #  }
    
    dataFramesByStemmingData = []

    bd = []

    qtyWords = []
    decade = []

    for path in listPathStemmingData:
        df = readCSV(path)
        dataFramesByStemmingData.append(df)

    i = 0
    listWordsRepts = []
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
            data2.append(len(wordCount[1]))

            count.append(data2)
        
        bd.append(count)


        # listWordsRepts.append(totalRepit)
        i = i + 1
    
    # data = {'decade': decade, 'len': qtyWords}

    # dfData = pd.DataFrame(data, columns=['decade', 'len'])
    # # dfData.to_csv("output.csv")
    # dfData.boxplot(column='len', by='decade', showfliers=False)
    # plt.xlabel("Década")
    # plt.ylabel("Quantidade de Palavras Repetidas")
    # plt.title("")
    # plt.show()


    x = 0
    for dataDecade in bd:
        print(decades[x])
        print(sorted(dataDecade, key=itemgetter(2)))
        x = x + 1

    # print(baseStemming)




    # for decade in decades:
    #     musics = baseStemming[decade]
    #     newlist = sorted(ut, key=lambda x: musics, reverse=True)
    #     print(musics)
        # for music in musics:
        #     print(baseStemming[decade][music])
        

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