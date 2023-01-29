from bs4 import BeautifulSoup
import requests
import datetime

from fastapi import FastAPI

AZURE_URL = "https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli"
GOOGLE_URL = "https://cloud.google.com/kubernetes-engine/docs/release-schedule"
AMAZON_URL = "https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html"


def aks():
    r = requests.get(AZURE_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find(".has-inner-focus")

    table = soup.find("table")
    # span = soup.find("span")
    # aria_label = span["aria-label"]
    # table = span.get("Table 2", "")

    print(table)
    # table_body = table.find("tbody")
    # rows = table_body.find_all("tr")

    # print(rows)


def eks():
    res = []
    r = requests.get(AMAZON_URL)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", attrs={"id": "w284aac15c41c21"})

    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if cols:

            # release_date = datetime.datetime.strptime(cols[1], "%B %d, %Y").strftime(
            #     "%Y-%m-%d"
            # )
            # eol = datetime.datetime.strptime(cols[3], "%B %d, %Y").strftime("%Y-%m-%d")
            o = {"version": cols[0], "release_date": cols[1], "eol": cols[3]}
            res.append(o)

    return {"aws": res}


def gke() -> list[dict]:
    res = []
    r = requests.get(GOOGLE_URL)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", attrs={"class": "vertical-rules"})
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        version = "{:.4}".format(cols[0])
        o = {"version": version, "release_date": cols[1], "eol": cols[-1]}
        res.append(o)

    return {"gcloud": res}


app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"ok": "true"}


@app.get("/")
def root():
    res = {}
    res.update(eks())
    res.update(gke())
    return res
