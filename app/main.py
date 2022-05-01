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


class EmbeddingModel(BaseModel):
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


@app.post("/api/v1/Transformers/BERT/{top_k}/{search_terms}", response_model=RecommendationResponse)
async def calim_for_Transformers_BERT(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.transformers_claim_for_BERT(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/api/v1/Vectorized/Tfidf/{top_k}/{search_terms}', response_model=RecommendationResponse)
# API for return N selected claims for a string (that is provided by the fact-checkers) using TfidfVectorizer
async def Tfidf_with_DBpedia_spotlight(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.TfidfVectorizer_with_DBpedia_spotlight(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/api/v1/Vectorized/Count/{top_k}/{search_terms}', response_model=RecommendationResponse)
# API for return N selected claims for a string (that is provided by the fact checkers) using CountVectorizer
async def Count_with_DBpedia_spotlight(request: RecommendationRequest, model: Model = Depends(get_model)):
    response = jsonable_encoder(request.search_terms)
    json_compatible_item_data = model.CountVectorizer_with_DBpedia_spotlight(request.top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/v1/test_api")
def test_api():
    logger.info(
        "Hit test api. test api status OK")
    return {"ok"}
