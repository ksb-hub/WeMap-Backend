from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def lambda_handler(event, context):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/python/bin/chromedriver')
    URL = "https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679"
    data_dict = {}

    try:
        driver.get(URL)
        # 페이지의 첫 번째 요소가 로드될 때까지 최대 10초간 대기합니다.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "disasterSms_tr_0_apiData1"))
        )

        disaster_type = driver.find_element(By.ID, f"disasterSms_tr_0_DSSTR_SE_NM").text
        emergency_step = driver.find_element(By.ID, f"disasterSms_tr_0_EMRGNCY_STEP_NM").text

        data_dict = {
            "disaster_type": disaster_type,
            "emergency_step": emergency_step,
        }

    except WebDriverException as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Selenium Error: {str(e)}")
        }
    finally:
        driver.quit()

    return {
        'statusCode': 200,
        'body': data_dict
    }
