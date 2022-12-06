from fastapi import FastAPI
import uvicorn

from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.ngsi.headers import FiwareContext
from uri import URI

app = FastAPI()


@app.get('/')
def read_root():
    client = QuantumLeapClient(
    base_url = URI("http://quantumleap:8668/"),
    ctx = FiwareContext(
        service='ai4sdw',
        service_path='/'
    )
    )

    entities = client.list_entities(entity_type='ai4sdw_service')
    print(f"number of workers: {len(entities)}")

    out = []
    for id in entities:
        r = client.entity_series(
        entity_id = id.id, entity_type = 'ai4sdw_service',
        )

        out.append(r.dict())

    return out


if __name__ == '__main__':
    uvicorn.run(app)
