from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

class Jobstreet():
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(4)

    def get_page(self, page_number):
        select_page = Select(self.driver.find_element(By.ID,'pagination'))
        select_page.select_by_visible_text(str(page_number))

    def search_op(self, searched_job):
        search_box = self.driver.find_element(By.NAME, 'key')
        self.driver.implicitly_wait(5)
        search_box.send_keys(searched_job)
        self.driver.implicitly_wait(5)
        search_box.submit()
        self.driver.implicitly_wait(5)

    def job_scraping(self):
        jobs = self.driver.find_elements(By.CSS_SELECTOR,'.z1s6m00._1hbhsw67i._1hbhsw66e._1hbhsw69q._1hbhsw68m._1hbhsw6n._1hbhsw65a._1hbhsw6ga._1hbhsw6fy')

        for job in jobs:
            job_name = job.find_element(By.CSS_SELECTOR,'.z1s6m00._1hbhsw64y.y44q7i0.y44q7i3.y44q7i21.y44q7ii').text
            company = job.find_element(By.CSS_SELECTOR, '.z1s6m00._1hbhsw64y.y44q7i0.y44q7i1.y44q7i21.y44q7ih').text
            location = job.find_element(By.CSS_SELECTOR,'.z1s6m00._1hbhsw64y.y44q7i0.y44q7i3.y44q7i21.y44q7ih').text
            published_date = job.find_element(By.CSS_SELECTOR,'.z1s6m00._1hbhsw64y.y44q7i0.y44q7i1.y44q7i22.y44q7ih').text

            raw_data = {'Job Name': [job_name],
                        'Company Name': [company],
                        'Location': [location],
                        'Published Date': [published_date]}

            # raw_data = (job_name, company, location, published_date)
            self.write_csv(raw_data)

    def write_csv(self, raw_data):
        df = pd.DataFrame(raw_data)
        df.to_csv('jobstreet.csv',mode='a',index=False, header=False)

    def execution(self):
        searched_job = input('Job that you want to search: ')
        self.search_op(searched_job)
        page_range = int(input('Number of pages that you want to scrape: '))
        for i in range(1,page_range+1):
            self.get_page(i)
            self.job_scraping()

if __name__ == "__main__":
    jobstreet = Jobstreet('https://www.jobstreet.com.sg/?icmpid=js_global_landing_page')
    jobstreet.execution()
