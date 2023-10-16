FROM python

LABEL "project" = "api-testing-framework"

WORKDIR /api-testing-framework

VOLUME /allure-results

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python -m pytest -s -v tests/* --alluredir=allure-results/