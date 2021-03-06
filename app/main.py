import json
import logging.config
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from util import Model, get_model

app = FastAPI()

# Load logger config
# with open('logger.yaml', 'r') as f:
#     config = yaml.safe_load(
#         f.read())
#     logging.config.dictConfig(
#         config)

# Create a custom logger
logger = logging.getLogger(__name__)


class RecommendationRequest(BaseModel):
    top_k: int
    search_terms: str


class RecommendationStore(BaseModel):
    threshold: float
    search_terms: str


class EmbeddingModel(BaseModel):
    parameter: bool


class ConceptNetEntityExtraction(BaseModel):
    parameter: bool


## Need to work on it
class RecommendationResponse(BaseModel):
    text: str
    research_paper: str
    author_name: str
    similarity_score: float


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


@app.get("/api/v1/Transformers/embeddings_ROBERTA/{parameter}", response_model=EmbeddingModel)
# Claim embeddings using ROBERTA large transformer
async def corpus_embeddings_ROBERTA(request: EmbeddingModel, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.parameter)
    json_compatible_item_data = model.corpus_embeddings_ROBERTA_large(response)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/v1/Transformers/embeddings_BERT/{parameter}", response_model=EmbeddingModel)
# Claim embeddings using BERT transformer
async def corpus_embeddings_Transformers_BERT(request: EmbeddingModel, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.parameter)
    json_compatible_item_data = model.corpus_embeddings_BERT(response)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/api/v1/Transformers/ROBERTA/{top_k}/{search_terms}", response_model=RecommendationResponse)
async def claim_for_ROBERTA(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.transformers_claim_for_ROBERTA_large(request.top_k, response)
    # print(json_compatible_item_data)
    return JSONResponse(content=json.dumps(json_compatible_item_data[0]))


@app.post("/api/v1/Transformers/ROBERTA/store_claim/{threshold}/{search_terms}", response_model=RecommendationResponse)
async def store_claim_for_ROBERTA(request: RecommendationStore, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.store_transformers_claim_for_ROBERTA_large(request.threshold, response)
    return JSONResponse(content="Similarity store in a csv file and store in the dump folder")


@app.post("/api/v1/Transformers/BERT/{top_k}/{search_terms}", response_model=RecommendationResponse)
async def calim_for_Transformers_BERT(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.transformers_claim_for_BERT(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/api/v1/Transformers/BERT/store_claim/{threshold}/{search_terms}", response_model=RecommendationResponse)
async def store_claim_for_BERT(request: RecommendationStore, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.store_transformers_claim_for_BERT(request.threshold, response)
    return JSONResponse(content="Similarity store in a csv file and store in the dump folder")


@app.post('/api/v1/Vectorized/Tfidf_DBPedia/{top_k}/{search_terms}', response_model=RecommendationResponse)
# API for return N selected claims for a string (that is provided by the fact-checkers) using TfidfVectorizer
async def Tfidf_with_DBpedia_spotlight(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.TfidfVectorizer_with_DBpedia_spotlight(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/api/v1/Vectorized/Count_DBPedia/{top_k}/{search_terms}')
# API for return N selected claims for a string (that is provided by the fact checkers) using CountVectorizer
async def Count_with_DBpedia_spotlight(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.CountVectorizer_with_DBpedia_spotlight(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


# @app.post('/api/v1/Extract_conceptnet_entities/{parameter}', response_model=EmbeddingModel)
# async def Extract_conceptnet_entities_with_DBpedia_spotlight(request: EmbeddingModel, model: Model = Depends(get_model)):
#     response = jsonable_encoder(request.parameter)
#     print(response)
#     json_compatible_item_data = model.Extract_conceptnet_entities_with_DBpedia_spotlight(response)
#     return JSONResponse(content=json_compatible_item_data)


# from models.Entity_extraction.dbpedia_spotlight_entities import dbp
# import pandas as pd


@app.post('/api/v1/Vectorized/Tfidf_conceptnet/{top_k}/{search_terms}', response_model=RecommendationResponse)
async def Tfidf_with_ConceptNet(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.TfidfVectorizer_with_conceptnet_entities(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/api/v1/Vectorized/Count_conceptnet/{top_k}/{search_terms}', response_model=RecommendationResponse)
async def Count_with_ConceptNet(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.CountVectorizer_with_conceptnet_entities(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


# How many claims are found, on average, for certain similarity thresholds


@app.get("/api/v1/test_api")
def test_api():
    logger.info(
        "Hit test api. test api status OK")
    return {"ok"}
