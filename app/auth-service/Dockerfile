FROM python
WORKDIR app
COPY . .
RUN echo "auth-server" && ls
RUN pip install -r requirements.txt

ENV FLASK_APP=auth-server
CMD ["flask","run","--port=8080","--host=0.0.0.0"]
