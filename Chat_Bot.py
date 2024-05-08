from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChatBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # headless modunu kapat
        self.driver = webdriver.Chrome(options=options)
        self.last_user_input = None
        self.last_seen_response = None

    def send_message(self, input_text):
        textbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='textbox']"))
        )
        textbox.clear()
        textbox.send_keys(input_text + Keys.RETURN)

    def check_for_new_responses(self):
        response_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='message bot svelte-a99nd8 latest']"))
        )
        time.sleep(5)
        responses = [element.text.strip() for element in response_elements if element.text.strip()]
        if responses:
            new_response = responses[-1]
            if new_response != self.last_seen_response and self.last_user_input != new_response:
                self.last_seen_response = new_response
                return self.last_seen_response
        return None

    def start_chat(self):
        self.driver.get("https://yuntian-deng-chatgpt.hf.space")
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "component-23")))
        button.click()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()

        while True:
            try:
                user_input = input("Sen: ")
                if user_input.lower() == 'çıkış':
                    break
                self.last_user_input = user_input
                self.send_message(user_input)
                while True:
                    response = self.check_for_new_responses()
                    if response:  # Yeni cevap varsa yazdır
                        print("Bot:", response)
                        break
            except KeyboardInterrupt:
                print("\nKullanıcı tarafından kesildi.")
                break

        self.driver.quit()

if __name__ == "__main__":
    chat_bot = ChatBot()
    chat_bot.start_chat()
