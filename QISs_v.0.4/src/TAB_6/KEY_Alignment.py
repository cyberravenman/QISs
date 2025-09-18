import math
import os
import random
from datetime import date
from pathlib import Path
import numpy as np
from PyQt5.QtCore import QThread
from matplotlib import pyplot as plt, cm
import shutil
from src.TAB_1.Gen_Scheme import create_dir
class KeyAlignment(QThread):
    def __init__(self, parent=None):
        super(KeyAlignment, self).__init__(parent)
        self.value = 0
        self.path_to_qubits = ""                                
        self.dir_output = ""                                    
        self.file_name_bad = "KEY_before_shift.txt"                 
        self.file_name_transpose = "transpose"                  
        self.file_name_result = "KEY_after_shift.txt"               
        self.file_p_value_csv = "P_value.csv"                   
        self.alpha = 0.01                                       
        self.bitmap_before_shift = "KEY_before_shift.png"       
        self.bitmap_after_shift = "KEY_after_shift.png"         
        self.RNG_from_file = False              
        self.file_with_RNG_numbers = ""         
    def run(self):
        print(f"-----ВЫРАВНИВАНИЕ ПОСЛЕДОВАТЕЛЬНОСТЕЙ-----\n")
        if self.RNG_from_file:
            if self.file_with_RNG_numbers == "":
                print("Выберите файл со значениями для сдвига СП")
                return
        try:
            if not os.path.exists(self.dir_output):
                dir_output = self.dir_output + "/experiment_0"
                create_dir(dir_output)
            else:
                cnt_of_files_in_dir = len(os.listdir(self.dir_output))
                new_name = "/experiment_" + str(int(cnt_of_files_in_dir))
                dir_output = self.dir_output + new_name
                create_dir(dir_output)
            dst_for_bad = os.path.join(dir_output, self.file_name_bad)
            dst_path_transpose = os.path.join(dir_output, self.file_name_transpose)
            dst_path_good = os.path.join(dir_output, self.file_name_result)
            dst_path_bitmap_bad = os.path.join(dir_output, self.bitmap_before_shift)
            dst_path_bitmap_good = os.path.join(dir_output, self.bitmap_after_shift)
            dst_path_pvalue = os.path.join(dir_output, self.file_p_value_csv)
            try:
                print("\nКопирование каталога с плохими СП   : ", end='')
                recursive_copy(self.path_to_qubits, dir_output)
                print("Успешно")
            except Exception as ex:
                print(f'Не удалось выполнить копирование каталога с плохими СП\n'
                      f'Выбранная директория : {self.path_to_qubits}\n'
                      f'Ошибка : {ex}')
            try:
                print("Сортировка файлов по номерам кубит : ", end='')
                txt_files = sort_sequences(dir_output)
                print("Успешно")
            except Exception as ex:
                print(f'Не удалось выполнить сортировку файлов с плохими СП.\n'
                      f'Сортировка выполняется по наименованиям файлов с СП, где в начале имени файла должен быть номер кубита,'
                      f'сгенерировавшего данную последовательность\n'
                      f'Ошибка : {ex}')
            try:
                print("Выравнивание последовательностей   : ", end='')
                alignment_sequences(txt_files,
                                    dst_for_bad, dst_path_transpose, dst_path_good,
                                    dst_path_bitmap_bad, dst_path_bitmap_good,
                                    self.RNG_from_file, self.file_with_RNG_numbers,
                                    dst_path_pvalue, self.alpha)
            except Exception as ex:
                print(f'Не удалось выполнить выравнивание последовательностей.\n'
                      f'Путь для сохранения плохого ключа : {dst_for_bad}\n'
                      f'Путь для сохранения результата транспонирования : {dst_path_transpose}\n'
                      f'Путь для сохранения выравненного ключа : {dst_path_good}\n'
                      f'Путь для сохранения bitmap хорошего ключа : {dst_path_bitmap_good}\n'
                      f'Путь для сохранения bitmap плохого ключа : {dst_path_bitmap_bad}\n'
                      f'Файл со случайными значениями сдвига СП : {self.file_with_RNG_numbers}\n'
                      f'Ошибка : {ex}')
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def recursive_copy(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        source_item = os.path.join(src, item)
        dest_item = os.path.join(dst, item)
        if os.path.isdir(source_item):
            recursive_copy(source_item, dest_item)
        else:
            shutil.copy2(source_item, dest_item)
def sort_sequences(directory_name):
    txt_files_no_path = []
    path_to_txt_files = []
    txt_sorted_result = []
    dic = {}
    pth = Path(directory_name)
    for file_name in pth.rglob('*.[tT][xX][tT]'):
        txt_files_no_path.append(file_name.name)
        path_to_txt_files.append(os.path.dirname(os.path.abspath(file_name)))
    txt_files_no_path.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    path_to_txt_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if (len(txt_files_no_path) == len(path_to_txt_files)):
        for i in range(0, len(txt_files_no_path)):
            txt_sorted_result.append((path_to_txt_files[i] + '/' + txt_files_no_path[i]))
    return txt_sorted_result
def bitmap_of_sequence(random_sequence, name_of_bitmap):
    sequence = [];  len_of_sequence = len(random_sequence)
    if len_of_sequence == 0:    return
    for i in range(0, len_of_sequence):
        sequence.append(int(random_sequence[i]))
    len_of_sequence = len(sequence)
    size_of_bitmap_max = 4096 * 4096
    if len_of_sequence > size_of_bitmap_max:
        len_of_sequence = 4096 ** 2;    x_axis = 4096;  y_axis = 4096
    else:
        len_of_sequence = math.floor(math.sqrt(len_of_sequence))
        x_axis = len_of_sequence;   y_axis = len_of_sequence;   len_of_sequence = len_of_sequence ** 2
    sequence_slice = sequence[0:len_of_sequence]
    plt.imsave(name_of_bitmap, np.array(sequence_slice).reshape(x_axis, y_axis), cmap=cm.gray)
    plt.clf()
def shift(array, shift_amount):
    ans = []
    if shift_amount < 0:
        return ans
    for i in range(len(array)):
        ans.append(array[(i - shift_amount) % len(array)])
    return ans
def alignment_sequences(sequences,
                        file_for_bad, file_for_transpose, file_for_result,
                        name_before_shift, name_after_shift,
                        RNG_from_file, file_with_RNG,
                        file_csv_pvalue, alpha):
    sequences_before_shift = []
    l_of_l = []
    dir_for_result_save = []
    for i in range (0, len(sequences)):
        dir_for_result_save.append('/'.join(sequences[i].split('/')[:-1]))
        dir_for_result_save[i] = '/'.join(dir_for_result_save[i].split('/')[-1:])
    for file_name in sequences:
        with open(file_name) as infile:
            tmp = infile.read().strip()
            sequences_before_shift.append(tmp)
            n = 1
            result = [tmp[idx: idx + n] for idx in range(0, len(tmp), n)]
            l_of_l.append(result)
    with open(file_for_bad, 'w+') as outfile:
        for i in range(0, len(sequences_before_shift)):
            outfile.write(str(sequences_before_shift[i]))
    matrix = np.array(l_of_l)
    matrix_transpose = np.transpose(matrix)
    with open(file_for_transpose, 'w+') as outfile:
        for i in range(0, len(matrix_transpose)):
            outfile.write(str(matrix_transpose[i]) + '\n')
    if RNG_from_file:
        with open(file_with_RNG, 'r') as f:
            lines = sum(1 for line in f)
        if lines < len(matrix_transpose):
            print(f"\nКоличество чисел в файле меньше числа необходимых перестановок.\n"
                  f"Необходимо {len(matrix_transpose)} случайных чисел, в указанном файле -- всего {lines} значений.");   return
        else:
            with open(file_with_RNG, 'r') as f:
                mas_with_numbers = f.read().splitlines()    
                rand_mas = random.sample(mas_with_numbers, len(matrix_transpose))   
    else:
        rand_mas = []
        for i in range(0, len(matrix_transpose)):
            rand_mas.append(random.randint(1, 100))
    for i in range(0, len(matrix_transpose)):
        try:
            tmp = shift(matrix_transpose[i], int(rand_mas[i]))
            matrix_transpose[i] = tmp
        except Exception as ex:
            print(f'Что-то пошло не так. Проверьте, что в файла записаны числа с новой строки. \n\nERROR: {ex}');    return
    matrix_transpose_2 = np.transpose(matrix_transpose)
    matrix_result = []
    for i in range(0, len(matrix_transpose_2)):
        tmp = "".join([sub[0] for sub in matrix_transpose_2[i]])
        matrix_result.append(tmp)
    with open(file_for_result, 'w+') as outfile:
        for i in range(0, len(matrix_result)):
            outfile.write(str(matrix_result[i]))
    if len(dir_for_result_save) == len(matrix_result):
        csv_str_1 = "Qubit,alpha,P_value_before,Quality_before,P_value_after,Quality_after"
        csv_file_with_pvalue = open(file_csv_pvalue, "a")
        if os.stat(file_csv_pvalue).st_size == 0:  csv_file_with_pvalue.write(csv_str_1)
        cnt_before = 0
        cnt_after = 0
        for i in range(0, len(dir_for_result_save)):
            path_for_result = '/'.join(sequences[0].split('/')[:-2]) + '/' + str(dir_for_result_save[i]) + '/' + str(dir_for_result_save[i]) + '_after_shift.txt'
            path_for_bitmap = '/'.join(sequences[0].split('/')[:-2]) + '/' + str(dir_for_result_save[i]) + '/' + str(dir_for_result_save[i]) + '_after_shift.png'
            with open(path_for_result, 'w+') as outfile:
                outfile.write(str(matrix_result[i]))
                key_sequence = []
                cnt = 0
                while cnt < len(matrix_result[i]):
                    bit1 = matrix_result[i][cnt]
                    if not bit1:    break
                    if bit1.isdigit():  key_sequence.append(int(bit1))
                    cnt+=1
                bitmap_of_sequence(key_sequence, path_for_bitmap)
            p_value_before = calculate_Pvalue(sequences_before_shift[i])
            quality_before = 0
            if p_value_before > alpha:  quality_before = 1; cnt_before += 1
            p_value_after = calculate_Pvalue(matrix_result[i])
            quality_after = 0
            if p_value_after > alpha:   quality_after = 1;  cnt_after += 1
            csv_file_with_pvalue.write(f"\n{dir_for_result_save[i]},0.01,{p_value_before},{quality_before},{p_value_after},{quality_after}")
        print("Успешно")
        print(f'\nКоличество хороших кубит до выравнивания: {cnt_before}\n'
              f'Количество хороших кубит после выравнивания: {cnt_after}')
    print("\nОтрисовка BitMap                                    : ", end='')
    key_sequence_before = []
    with open(file_for_bad, 'r', encoding='utf-8') as file:
        while True:
            bit1 = file.read(1)
            if not bit1:    break
            if bit1.isdigit():  key_sequence_before.append(int(bit1))
    bitmap_of_sequence(key_sequence_before, name_before_shift)
    key_sequence_after = []
    with open(file_for_result, 'r', encoding='utf-8') as file:
        while True:
            bit1 = file.read(1)
            if not bit1:    break
            if bit1.isdigit():  key_sequence_after.append(int(bit1))
    bitmap_of_sequence(key_sequence_after, name_after_shift)
    print("Успешно")
def calculate_Pvalue(string_of_bits):
    bitstring_list = []  
    len_of_birstring = len(string_of_bits)  
    for j in range(0, len_of_birstring):  
        bitstring_list.append(int(string_of_bits[j]))
    s = sum(bitstring_list) + (
                (len_of_birstring - sum(bitstring_list)) * (-1))  
    s_obs = abs(s) / math.sqrt(len_of_birstring)  
    p_value = s_obs / math.sqrt(2)  
    p_value_final = math.erfc(p_value)  
    return (p_value_final)