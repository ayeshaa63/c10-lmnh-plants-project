FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt

COPY extract.py ${LAMBDA_TASK_ROOT}

COPY transform.py ${LAMBDA_TASK_ROOT}
COPY email_alert.py ${LAMBDA_TASK_ROOT}

COPY load.py ${LAMBDA_TASK_ROOT}
COPY insert_missing_metadata.py ${LAMBDA_TASK_ROOT}

CMD ["load.handler"]