from collections import Counter
import spacy
import en_core_web_sm
import fi_core_news_sm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")


def choose_language():
    
    language = input('Write "english" for English data, write "finnish" for Finnish data:  ')
    if language == "finnish":
        finnish = open("finnish.txt")
        finnish = finnish.read()  
        nlp = fi_core_news_sm.load()
        doc = nlp(finnish)
        return doc
    elif language == "english":
        english = open("english.txt")
        english = english.read() 
        nlp = en_core_web_sm.load()
        doc = nlp(english)
        return doc
    else: 
        print('\n', '"',language,'"', 'is not an option.')
        choose_language()


def normalization(doc):
    words = [token.text
             for token in doc
             if not token.is_punct]

    words_norm = [w.lower() for w in words]
    return words_norm


def zipfslaw(words):
    df = pd.DataFrame.from_records(list(dict(Counter(words)).items()), columns=['word','frequency'])
    df = df.sort_values(by=['frequency'], ascending=False)

    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)

    df['length']  = df['word'].str.len()

    sns.relplot(x="length", y="frequency", data=df);
    plt.show()
    plt.close()


def main():

    zipfslaw(normalization(choose_language()))


main()


        


