FROM ducluongvn/superset_extended
USER root
WORKDIR /app

ENV DATABASE_DIALECT=postgres
ENV DATABASE_USER=superset_user_pdt
ENV DATABASE_PASSWORD=v51Qrgcb4fFSRB8mC4ENDOLSk40T1dBI
ENV DATABASE_HOST=159.223.66.111
ENV DATABASE_PORT=5432
ENV DATABASE_DB=superset_pdt

USER superset

COPY client_secret.json ./pythonpath/

RUN superset db upgrade
RUN superset init

EXPOSE 8088
    