from fastapi import FastAPI
import uvicorn

from dazzler import __version__
from dazzler.config import dazzler_config
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI

app = FastAPI()
DashboardSubApp(app, __name__).mount_dashboards(dazzler_config())



@app.get('/')
def read_root():
    return {'dazzler': __version__}

@app.get("/a")
async def a():
    return "a-async"

@app.get("/b")
def b():
    return "b-not_async"

@app.get("/prova")
async def prova():
    print("init prova")

    client = QuantumLeapClient(
    base_url = URI("http://quantumleap:8668/"),
    ctx = FiwareContext(
        service='ai4sdw',
        service_path='/'
    )
    )

    print("after client")

    entities = client.list_entities(entity_type='RoughnessEstimate')
    print(f"entities: {entities}")

    print("after entities")

    out = []
    for id in entities:
        r = client.entity_series(
        entity_id = id.id, entity_type = 'RoughnessEstimate',
        )

        out.append(r.dict())

    return out

@app.get("/version")
def read_version():
    return read_root()


if __name__ == '__main__':
    uvicorn.run(app)
