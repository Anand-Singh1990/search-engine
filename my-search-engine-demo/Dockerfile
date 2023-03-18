FROM python:3.11
EXPOSE 8080

COPY . .
RUN pip install -r requirements.txt

RUN mkdir -p ~/.streamlit
RUN cp .streamlit/config.prod.toml ~/.streamlit/config.toml
RUN cp .streamlit/credentials.prod.toml ~/.streamlit/credentials.toml

#Store env variable in container
ARG BUILDTIME_ACS_ENDPOINT
ENV ACS_ENDPOINT="https://vedic-search.search.windows.net/"

ARG BUILDTIME_ACS_API_KEY
ENV ACS_API_KEY="j4aOJ9YtD3KIQnh5xY9F4ohFBltJ7TcPXYZ3gBnRAfAzSeC40KqJ"

ARG BUILDTIME_SA_CONN_STR
ENV SA_CONN_STR="DefaultEndpointsProtocol=https;AccountName=vedicdata;AccountKey=yoSqGy2wvdzvBjmwRNJq7kzZJfHdnDcQOrlskj0noyvArIV61Ov4TsKkVHLdvf/10pD3IAjcdfs6+ASt/DytJQ==;"

CMD streamlit run ./my-search-engine-demo/user_interface.py 

