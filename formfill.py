from selenium import webdriver
import base64
from selenium.webdriver.common.by import By
import time
import tesseractexp
import xlsxwriter

#for saving data.
names = []
dates = []


def downloadImage(captchImage):
    # get the captcha as a base64 string
    img_captcha_base64 = web.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, captchImage)

    # save the captcha to a file
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))

#automating form registration
def register(dd, mm):
    name = web.find_element(By.XPATH, '//*[@id="txtDec"]')
    date = web.find_element(By.XPATH, '//*[@id="txtday"]')
    month = web.find_element(By.XPATH, '//*[@id="txtMonth"]')
    year1977 = web.find_element(By.XPATH, '//*[@id="CboYear"]/option[37]')
    year1978 = web.find_element(By.XPATH, '//*[@id="CboYear"]/option[38]')
    year1979 = web.find_element(By.XPATH, '//*[@id="CboYear"]/option[39]')

    captchImage = web.find_element(
        By.XPATH, '//*[@id="DeathRegistration"]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[2]/img')

    downloadImage(captchImage)

    captchInput = web.find_element(By.XPATH, '//*[@id="security_code"]')
    name.clear()
    name.send_keys('Thankappan')
    date.clear()
    date.send_keys(dd)
    month.clear()
    month.send_keys(mm)
    year1979.click()

    # time.sleep(1)

    captchText = tesseractexp.imageText()

    # time.sleep(1)
    captchInput.clear()
    captchInput.send_keys(captchText)
    # time.sleep(1)
    SearchButton = web.find_element(By.XPATH, '//*[@id="btnSearch"]')
    SearchButton.click()
    time.sleep(2)

    try:
        error = web.find_element(By.XPATH, '//*[@id="security_cod"]/font')
        print("error in captcha")
        register(dd, mm)
    except:
        try:
            print("no error in captcha")
            nameDetails = web.find_element(
                By.XPATH, '//*[@id="Tborder"]/table/tbody/tr[2]/td[1]').text
            dateDetails = web.find_element(
                By.XPATH, '//*[@id="Tborder"]/table/tbody/tr[2]/td[2]').text
            names.append(nameDetails)
            dates.append(dateDetails)
            web.back()
            time.sleep(2)
            return
        except:
            print("no data to get")
            web.back()
            time.sleep(2)
            return

# for chrome 
web = webdriver.Chrome()

web.get("https://cr.lsgkerala.gov.in/regsearch.php")

time.sleep(1)


District = web.find_element(By.XPATH, value='//*[@id="cboDist"]/option[1]')
LocalBodyType = web.find_element(
    By.XPATH, value='//*[@id="cboLBType"]/option[2]')
SubmitButton = web.find_element(
    By.XPATH, '//*[@id="SevanaIndex"]/table/tbody/tr/td/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[7]/td/input')


District.click()
time.sleep(2)
LocalBodyType.click()
time.sleep(2)
SubmitButton.click()

time.sleep(1)

deathRegistionForm = web.find_element(
    By.XPATH, '//*[@id="DataStatus"]/table/tbody/tr[3]/td[2]/a')
deathRegistionForm.click()

time.sleep(1)


for i in range(1, 2):
    for j in range(1, 32):
        register(j, i)
time.sleep(1)

#print accquired data in console.
print(names)


# writing data to execl file

outWork = xlsxwriter.Workbook("newdata.xlsx")
outsheet = outWork.add_worksheet()

outsheet.write("A1", "Names")
outsheet.write("B1", "Dates")

for item in range(len(names)):
    outsheet.write(item+1, 0, names[item])
    outsheet.write(item+1, 1, dates[item])

outWork.close()
