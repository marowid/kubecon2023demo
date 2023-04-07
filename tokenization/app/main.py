import logging
import os
import uuid
from typing import Union

import boto3
import pandas as pd
from fastapi import FastAPI

from app.models import ClinicalDataBreastCancer
from app.tokenization import Tokenizer


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

STORAGE_KEY = os.getenv("TOKENIZER_STORAGE_KEY") or "minio123"
STORAGE_SECRET = os.getenv("TOKENIZER_STORAGE_SECRET") or "minio123"
STORAGE_URL = os.getenv("TOKENIZER_STORAGE_URL") or "http://10.152.183.193:9000"

TOKENS_BUCKET = "tokens"
DATA_BUCKET = "data"
DATA_PAM50_PREFIX = "pam50"
DATA_BREAST_CANCER_PREFIX = "breast_cancer"
DATA_CANCER_PROTEOMES_PREFIX = "cancer_proteomes"

TOKEN = (
    os.getenv("TOKENIZER_TOKEN_VALUE")
    or "5aLNDuGa0HlpRhINCmWRInIgjjG6xuatcEaI6GufjnwzxUMYVbptvtFwK0RpPKGKOQFXksso2jL+Pv4ozFUm+2dpeYIjxzN0785lM5loKHJsU+/FCj6cDoqINWnotK3oBQ5E20kgcBVgOu5MY/wx8P2Yv2Afln6rjRZaj/o9Xt3qMKmbMP0ExQaHLcEMfJlqzOyxwzKPTgEj3peWwLJPO2K6RS+htEMwjvbUvROTyWYTjwXy44eqdfYmYJDI3HP2czhz53XotxS5Zw2+PZlmNiwSttdl0EE0Eu4qpeOz5W+I6vQUFocnGhhZ8vSdbvMg3IgMbmGfpnfFnlwwDQHK295Qnwyuq1gd9XqrIha9BvgdU1lmVS1hHt5PUtAXQe45FOwhL8YqZG+Q2zIyMhycKxmDzUkST7/+loppTO0ZwjRz1gzKVb"
)
TOKEN_ID = os.getenv("TOKENIZER_TOKEN_ID") or "c640aad2-d87e-4eea-b523-4fea8fd04718"

tokenizer = Tokenizer(TOKEN)

# Save token if not saved
s3 = boto3.client(
    "s3",
    aws_access_key_id=STORAGE_KEY,
    aws_secret_access_key=STORAGE_SECRET,
    endpoint_url=STORAGE_URL,
)

token_objects = s3.list_objects_v2(Bucket=TOKENS_BUCKET)
if token_objects.get("KeyCount") > 0:
    token_files = [f.get("Key") for f in token_objects.get("Contents")]
    if TOKEN_ID not in token_files:
        s3.put_object(Body=TOKEN, Bucket=TOKENS_BUCKET, Key=TOKEN_ID)
        logger.info(f"Created a token file for id:{TOKEN_ID}")
    else:
        logger.info(f"Token key found for id: {TOKEN_ID}")
else:
    s3.put_object(Body=TOKEN, Bucket=TOKENS_BUCKET, Key=TOKEN_ID)
    logger.info(f"Created a token file for id:{TOKEN_ID}")

# initial data processing / upload
s3.upload_file(
    "./app/data/PAM50_proteins_with_columns.csv",
    Bucket=DATA_BUCKET,
    Key=f"{DATA_PAM50_PREFIX}/PAM50_proteins_with_columns.csv",
)
logger.info("Uploaded file: PAM50_proteins_with_columns.csv")
df_breast_cancer = pd.read_csv(
    "./app/data/clinical_data_breast_cancer_with_columns.csv"
)
df_breast_cancer["first_name"] = tokenizer.mask_series(df_breast_cancer["first_name"])
df_breast_cancer["last_name"] = tokenizer.mask_series(df_breast_cancer["first_name"])
df_breast_cancer.to_csv(
    f"s3://{DATA_BUCKET}/{DATA_BREAST_CANCER_PREFIX}/clinical_data_breast_cancer_with_columns.csv",
    index=False,
    storage_options={
        "key": STORAGE_KEY,
        "secret": STORAGE_SECRET,
        "client_kwargs": {"endpoint_url": STORAGE_URL},
    },
)
logger.info("Uploaded tokenized file: clinical_data_breast_cancer_with_columns.csv")
s3.upload_file(
    "./app/data/77_cancer_proteomes_CPTAC_itraq_with_columns.csv",
    Bucket=DATA_BUCKET,
    Key=f"{DATA_CANCER_PROTEOMES_PREFIX}/77_cancer_proteomes_CPTAC_itraq_with_columns.csv",
)
logger.info("Uploaded file: 77_cancer_proteomes_CPTAC_itraq_with_columns.csv")

# API
app = FastAPI()


@app.get("/files/{dataset}")
def list_files(dataset: str, q: Union[str, None] = None):
    response = s3.list_objects_v2(Bucket=DATA_BUCKET, Prefix=dataset)
    return response.get("Contents")


@app.post("/files/breast_cancer")
def insert_clinical_data(item: ClinicalDataBreastCancer):
    masked = item.dict()
    masked["first_name"] = tokenizer.mask_value(masked["first_name"])
    masked["last_name"] = tokenizer.mask_value(masked["last_name"])
    masked_data = ClinicalDataBreastCancer(**masked)

    file_key = str(uuid.uuid4())
    s3.put_object(
        Body=masked_data.json(),
        Bucket=DATA_BUCKET,
        Key=f"{DATA_BREAST_CANCER_PREFIX}/{file_key}.json",
    )
    logger.info("New Breast Cancer record added.")
    return masked_data
