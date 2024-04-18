FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY extract.py .

COPY transform.py .
COPY email_alert.py .

COPY load.py .
COPY insert_missing_metadata.py .

CMD ["load.handler"]