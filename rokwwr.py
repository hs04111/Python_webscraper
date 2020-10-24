import requests
from bs4 import BeautifulSoup


"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def extract_remoteok_jobs(KEYWORD):
    URL = f"https://remoteok.io/remote-dev+{KEYWORD}-jobs"
    result = requests.get(URL, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    jobsboard = soup.find("table", {"id": "jobsboard"})
    table_rows = jobsboard.find_all("tr", {"class": "remoteok-original"})
    print("Scrapping RemoteOK pages")
    for tr in table_rows:
        link_td = tr.find("td", {"class": "source"}).find("a")
        if link_td:
            link_end = link_td["href"]
            link = f"https://remoteok.io{link_end}"
            title = tr.find("td", {"class": "company_and_position"}).find(
                "h2", {"itemprop": "title"}).string
            company = tr.find("td", {"class": "company_and_position"}).find(
                "h3", {"itemprop": "name"}).string
            print("title = " + title, "company = " + company, "apply = " + link)
        else:
            pass


def find_jobs_wwr(row, i):
    apply_link = row.find_all("a")
    apply_link_end = apply_link[i]["href"]
    link = f"https://weworkremotely.com{apply_link_end}"
    company = row.find("span", {"class": "company"}).string
    title = row.find("span", {"class": "title"}).string
    print("title = " + title, "company = " + company, "apply = " + link)


def extract_wwr_job(html):
    job_rows = html.find_all("li", {"class": "feature"})

    for row in job_rows:
        company_link = row.find("div", {"class": "tooltip"})
        if company_link:
            find_jobs_wwr(row, 1)
        else:
            find_jobs_wwr(row, 0)


def extract_wwr_jobs(KEYWORD):
    URL = f"https://weworkremotely.com/remote-jobs/search?term={KEYWORD}"
    result = requests.get(URL, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    job_sections = soup.find_all("section", {"class": "jobs"})
    print("Scrapping WeWorkRemotely pages")
    for section in job_sections:
        extract_wwr_job(section)


def get_jobs(item):
    if False:  # fakeDB 조건 들어갈 것
        pass
    else:
        extract_wwr_jobs(item)
        extract_remoteok_jobs(item)


get_jobs("python")
