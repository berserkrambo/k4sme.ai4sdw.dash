
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI


import streamlit as st
import pandas as pd
import numpy as np

fiware = FiwareContext(
        service='ai4sdw',
        service_path='/'
    )
st.title("AI4SDW")

try:
    client = QuantumLeapClient(
        base_url=URI("http://quantumleap:8668/"),
        ctx=fiware
    )
    entities = client.list_entities(entity_type='ai4sdw_service')
    w_ids = [e.id for e in entities]

    st.header("Select a worker to view statistics")
    choice = st.selectbox("Select a worker", w_ids)

    r = client.entity_series(
        entity_id=choice, entity_type='ai4sdw_service',
    )

    st.write(r.dict())

except:
    st.write("connection problem")






