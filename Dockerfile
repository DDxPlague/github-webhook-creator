FROM python:3.6-alpine
RUN pip install PyGithub

COPY init.py /

ENTRYPOINT ["python", "init.py"]
