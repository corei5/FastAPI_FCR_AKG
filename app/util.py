import pandas as pd
import pickle
import json
from fastapi import HTTPException

# Transformers ROBERTA-large
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('stsb-roberta-large')
# Transformers BERT
model_bert = SentenceTransformer('bert-base-nli-mean-tokens')

from models.Selected_Claim_transformers import selected_claim,store_selected_claim
from models.Entity_extraction.dbpedia_spotlight_entities import dbp
from models.Entity_extraction.ConceptNet import conceptNetExpansion
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from models.Data_processing.Split_tokenizer import split_tokenizer
from models.Selected_Claim_vectorizer import Selected_Claim


class Model:
    # def __init__(self):

    def corpus_embeddings_ROBERTA_large(self, parameter):
        if parameter is True:
            claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
            pickle_path = 'Dataset/pickle/Transformer_similarity_embedding_model_ROBERTA_large.pickle'
            try:
                claim_df = pd.read_csv(claim_file_path)
                corpus_embeddings = model.encode(claim_df['calim_cleaned'], convert_to_tensor=True)
                with open(pickle_path, 'wb') as pkl:
                    pickle.dump(corpus_embeddings, pkl)
                return "Transformer similarity embedding model ROBERTA large is saved as pickle."
            except ValueError:
                raise HTTPException(status_code=404,
                                    detail=f"Getting error for embedding model using ROBERTA large.")
        else:
            return "Transformer similarity embedding model ROBERTA large is already in your server."

    def corpus_embeddings_BERT(self, parameter):
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        pickle_path = 'Dataset/pickle/Transformer_similarity_embedding_model_Transformers_BERT.pickle'
        if parameter is True:
            try:
                claim_df = pd.read_csv(claim_file_path)
                corpus_embeddings_bert = model_bert.encode(claim_df['calim_cleaned'], convert_to_tensor=True)
                with open(pickle_path, 'wb') as pkl:
                    pickle.dump(corpus_embeddings_bert, pkl)
                return "Transformer similarity embedding model Transformers BERT is saved as pickle."
            except ValueError:
                raise HTTPException(status_code=404,
                                    detail=f"Getting error for embedding model using BERT.")
        else:
            return "Transformer similarity embedding model Transformers BERT is already in your server."

    def transformers_claim_for_ROBERTA_large(self, top_k: int, search_terms):
        try:
            file_name = 'Dataset/pickle/Transformer_similarity_embedding_model_ROBERTA_large.pickle'
            claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
            with open(file_name, 'rb') as pkl:
                corpus_embeddings = pickle.load(pkl)
            claim_df = pd.read_csv(claim_file_path)
            # encode sentence to get sentence embeddings
            sentence_embedding = model.encode(search_terms, convert_to_tensor=True)
            # compute similarity scores of the sentence with the corpus
            cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]
            # top_k results to return
            # Sort the results in decreasing order and get the first top_k
            list_of_selected_claim_biblo = selected_claim(cos_scores, claim_df, top_k)
            return list_of_selected_claim_biblo
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid input. Please enter a positive integer and search terms")

    def store_transformers_claim_for_ROBERTA_large(self, threshold: float, search_terms):
        try:
            file_name = 'Dataset/pickle/Transformer_similarity_embedding_model_ROBERTA_large.pickle'
            claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
            folder_path = "dump/ROBERTA/"
            with open(file_name, 'rb') as pkl:
                corpus_embeddings = pickle.load(pkl)
            claim_df = pd.read_csv(claim_file_path)
            # encode sentence to get sentence embeddings
            sentence_embedding = model.encode(search_terms, convert_to_tensor=True)
            # compute similarity scores of the sentence with the corpus
            cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]
            store_selected_claim_ = store_selected_claim(cos_scores, claim_df, threshold, search_terms, folder_path)
            return store_selected_claim_
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid input. Please enter a positive threshold and search terms")

    def transformers_claim_for_BERT(self, top_k: int, search_terms):
        try:
            file_name = 'Dataset/pickle/Transformer_similarity_embedding_model_Transformers_BERT.pickle'
            claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
            with open(file_name, 'rb') as pkl:
                corpus_embeddings_bert = pickle.load(pkl)
            claim_df = pd.read_csv(claim_file_path)
            # encode sentence to get sentence embeddings
            sentence_embedding = model_bert.encode(search_terms, convert_to_tensor=True)
            # compute similarity scores of the sentence with the corpus
            cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings_bert)[0]
            # top_k results to return
            # Sort the results in decreasing order and get the first top_k
            list_of_selected_claim = selected_claim(cos_scores, claim_df, top_k)
            return list_of_selected_claim
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid input. Please enter a positive integer and search terms")

    def store_transformers_claim_for_BERT(self, threshold: float, search_terms):
        try:
            file_name = 'Dataset/pickle/Transformer_similarity_embedding_model_Transformers_BERT.pickle'
            claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
            folder_path = "dump/BERT/"
            with open(file_name, 'rb') as pkl:
                corpus_embeddings = pickle.load(pkl)
            claim_df = pd.read_csv(claim_file_path)
            # encode sentence to get sentence embeddings
            sentence_embedding = model_bert.encode(search_terms, convert_to_tensor=True)
            # compute similarity scores of the sentence with the corpus
            cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]
            store_selected_claim_ = store_selected_claim(cos_scores, claim_df, threshold, search_terms, folder_path)
            return store_selected_claim_
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid input. Please enter a positive threshold and search terms")

    def TfidfVectorizer_with_DBpedia_spotlight(self, top_k: int, search_terms):
        min_df = 32
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        claim_df = pd.read_csv(claim_file_path)
        try:
            search_terms_spotlight = dbp(search_terms)
            vectorized_spotlight = TfidfVectorizer(analyzer="word",
                                                   tokenizer=split_tokenizer,
                                                   ngram_range=(1, 3),
                                                   lowercase=True,
                                                   strip_accents="ascii",
                                                   binary=True,
                                                   stop_words='english',
                                                   min_df=min_df
                                                   )
            selected_claims = Selected_Claim(vectorized_spotlight, search_terms_spotlight, claim_df, top_k)
            return selected_claims
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail=f"Entity not found.")

    def CountVectorizer_with_DBpedia_spotlight(self, top_k: int, search_terms):
        min_df = 32
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        claim_df = pd.read_csv(claim_file_path)
        try:
            search_terms_spotlight = dbp(search_terms)
            vectorized_spotlight = CountVectorizer(analyzer="word",
                                                   tokenizer=split_tokenizer,
                                                   ngram_range=(1, 3),
                                                   lowercase=True,
                                                   strip_accents="ascii",
                                                   binary=True,
                                                   stop_words='english',
                                                   min_df=min_df
                                                   )
            selected_claims = Selected_Claim(vectorized_spotlight, search_terms_spotlight, claim_df, top_k)
            return selected_claims
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail=f"Entity not found."
            )

    def Extract_conceptnet_entities_with_DBpedia_spotlight(self, parameter):
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        claim_df = pd.read_csv(claim_file_path)
        if parameter is True:
            print("yes")
            try:
                claim_df['conceptnet_entities_for_dbpedia_spotlight'] = claim_df['dbpedia_spotlight_entities'].apply(
                    conceptNetExpansion)
                claim_df.to_csv('cord19-claimKG_with_conceptnet_entities_for_dbpedia_spotlight.csv', index=True,
                                index_label="id")
            except ValueError:
                raise HTTPException(status_code=404,
                                    detail=f"Getting error for extract ConceptNet entities.")
        else:
            return {'Messages': "ConceptNet entities for DBPedia is already in your server."}

    def ConceptNet_entity_extraction_from_DBpedia_entity(self, search_terms):
        search_terms_spotlight = dbp(search_terms)
        Dbp_entity = search_terms_spotlight.split(",")
        conceptnet_entity_list = []
        for i in range(0, len(Dbp_entity), 1):
            ans = conceptNetExpansion(Dbp_entity[i].lstrip().rstrip())
            for j in range(0, len(ans), 1):
                conceptnet_entity_list.append(ans[j])
        conceptnet_entity_list_str = ','.join(conceptnet_entity_list)
        return conceptnet_entity_list_str

    def TfidfVectorizer_with_conceptnet_entities(self, top_k: int, search_terms):

        min_df = 32
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        claim_df = pd.read_csv(claim_file_path)
        try:

            conceptnet_entity_list_str = self.ConceptNet_entity_extraction_from_DBpedia_entity(search_terms)
            vectorized_spotlight = TfidfVectorizer(analyzer="word",
                                                   tokenizer=split_tokenizer,
                                                   ngram_range=(1, 3),
                                                   lowercase=True,
                                                   strip_accents="ascii",
                                                   binary=True,
                                                   stop_words='english',
                                                   min_df=min_df
                                                   )
            selected_claims = Selected_Claim(vectorized_spotlight, conceptnet_entity_list_str, claim_df, top_k)
            return selected_claims
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail=f"Entity not found."
            )

    def CountVectorizer_with_conceptnet_entities(self, top_k: int, search_terms):
        min_df = 32
        claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
        claim_df = pd.read_csv(claim_file_path)
        try:
            conceptnet_entity_list_str = self.ConceptNet_entity_extraction_from_DBpedia_entity(search_terms)
            vectorized_spotlight = CountVectorizer(analyzer="word",
                                                   tokenizer=split_tokenizer,
                                                   ngram_range=(1, 3),
                                                   lowercase=True,
                                                   strip_accents="ascii",
                                                   binary=True,
                                                   stop_words='english',
                                                   min_df=min_df
                                                   )
            selected_claims = Selected_Claim(vectorized_spotlight, conceptnet_entity_list_str, claim_df, top_k)
            return selected_claims

        except ValueError:
            raise HTTPException(
                status_code=404,
                detail=f"Entity not found."
            )


model_ = Model()


def get_model():
    return model_
