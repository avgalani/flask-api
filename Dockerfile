FROM python:3.6.6-jessie
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y clang
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["manage.py"]
