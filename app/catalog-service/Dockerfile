FROM python
WORKDIR app
COPY . .
RUN pip install -r requirements.txt
ENV FLASK_APP=catalog-service
CMD ["flask","run","--port=8080","--host=0.0.0.0"]