FROM python:3.9
ADD requirements.txt /requirements.txt
ADD okteto-stack.yaml /okteto-stack.yaml
RUN pip install -r requirements.txt
EXPOSE 8080
COPY ./app app
CMD ["cd", "app", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]