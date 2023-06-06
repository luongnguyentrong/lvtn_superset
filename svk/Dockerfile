FROM ducluongvn/superset_extended
USER root
WORKDIR /app

ENV DATABASE_DIALECT=postgres
ENV DATABASE_USER=superset_user_svk
ENV DATABASE_PASSWORD=MSt7GxVc6Wpye9vVPPj48n0yoDXzFJjM
ENV DATABASE_HOST=159.223.66.111
ENV DATABASE_PORT=5432
ENV DATABASE_DB=superset_svk

USER superset

COPY client_secret.json ./pythonpath/

EXPOSE 8088
    