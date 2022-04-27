import logging
import logging.config
import yaml

import pandas as pd
import pickle
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Transformers ROBERTA-large
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('stsb-roberta-large')
# Transformers BERT
model_bert = SentenceTransformer('bert-base-nli-mean-tokens')

from models.Selected_Claim_transformers import selected_claim
from models.Entity_extraction.dbpedia_spotlight_entities import dbp
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from models.Data_processing.Split_tokenizer import split_tokenizer
from  models.Selected_Claim_vectorizer import Selected_Claim

app = FastAPI()

# Load logger config
# with open('logger.yaml', 'r') as f:
#     config = yaml.safe_load(
#         f.read())
#     logging.config.dictConfig(
#         config)

# Create a custom logger
logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(
        f"URL: {request.url}")
    logger.error(
        f"user input: {request.path_params}")
    logger.error(
        f"status code: {status.HTTP_422_UNPROCESSABLE_ENTITY}")
    logger.error(jsonable_encoder(
        {"detail": exc.errors()}))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": exc.errors()}),
    )


@app.get('/api/v1/Transformers/embeddings_ROBERTA/{parameter}')
# Claim embeddings using ROBERTA large transformer
async def corpus_embeddings_ROBERTA_large(parameter):
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


@app.get('/api/v1/Transformers/embeddings_BERT/{parameter}')
# Claim embeddings using BERT transformer
async def corpus_embeddings_Transformers_BERT(parameter):
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


@app.get("/api/v1/Transformers/ROBERTA/{top_k}/{search_terms}")
async def transformers_claim_for_ROBERTA_large(top_k: int, search_terms):
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
        list_of_selected_claim = selected_claim(cos_scores, claim_df, top_k)
        return list_of_selected_claim
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid input. Please enter a positive integer and search terms")

@app.get("/api/v1/Transformers/BERT/{top_k}/{search_terms}")
async def transformers_calim_for_Transformers_BERT(top_k: int, search_terms):
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

@app.get('/api/v1/Vectorizer/TfidfVectorizer/{top_k}/{search_terms}')
#API for return N selected claims for a string (that is provided by the fact checkers) using TfidfVectorizer
async def TfidfVectorizer_with_DBpedia_spotlight(top_k: int, search_terms):
    min_df = 32
    claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
    claim_df = pd.read_csv(claim_file_path)
    try:
        search_terms_spotlight = dbp(search_terms)
        vectorized_spotlight = TfidfVectorizer(analyzer="word",
                                               tokenizer=split_tokenizer,
                                               ngram_range=(1,3),
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

@app.get('/api/v1/Vectorizer/CountVectorizer/{top_k}/{search_terms}')
#API for return N selected claims for a string (that is provided by the fact checkers) using CountVectorizer
async def CountVectorizer_with_DBpedia_spotlight(top_k: int,search_terms):
    min_df = 32
    claim_file_path = 'Dataset/cord19_ClaimKG_With_Conceptnet_Entities_For_DbpediaSpotlight.csv'
    claim_df = pd.read_csv(claim_file_path)
    try:
        search_terms_spotlight = dbp(search_terms)
        vectorized_spotlight = CountVectorizer(analyzer="word",
                                               tokenizer=split_tokenizer,
                                               ngram_range=(1,3),
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

@app.get("/api/v1/test_api")
def test_api():
    logger.info(
        "Hit test api. test api status OK")
    return {"ok"}
