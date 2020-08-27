import pandas as pd
import matplotlib.pylab as plt

s60DataSetClear = '/data/clearData/musicReport-ClearData-60.csv'
s60DataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

s70DataSetClear = '/data/clearData/musicReport-ClearData-70.csv'
s70DataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

s80DataSetClear = '/data/clearData/musicReport-ClearData-80.csv'
s80DataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

s90DataSetClear = '/data/clearData/musicReport-ClearData-90.csv'
s90DataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

s2000DataSetClear = '/data/clearData/musicReport-ClearData-2000.csv'
s2000ataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

s2010DataSetClear = '/data/clearData/musicReport-ClearData-2010.csv'
s2010ataSetStemming = '/data/stemmingData/musicReport-StemmingData-60.csv'

def main():

    decades = ['60', '70', '80', '90', '2000', '2010']

    listPathClearData = [s60DataSetClear, s70DataSetClear, s80DataSetClear, s90DataSetClear, s2000DataSetClear, s2010DataSetClear]

    listPathStemmingData = [s60ataSetStemming, s70ataSetStemming, s80ataSetStemming, s90ataSetStemming, s2000ataSetStemming, s2010ataSetStemming]


if __name__ == '__main__':
	main()