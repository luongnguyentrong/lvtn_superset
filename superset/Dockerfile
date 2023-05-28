FROM apache/superset:2.1.0
USER root
WORKDIR /app
ENV SUPERSET_SECRET_KEY=0NjDl036arerLFCMVtL3asykJVhUI0TuePSirkruJA4Fw73EuDSaIBfn

RUN pip install psycopg2
RUN pip install sqlalchemy
RUN pip install flask_openid 
RUN pip install itsdangerous==2.0.1
RUN pip install flask_oidc==1.3.0

USER superset

COPY *.py ./pythonpath/

EXPOSE 8088