import time
import glob
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# TODO: documentation 
# TODO: alter timing parameters 
# TODO: error handling

_logger = logging.getLogger(__name__)
USERNAME = 'innocent.mpasi@inonit.no'
PASSWORD = 'innocent.mpasi@inonit.no'
URL = 'https://www.odoo.sh/project/vad2/branches/stage/backups'
chrome_options = Options()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1480')


def download_file():
    try:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(URL)
        login = driver.find_element(By.ID, "login_field")
        password = driver.find_element(By.ID, "password")
        commit = driver.find_element(By.NAME, "commit")

        login.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        commit.click()
        time.sleep(10)
        if driver.title == 'Sign in to GitHub · GitHub':
            _logger.info("------- Sign in to GitHub · GitHub --------")
            return {"status": "failed", "payload": driver.title}

        elif driver.title == 'Odoo.sh - Branches':
            _logger.info(" --- logged in ----")
            notification_tab = driver.find_element(By.ID, "o_sh_notifications")
            notification_anchor = notification_tab.find_element(
                By.CLASS_NAME, "o_sh_no_caret")
            notification_anchor.click()
            time.sleep(2)
            info_tab = driver.find_element(
                By.CLASS_NAME, "o_sh_notify_item")
            download_btn = info_tab.find_element(By.CLASS_NAME, "btn-primary")
            if download_btn.text == 'Download':
                download_btn.click()
                _logger.info(download_btn.text)
            else:
                _logger.info(download_btn.text)
                return {"status": "failed", "payload": "Button not found"}

            file_list = []
            timeout = 0
            while not file_list:
                time.sleep(60)
                file_list = glob.glob('*.zip')
                timeout += 1
                _logger.info(f"{timeout} mins passed ")
                if timeout >= 30:
                    break
            filename = file_list[0]
            _logger.info(f"done dowwnlaoding {filename}")
            driver.close()
            return {"status": "success", "payload": filename}
        else:
            _logger.info(driver.title)
            return {"status": "failed", "payload": driver.title}

    except Exception as e:
        return {"status": "failed", "payload": str(e)}


def trigger_download():
    try:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(URL)
        login = driver.find_element(By.ID, "login_field")
        password = driver.find_element(By.ID, "password")
        commit = driver.find_element(By.NAME, "commit")

        login.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        # submit login form
        commit.click()
        time.sleep(10)
        # Check if the script is authenticated
        if driver.title == 'Sign in to GitHub · GitHub':
            _logger.info("------- Sign in to GitHub · GitHub --------")
            return {"status": "failed", "payload": driver.title}
        elif driver.title == 'Odoo.sh - Branches':
            _logger.info(" --- logged in ----")
            html = driver.find_element(By.CLASS_NAME, "col-lg-12")
            backup_list = html.find_elements(
                By.CLASS_NAME, "o_branch_backups_item")
            time.sleep(2)
            # get the latest backup on the list
            latest_backup = backup_list[1]
            o_make_backup = latest_backup.find_element(
                By.CLASS_NAME, "o_make_backup")
            o_make_backup.click()
            time.sleep(2)
            # get the download modal
            o_make_backup = latest_backup.find_element(
                By.CLASS_NAME, "o_make_backup")
            backup_modal = driver.find_element(
                By.CLASS_NAME, "o_legacy_dialog")
            test_dump_2 = backup_modal.find_element(By.ID, "test_dump_2")
            filestore_2 = backup_modal.find_element(By.ID, "filestore_2")
            # select exact dump
            test_dump_2.click()
            # select with filestore
            filestore_2.click()
            # start download
            start_button = backup_modal.find_element(
                By.CLASS_NAME, "btn-primary")
            start_button.click()
            _logger.info(" --- backup downloading ---")
            # close the browser
            driver.close()
            return {"status": "success", "payload": driver.title}
        else:
            _logger.info(driver.title)
            return {"status": "failed", "payload": driver.title}

    except Exception as e:
        return {"status": "failed", "payload": str(e)}
