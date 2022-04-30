import logging.config
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Transformers ROBERTA-large
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('stsb-roberta-large')
# Transformers BERT
model_bert = SentenceTransformer('bert-base-nli-mean-tokens')

from util import transformers_claim_for_ROBERTA_large, transformers_claim_for_BERT, \
    TfidfVectorizer_with_DBpedia_spotlight, \
    CountVectorizer_with_DBpedia_spotlight, corpus_embeddings_ROBERTA_large, corpus_embeddings_BERT

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
async def corpus_embeddings_ROBERTA(parameter):
    response = jsonable_encoder(parameter)
    json_compatible_item_data = corpus_embeddings_ROBERTA_large(response)
    return JSONResponse(content=json_compatible_item_data)


@app.get('/api/v1/Transformers/embeddings_BERT/{parameter}')
# Claim embeddings using BERT transformer
async def corpus_embeddings_Transformers_BERT(parameter):
    response = jsonable_encoder(parameter)
    json_compatible_item_data = corpus_embeddings_BERT(response)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/v1/Transformers/ROBERTA/{top_k}/{search_terms}")
async def claim_for_ROBERTA_large(top_k: int, search_terms):
    response = jsonable_encoder(search_terms)
    json_compatible_item_data = transformers_claim_for_ROBERTA_large(top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/v1/Transformers/BERT/{top_k}/{search_terms}")
async def calim_for_Transformers_BERT(top_k: int, search_terms):
    response = jsonable_encoder(search_terms)
    json_compatible_item_data = transformers_claim_for_BERT(top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.get('/api/v1/Vectorized/Tfidf/{top_k}/{search_terms}')
# API for return N selected claims for a string (that is provided by the fact checkers) using TfidfVectorizer
async def Tfidf_with_DBpedia_spotlight(top_k: int, search_terms):
    response = jsonable_encoder(search_terms)
    json_compatible_item_data = TfidfVectorizer_with_DBpedia_spotlight(top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.get('/api/v1/Vectorized/Count/{top_k}/{search_terms}')
# API for return N selected claims for a string (that is provided by the fact checkers) using CountVectorizer
async def Count_with_DBpedia_spotlight(top_k: int, search_terms):
    response = jsonable_encoder(search_terms)
    json_compatible_item_data = CountVectorizer_with_DBpedia_spotlight(top_k, response)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/v1/test_api")
def test_api():
    logger.info(
        "Hit test api. test api status OK")
    return {"ok"}
