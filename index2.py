import pandas as pd
import matplotlib.pylab as plt
import re
import seaborn as sns
import nltk

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
    wordRepeated = []

    fdist = nltk.FreqDist(text)

    print(len(fdist.items()))

    for word, qtd in fdist.items():
        if(qtd == 1):
            wordUniques.append(word)
        else:
            wordRepeated.append(word)

    return (wordRepeated, wordUniques)
            


def main():

    tokens = word_tokenize("cabeça dinossauro cabeça dinossauro cabeça cabeça cabeça dinossauro pança de mamute pança de mamute pança pança pança de mamute espírito de porco espírito de porco espírito de porco")

    print(tokens)

    a = countWords(tokens)
    print(len(a[0]))
    print(len(a[1]))


if __name__ == '__main__':
	main()