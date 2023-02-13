from collections import Counter     #comes with Python, does not need to be installed
import spacy                        #needs to be installed
import en_core_web_sm               #install with python -m spacy download en_core_web_sm
import fi_core_news_sm              #install with python -m spacy download fi_core_news_sm
import pandas as pd                 #needs to be installed
import matplotlib.pyplot as plt     #needs to be installed
import seaborn as sns               #needs to be installed


# a function for choosing the language of the data (Finnish or English) 
def choose_language():  
    language = input('Write "english" for English data, write "finnish" for Finnish data: ')   #the user chooses english or finnish
    if language == "finnish":           #if the chosen language is Finnish, the Finnish data will be loaded
        finnish = open("finnish.txt")
        finnish = finnish.read()  
        nlp = fi_core_news_sm.load()    
        doc = nlp(finnish)              #lemmatizes and tokenizes the data using Spacy
        return doc                      #returns the Finnish preprocessed data
    elif language == "english":         #if the chosen language is English, the English data will be loaded
        english = open("english.txt")
        english = english.read() 
        nlp = en_core_web_sm.load()
        doc = nlp(english)              #lemmatizes and tokenizes the data using Spacy
        return doc                      #returns the English preprocessed data
    else: 
        print('\n', '"',language,'"', 'is not an option.')      #if neither English or Finnish is chosen, the program tells you that whatever you wrote isn't an option...
        choose_language()                                       #...and you are sent back to the beginning of choose_language() where it prompts you to choose english or finnish again


# a function for normalizing the data
def normalization(doc):
    words = [token.text
             for token in doc
             if not token.is_punct]             #removes punctuation 
    words_norm = [w.lower() for w in words]     #makes everything lowercase
    return words_norm                           #returns a list of normalized words


# a function that creates a dataframe using pandas, and plots the information onto a scatterplot using seaborn and matplotlib
def zipfslaw(words):
    df = pd.DataFrame.from_records(list(dict(Counter(words)).items()), columns=['word','frequency'])    #creates a dataframe with columns 'word' and 'frequency', taken from the tuple with each type and its number of occurences that the Counter() function creates
    df = df.sort_values(by=['frequency'], ascending=False)      #sorts the values in the dataframe by frequency so that the most frequent word is at the top
    df.drop(index=df.index[0],                                  #the most frequenct type in both the Finnish and English data is "\n", so this one is removed
            axis=0, 
            inplace=True)
    df['length']  = df['word'].str.len()                        #a new column "length" is created in the dataframe, containing the length of each type (word)
    sns.relplot(x="length", y="frequency", data=df);            #a scatterplot showing length on the x-axis and frequency on the y-axis is created
    plt.show()
    plt.close()


# the main function where zipfslaw() takes the normalized and tokenized words from normalization(), and normaliztion() takes the correct data from choose_language() depending on which language was chosen
def main():
    zipfslaw(normalization(choose_language()))      

main()