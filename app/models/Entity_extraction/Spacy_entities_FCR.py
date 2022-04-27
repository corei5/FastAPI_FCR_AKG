# import spacy
# nlp = spacy.load("en_core_web_sm")
import en_core_web_trf
nlp1 = en_core_web_trf.load()

def spacy_entities_FCE(text):
    doc = nlp1(text)
    return ([(X.text, X.label_) for X in doc.ents])