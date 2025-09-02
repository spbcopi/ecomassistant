import csv
import time
import re
import os
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class WebDataScraper:
    def __init__(self, output_directory="data"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def retrieve_top_reviews(self,product_url,count=3):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = uc.Chrome(options=options, use_subprocess=True)

        if not product_url.startswith("http"):
            return "!!! No reviews found !!!"
        
        try:
            driver.get(product_url)
            time.sleep(5)

            try:
                driver.find_element(By.XPATH, "//button[contains(text(), '✕')]").click()
                time.sleep(2)
            except Exception as e:
                print(f"Popup close error: {e}")   
            
            for _ in range(4):
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(1.5)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            review_blocks = soup.select("div._27M-vq, div.col.EPCmJX, div._6K-7Co")
            seen = set()
            reviews = []

            for block in review_blocks:
                text = block.get_text(separator=" ", strip=True)
                if text and text not in seen:
                    reviews.append(text)
                    seen.add(text)
                if len(reviews) >= count:
                    break
        except Exception as e:
            reviews = []

        driver.quit()
        return " || ".join(reviews) if reviews else "!!! No reviews found !!!"