import spacy
import pandas as pd

def analyze(language, model, document):                                 #A function 'analyze' that takes the language, spacy model and dataset-document as arguments
    nlp = spacy.load(model)                                             #Loading the Spacy model
    df = pd.read_csv(document, sep='\t', comment='#', header=None, names=['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'])    #Opening up the file as a dataframe using pandas, and naming the columns
    df = df[['FORM', 'DEPREL']]                                         #Selecting the columns we need
    tokens = df.FORM.tolist()                                           #Taking the tokens from the sentences in the column "form" and putting them in a list
    tokens_string = ' '.join(tokens)                                    #Joining the tokens in the list into a string
    doc = nlp(tokens_string)                                            #Processing the tokens with the spacy model
    gold_deps = list(zip(df.FORM.tolist(), df.DEPREL.tolist()))         #Creating a list of tuples with the gold-standard dependencies
    predicted_deps = [(token.text, token.dep_) for token in doc]        #Creating a list of tuples with the predicted dependencies from Spacy

    mismatch = 0                                                        #A counter for mismatches
    match = 0                                                           #A counter for matches
    for i in range(len(gold_deps)):                                     #Iterating over the gold labels
        if gold_deps[i][1] != predicted_deps[i][1]:                     #If the n:th item of the gold labels is not equal to the n:th item of Spacy's predicted dependencies...
            mismatch += 1                                               #Add one to the mismatch-counter
        elif gold_deps[i][1] == predicted_deps[i][1]:                   #If the n:th item of the gold labels is equal to the n:th item of Spacy's predicted dependencies...
            match += 1                                                  #Add one to the match-counter
                 
    print('\n', language, ':\n', mismatch, 'mismatches\n', match, 'matches')    #Printing the number of matches and mismatches
    print(match / (mismatch + match) * 100, '%', 'correct')                     #Printing the accuracy as percentage correct

def main():                                                                     #The main function that runs 'analyze' twice, once with the English data and once with the Spanish data
    analyze('ENGLISH', "en_core_web_sm", 'en_lines-ud-dev.conllu.txt')
    analyze('SPANISH', "es_core_news_sm", 'es_ancora-ud-dev.conllu.txt')

main()    

