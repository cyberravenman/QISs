import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

class BitmapLaunch(QThread):

    def __init__(self, parent=None):
        super(BitmapLaunch, self).__init__(parent)

        self.value = 0

        self.path_to_folder = "" 

    def run(self):
        print("-----ФОРМИРОВАНИЕ 'BITMAP' ДЛЯ СП-----\n")

        try:
            calculate_Bitmap(self.path_to_folder)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def calculate_Bitmap(path):
    sequence = []

    txt_files = list(Path(path).rglob("*.[tT][xX][tT]"))

    for file_name in txt_files:
        with open(file_name, 'r', encoding='utf-8') as file:

            while True:
                bit1 = file.read(1)
                if not bit1:    break
                if bit1.isdigit():  sequence.append(int(bit1))
        if len(sequence) == 0:
            print("Размер файла равен 0.");  print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
            QApplication.restoreOverrideCursor();   return
        if len(sequence) == -1:
            print("Файл не найден.");  print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
            QApplication.restoreOverrideCursor();   return

        len_of_sequence = len(sequence)
        if len_of_sequence > 2 ** 20:
            len_of_sequence = 1024 ** 2;    x_axis = 1024;  y_axis = 1024
        else:
            len_of_sequence = math.floor(math.sqrt(len_of_sequence))
            x_axis = len_of_sequence;   y_axis = len_of_sequence;   len_of_sequence = len_of_sequence ** 2

        sequence_slice = sequence[0:len_of_sequence]

        path, filename = os.path.split(file_name);  file_bitmap = path + "/" + file_name.stem + ".png"

        plt.imsave(file_bitmap, np.array(sequence_slice).reshape(x_axis, y_axis), cmap=cm.gray)
        plt.clf()
        print(f"BitMap '{filename}' успешно сохранен. Картинка находится в расположении: ", file_bitmap)