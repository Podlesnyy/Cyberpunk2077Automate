import pyautogui
import pydirectinput
import time
import numpy as np
import cv2


class CyberpankBot:
    def __init__(self):
        self.game_window = pyautogui.getWindowsWithTitle('Cyberpunk 2077 (C) 2020 by CD Projekt RED')[0]

        self.cursor_image = self.load_image('cursor.jpg')
        self.filter_all_items_image = self.load_image('filter_all_items.jpg')
        self.untitled18_image = self.load_image('untitled18.jpg')
        self.left_button_image = self.load_image('left_button.jpg')
        self.wait_button_rus_image = self.load_image('wait_button_rus.jpg')

    @staticmethod
    def load_image(image_file_name):
        image = cv2.imread(f'images/{image_file_name}', 0)
        return image

    def __setup_game_window(self):
        self.game_window.left = 0
        self.game_window.top = 0
        self.game_window.activate()
        time.sleep(1)

    def start_selling_untitled18(self, count):
        self.__setup_game_window()
        for i in range(count):
            if i % 5 == 0:
                self.sleep_24_hours()
            self.sell_and_buy_untitled18()

    @staticmethod
    def __enter_shop():
        pyautogui.press('r')
        time.sleep(1)

    @staticmethod
    def press_key(key):
        pyautogui.press(key)
        time.sleep(1)

    def __click_on(self, image):
        screen = self.__get_screen()
        cursor_pos = self.__get_template_location(screen, self.cursor_image)
        filter_all_items_point = self.__get_template_location(screen, image)
        pydirectinput.moveRel(int(filter_all_items_point[0] - cursor_pos[0]),
                              int(filter_all_items_point[1] - cursor_pos[1]), relative=True)
        time.sleep(0.5)
        pydirectinput.click()
        time.sleep(0.3)

    @staticmethod
    def __get_screen():
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        return cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def __get_template_location(screen, image):
        res = cv2.matchTemplate(screen, image, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return min_loc

    def sleep_24_hours(self):
        self.__setup_game_window()
        self.press_key('I')
        self.__click_on(self.wait_button_rus_image)
        self.__click_on(self.left_button_image)
        pydirectinput.moveRel(0, 50, relative=True)
        time.sleep(0.5)
        self.press_key('F')
        self.press_key('ESC')
        time.sleep(15)  # due to biochip glitching

    def sell_and_buy_untitled18(self):
        self.press_key('R')
        self.__click_on(self.filter_all_items_image)
        self.__click_on(self.untitled18_image)
        self.press_key('ESC')
        self.press_key('R')
        self.__click_on(self.untitled18_image)
        self.press_key('ESC')


def main():
    bot = CyberpankBot()
    bot.start_selling_untitled18(10)


if __name__ == '__main__':
    main()