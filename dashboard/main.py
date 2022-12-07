
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI

import streamlit as st
import datetime
import pandas as pd
import numpy as np


def get_client():
    fiware = FiwareContext(
        service='ai4sdw',
        service_path='/'
    )
    client = QuantumLeapClient(
        base_url=URI("http://quantumleap:8668/"),
        ctx=fiware
    )

    return client

def get_entitis_id(client):
    try:
        entities = client.list_entities(entity_type='ai4sdw_service')
        w_ids = [e.id for e in entities]
        return w_ids
    except:
        return False

def get_data(client, e_id, d1=None, d2=None):
    try:
        r = client.entity_series(
            entity_id=e_id, entity_type='ai4sdw_service',from_timepoint=d1, to_timepoint=d2
        )
        return r.dict()
    except:
        return False

def main():
    st.title("AI4SDW")
    client = get_client()
    st.header("Select a worker to view statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        entities = get_entitis_id(client)
        if entities:
            entity_id = st.selectbox("Select a worker", entities)
        else:
            entity_id = st.selectbox("Select a worker", "")
            st.write("connection problem")
        date1 = st.date_input("From", datetime.datetime.now())
        date2 = st.date_input("To", datetime.datetime.now())

    with col2:
        if entities:
            res = get_data(client, entity_id, date1, date2)
            if res:
                st.write(res)



if __name__ == '__main__':
    main()