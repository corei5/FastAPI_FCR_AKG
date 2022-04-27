import spacy
import scispacy
import en_core_sci_lg
import en_core_sci_scibert
import en_ner_craft_md
import en_ner_bionlp13cg_md
import en_ner_jnlpba_md

nlp  = en_core_sci_scibert.load()
# nlp = en_core_sci_lg.load()
# bionlp = en_ner_bionlp13cg_md.load()
# jnlpba = en_ner_jnlpba_md.load()
# craft = en_ner_craft_md.load()

def scispacy_entities_extraction(text):
    ent_nlp = nlp(text)
    # ent_bionlp = bionlp(text)
    # ent_craft = craft(text)
    # ent_jnlpba = jnlpba(text)
    all_ents = set(ent_nlp.ents)#set(ent_nlp.ents + ent_bionlp.ents + ent_craft.ents + ent_jnlpba.ents)
    # new - lemmatization
    #all_ents = map(lambda x: x.lemma_, all_ents)

    # TODO it would be better to sanitize entities with non-ascii char rather than completely remove them
    #all_ents = filter(lambda x: not (is_not_ascii(str(x))), all_ents)

    return all_ents