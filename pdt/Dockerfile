FROM ducluongvn/superset_extended
USER root
WORKDIR /app

ENV DATABASE_DIALECT=postgres
ENV DATABASE_USER=superset_user_pdt
ENV DATABASE_PASSWORD=XIgq5HtV6HRPzWHBQcnSbQEhwCpUS0CT
ENV DATABASE_HOST=159.223.66.111
ENV DATABASE_PORT=5432
ENV DATABASE_DB=superset_pdt

USER superset

COPY client_secret.json ./pythonpath/

RUN superset db upgrade

EXPOSE 8088
    