import requests
import csv
from bs4 import BeautifulSoup


def get_brand_URL():
    result = requests.get("http://www.alba.co.kr/")
    alba_soup = BeautifulSoup(result.text, "html.parser")
    super_brand_box = alba_soup.find("div", {"id": "MainSuperBrand"})
    super_brand_list = super_brand_box.find_all(
        "li", {"class": "impact"})
    URL_list = []
    for super_brand in super_brand_list:
        URL = super_brand.find_all("a", {"class": "brandHover"})
        for a_tag in URL:
            super_brand_URL = a_tag["href"]
            URL_list.append(super_brand_URL)
    return URL_list


def extract_job(html):
    try:
        place = html.find("td", {"class": "local"}).get_text(strip=True)
        title = html.find("td", {"class": "title"}).find(
            "span", {"class": "company"}).get_text(strip=True)
        time = html.find("td", {"class": "data"}).find(
            "span", {"class": "time"}).get_text(strip=True)
        pay_unit = html.find("td", {"class": "pay"}).find(
            "span", {"class": "payIcon"}).get_text(strip=True)
        pay_number = html.find("td", {"class": "pay"}).find(
            "span", {"class": "number"}).get_text(strip=True)
        pay = pay_unit + pay_number
        if html.find("td", {"class": "regDate"}).find(
                "strong") == None:
            date = html.find("td", {"class": "regDate"}).get_text(strip=True)
        else:
            date = html.find("td", {"class": "regDate"}).find(
                "strong").get_text(strip=True)

        return {
            'place': place,
            'title': title,
            'time': time,
            'pay': pay,
            'date': date,

        }
    except:
        pass


def save_to_file(jobs, company):
    file = open(f"jobs/{company}.csv", mode="w", encoding="utf-8", newline='')
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return


def extract_jobs():
    jobs = []
    URL_list = get_brand_URL()
    for i, page in enumerate(URL_list):
        left_pages = 120-int(i)
        print(f"scraping alba: {i} page. {left_pages} pages left")
        result = requests.get(page)
        soup = BeautifulSoup(result.text, "html.parser")

        job_table = soup.find_all("table", {"cellspacing": "0"})

        for tr in job_table:
            if tr.get('cellpadding') == None:
                pass
            else:
                if tr["cellpadding"] == ["0"]:
                    job_table.remove(tr)

        table_body = job_table[0].find("tbody")
        if table_body == None:
            pass
        else:
            table_row = table_body.find_all("tr")
            for tr in table_row:
                if tr.get('class') == None:
                    continue
                else:
                    if tr["class"] == ["summaryView"]:
                        table_row.remove(tr)
            for info in table_row:
                job = extract_job(info)

                if job != None:

                    jobs.append(job)

                else:
                    pass
        company = soup.find("title").string[0:-20]
        save_to_file(jobs, company)
        jobs = []
    return jobs


extract_jobs()
