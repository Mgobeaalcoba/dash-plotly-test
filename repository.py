# BigQuery
import base64

from google.oauth2 import service_account

from google.cloud import bigquery
from google.cloud import bigquery_storage

import json

import pandas as pd

class Repository:
    def __init__(self):
        self.project_id = 'meli-bi-data'
        self.scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/bigquery']
        self.credentials = service_account.Credentials.from_service_account_info(json.loads(self.get_credentials_bq()), scopes=self.scopes)
        self.client = bigquery.Client(self.project_id, self.credentials)
        self.bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=self.credentials)

    def get_credentials_bq(self) -> str:
        # Leo el archivo secret.txt para obtener las credenciales de bigquery
        with open('secret.json', 'r') as file: # TODO: Usar get_secret() en producción
            credentials_bq = file.read()
        return credentials_bq

    def get_data(self, query: str) -> pd.DataFrame:
        df = self.client.query(query).result().to_dataframe(bqstorage_client=self.bqstorageclient)
        return df

