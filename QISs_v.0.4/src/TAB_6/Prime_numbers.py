import re
from os import path, listdir
from PyQt5.QtCore import QThread
import time
class PrimeGen(QThread):
    def __init__(self, parent=None):
        super(PrimeGen, self).__init__(parent)
        self.value = 0
        self.start_value = 0      
        self.stop_value = 100     
        self.path_to_result = ""  
        self.file_name = ""       
    def run(self):
        try:
            Prime_numbers_Generate(self.start_value, self.stop_value,
                                   self.path_to_result, self.file_name)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def Prime_numbers_Generate(start_pos, stop_pos,
                           path_to_result, file_name):
    start_time = time.time()
    try:
        print(f"-----ГЕНЕРАЦИЯ ПРОСТЫХ ЧИСЕЛ В ДИАПАЗОНЕ от {start_pos} до {stop_pos}-----\n")
        if start_pos != 0:
            list_prime_numbers = []
            for i in range(start_pos, stop_pos + 1, 2):
                if (i > 10) and (i % 10 == 5):
                    continue
                for j in list_prime_numbers:
                    if j * j - 1 > i:
                        list_prime_numbers.append(i)
                        break
                    if (i % j == 0):
                        break
                else:
                    list_prime_numbers.append(i)
        else:
            list_prime_numbers = [2]
            for i in range(3, stop_pos + 1, 2):
                if (i > 10) and (i % 10 == 5):
                    continue
                for j in list_prime_numbers:
                    if j * j - 1 > i:
                        list_prime_numbers.append(i)
                        break
                    if (i % j == 0):
                        break
                else:
                    list_prime_numbers.append(i)
    except Exception as ex:
        print("Возникла ошибка: \n", ex)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'В диапазоне от {start_pos} до {stop_pos} количество сгенерированных чисел: {len(list_prime_numbers)}')
    print(f'\nЗатраченное время: {(elapsed_time / 60):.2f} минут.')
    dst_path = path.join(path_to_result, file_name)
    if path.isfile(dst_path):
        cnt_of_files_in_dir = len(listdir(path_to_result))
        new_name = str(int(cnt_of_files_in_dir)) + '_' + file_name
        dst_path = path.join(path_to_result, new_name)
    with open(dst_path, 'w') as f:
        for item in list_prime_numbers:
            f.write("%s\n" % item)
    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")