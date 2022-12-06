FROM python:3.9.12

RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY dazzler /app/dazzler

ENV PYTHONPATH=$PWD:$PYTHONPATH

# comment / uncomment this to use streamlit in our docker-compose conf
EXPOSE 8081
ENTRYPOINT ["streamlit", "run", "dazzler/main_st.py", "--server.address", "0.0.0.0", "--server.port", "8081"]

# comment / uncomment this to use streamlit in the kitt4sme cluster env
#EXPOSE 8000
#ENTRYPOINT ["uvicorn", "dazzler.main:app", "--host", "0.0.0.0", "--port", "8000"]