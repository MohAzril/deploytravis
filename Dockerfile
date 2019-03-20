FROM python:3.6.7
MAINTAINER Your Name "azril@alphatech.id"
RUN mkdir -p /portofolio
COPY . /portofolio
RUN pip install -r /portofolio/requirements.txt
WORKDIR /portofolio
ENTRYPOINT ["python3"]
CMD ["app.py"]