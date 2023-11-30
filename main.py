import requests
import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import io
from PIL import Image

TOKEN = '6711378771:AAEsihbqhSfjpz0D7Fx3KQCzjGcOxmhsX54'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler()
def info(message):
    CHAT_ID = message.chat.id
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}"

    def main(url):
        def get_images_urls():
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome()
            # Create url variable containing the webpage for a Google image search.
            # Launch the browser and open the given url in the webdriver.
            driver.get(url)
            # Scroll down the body of the web page and load the images.
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(5)

            # Access and store the scr list of image url's.
            kuki = driver.find_element(By.XPATH, "//button[@class='_a9-- _ap36 _a9_0']").click()
            time.sleep(2)
            nextButton = driver.find_element(By.XPATH, "//button[@class=' _afxw _al46 _al47']")

            count = 0
            imageCounts = driver.find_elements(By.XPATH, "//div[@class='_acnb']")
            for i in imageCounts:
                count += 1

            src = []
            index = 0
            while index < count:
                # Find the images.
                # imgResults = driver.find_elements(By.TAG_NAME, 'img')
                imgResults = driver.find_elements(By.XPATH,
                                                  "//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3']")
                for img in imgResults:
                    src.append(img.get_attribute('src'))
                index += 1
                nextButton.click()

            uniqueImages = []
            for source in src:
                if not (source in uniqueImages):
                    uniqueImages.append(source)

            return uniqueImages

        from telebot.types import InputMediaPhoto
        imgBytes = []
        imageUrls = get_images_urls()
        for img_url in imageUrls:
            img = Image.open(requests.get(img_url, stream = True).raw)
            # save image in memory
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            imgBytes.append(InputMediaPhoto(img_bytes))

        bot.send_media_group(message.chat.id, imgBytes)



    url = message.text #'https://www.instagram.com/p/C0JRJR_yUCT/?igshid=MzRlODBiNWFlZA&img_index=1'
    # CALL MAIN FUNCTION
    main(url)

bot.polling(none_stop=True)