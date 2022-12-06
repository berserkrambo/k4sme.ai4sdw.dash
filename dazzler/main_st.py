
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI
import urllib.request
from urllib.error import HTTPError

import streamlit as st
import pandas as pd
import numpy as np

fiware = FiwareContext(
        service='ai4sdw',
        service_path='/'
    )
st.title("AI4SDW")


# non funziona.....
# try:
#     urllib.request.urlopen("http://quantumleap:8668/")
# except HTTPError as httperr:
#     print(httperr)



client = QuantumLeapClient(
    base_url=URI("http://quantumleap:8668/"),
    ctx=fiware
)

entities = client.list_entities(entity_type='ai4sdw_service')
w_ids = [e.id for e in entities]

st.header("Select a worker to view statistics")
choice = st.selectbox("Select a worker", w_ids)

r = client.entity_series(
        entity_id = choice, entity_type = 'ai4sdw_service',
        )

st.write(r.dict())







