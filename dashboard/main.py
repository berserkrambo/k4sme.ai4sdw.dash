from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI


import streamlit as st
import datetime
import pandas as pd


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
        return None

def get_data(client, e_id, d1, d2, t_aggr):
    try:
        r = client.entity_series(
            entity_id=e_id, entity_type='ai4sdw_service',from_timepoint=d1, to_timepoint=d2 + datetime.timedelta(days=1)
        )
    except:
        return None
    else:
        data = r.dict()

        t_aggr = str(t_aggr).upper().replace("M", "T")
        data = pd.DataFrame(data)
        group = data.resample(t_aggr, on='index').mean().fillna(0)

        fa = pd.DataFrame(group["fall_pred"])
        fa["Warning Level"] = [1 for i in range(len(fa["fall_pred"]))]

        ac = pd.DataFrame(group["area_crossed"])
        ac["Warning Level"] = [1 for i in range(len(ac["area_crossed"]))]

        wd = pd.DataFrame(group["risk_level"])
        wd["Warning Level"] = [80 for i in range(len(wd["risk_level"]))]

        return fa, ac, wd

def main():
    st.title("AI4SDW")
    client = get_client()
    st.header("Select a worker to view statistics")

    entities = get_entitis_id(client)
    if entities is not None:
        entity_id = st.selectbox("Select a worker", entities)
    else:
        entity_id = st.selectbox("Select a worker", "")
        st.write("connection problem")

    date1 = st.date_input("From", datetime.datetime.now())
    date2 = st.date_input("To", datetime.datetime.now())

    t_aggr = st.select_slider(
        'Temporal aggregation',
        options=['30s', '1m', '5m', '15m', '30m', '1h', '2h', '8h', '12h', '24h'])

    if entities is not None:
        res = get_data(client, entity_id, date1, date2, t_aggr)
        if res is not None:
            # import pickle
            # resd = pickle.dumps(res)
            # st.download_button("Download file", resd)

            fa, ac, wd = res
            st.subheader("Falls occurred")
            st.line_chart(fa)
            st.subheader("Denied area crossed")
            st.line_chart(ac)
            st.subheader("Distance level warning")
            st.line_chart(wd)

        else:
            st.header("No data available")



# if __name__ == '__main__':
    # import pickle
    # with open("/home/rgasparini/Desktop/Main_2022-12-10_10-47-58.bin", "rb") as f:
    #     data = pickle.load(f)
    # data = pd.DataFrame(data)
    # group = data.resample('15S', on='index').mean().fillna(0)
    # fa = pd.DataFrame(group["fall_pred"])
    # fa["Warning Level"] = [1 for i in range(len(fa["fall_pred"]))]
    #
    # a=0

    # main()