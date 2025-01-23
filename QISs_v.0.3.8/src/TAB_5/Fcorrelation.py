from datetime import date
from datetime import datetime
from src.TAB_2.QRNG import create_dir
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
from PyQt5.QtCore import QThread
import pandas as pd
import seaborn as sns
import os

class FCorrEasy(QThread):

    def __init__(self, parent=None):
        super(FCorrEasy, self).__init__(parent)

        self.value = 0

        self.USR_FILE_NAME_1 = ""   
        self.USR_FILE_NAME_2 = ""   

    def run(self):
        print("-----ВЫЧИСЛЕНИЕ ВЗАИМНОЙ КОРРЕЛЯЦИИ ДВУХ ФАЙЛОВ-----\n")

        try:
            Fcorr_easy(self.USR_FILE_NAME_1, self.USR_FILE_NAME_2)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class FCorrProfi(QThread):

    def __init__(self, parent=None):
        super(FCorrProfi, self).__init__(parent)

        self.value = 0

        self.USR_FILE_NAME_1 = ""   
        self.USR_FILE_NAME_2 = ""   

    def run(self):
        print("-----ВЫЧИСЛЕНИЕ ВЗАИМНОЙ КОРРЕЛЯЦИИ [С ЦИКЛИЧЕСКИМ СДВИГОМ]-----\n")

        try:
            Fcorr_profi(self.USR_FILE_NAME_1, self.USR_FILE_NAME_2)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class FCorrMatrix(QThread):

    def __init__(self, parent=None):
        super(FCorrMatrix, self).__init__(parent)

        self.value = 0

        self.csv_for_matrix = ""        
        self.path_for_output_txt = ""        
        self.path_for_output_image = "" 
        self.method = ""                

    def run(self):
        print("-----ВЫЧИСЛЕНИЕ КОРРЕЛЯЦИОННОЙ МАТРИЦЫ-----\n")

        try:
            calculate_cor_matrix(self.csv_for_matrix, self.path_for_output_txt, self.path_for_output_image, self.method)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Fcorr_easy(file1, file2):

    bit_string_1 = []           
    bit_string_2 = []           
    result_of_function = []     

    USR_NEED_INVERSE = True     

    with open(file1, 'r', encoding='utf-8') as file:
        while True:
            bit1 = file.read(1)
            if not bit1:    break
            if bit1.isdigit():  bit_string_1.append(int(bit1))
    with open(file2, 'r', encoding='utf-8') as file:
        while True:
            bit2 = file.read(1)
            if not bit2:    break
            if bit2.isdigit():  bit_string_2.append(int(bit2))

    SIZE_OF_BITSTRING = len(bit_string_2)  

    xor_list = []  

    for j in range(0, SIZE_OF_BITSTRING):
        xor_list.append(bit_string_1[j] ^ bit_string_2[j])

    if (USR_NEED_INVERSE):
        xor_list = [k ^ 1 for k in xor_list]

    corr_func = sum(xor_list) + ((SIZE_OF_BITSTRING - sum(xor_list)) * (-1))

    result_of_function.append(corr_func / SIZE_OF_BITSTRING)
    print("result: ", result_of_function)

    number_of_interation = []
    for i in range(0, len(result_of_function)):
        number_of_interation.append(i)

    plt.style.use("seaborn")
    plt.figure(figsize=(15, 3))  

    TITLE_1 = "График корреляции двух последовательностей" + '\n' + "Fcorr = " + str(sum(result_of_function))

    user_time = datetime.now(); current_time = user_time.strftime("%H:%M:%S");  current_date = date.today()
    PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/Instruments/Corr/Fcorr_NO_shift/" + str(current_date)
    create_dir(PATH_TO_PROJECT_QIS)

    TITLE_2 = PATH_TO_PROJECT_QIS + f"/{current_time}.png"

    plt.title(TITLE_1)
    plt.ylabel('Значение функции')
    plt.xlabel('Номер итерации')

    plt.scatter(number_of_interation, result_of_function)  

    plt.savefig(TITLE_2)  

def Fcorr_profi(file1, file2):

    bit_string_1 = []  
    bit_string_2 = []  
    result_of_function = []  

    USR_NEED_INVERSE = True  
    USR_SHIFT = 1  

    with open(file1, 'r', encoding='utf-8') as file:
        while True:
            bit1 = file.read(1)
            if not bit1:    break
            if bit1.isdigit():  bit_string_1.append(int(bit1))

    with open(file2, 'r', encoding='utf-8') as file:
        while True:
            bit2 = file.read(1)
            if not bit2:    break
            if bit2.isdigit():  bit_string_2.append(int(bit2))

    SIZE_OF_BITSTRING = len(bit_string_2)  

    for i in range(0, SIZE_OF_BITSTRING):
        xor_list = []  

        for j in range(0, SIZE_OF_BITSTRING):
            xor_list.append(bit_string_1[j] ^ bit_string_2[j])

        if (USR_NEED_INVERSE):
            xor_list = [k ^ 1 for k in xor_list]

        corr_func = sum(xor_list) + ((SIZE_OF_BITSTRING - sum(xor_list)) * (-1))

        result_of_function.append(corr_func / SIZE_OF_BITSTRING)

        bit_string_2 = bit_string_2[-USR_SHIFT:] + bit_string_2[:-USR_SHIFT]  

    print(sum(result_of_function) / SIZE_OF_BITSTRING)

    number_of_interation = []
    for i in range(0, len(result_of_function)):
        number_of_interation.append(i)

    plt.style.use('seaborn')
    plt.figure(figsize=(15, 3))  

    TITLE_1 = "График корреляции двух последовательностей" + '\n' + "Fcorr = " + str(sum(result_of_function) / SIZE_OF_BITSTRING)

    user_time = datetime.now(); current_time = user_time.strftime("%H:%M:%S");  current_date = date.today()
    PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/Instruments/Corr/Fcorr_WITH_shift/" + str(current_date)
    create_dir(PATH_TO_PROJECT_QIS)

    TITLE_2 = PATH_TO_PROJECT_QIS + f"/{current_time}.png"

    plt.title(TITLE_1)
    plt.ylabel('Значение функции')
    plt.xlabel('Номер итерации')

    plt.scatter(number_of_interation, result_of_function)  

    plt.savefig(TITLE_2)  

def calculate_cor_matrix(csv_for_corr_matrix, path_for_cor_matrix, path_for_image_with_cor_matrix, corr_method):

    df = pd.read_csv(csv_for_corr_matrix, sep=',')
    print(df)

    correlation_matrix = df.corr(method=corr_method)

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Корреляционная матрица')

    file_name = os.path.basename(csv_for_corr_matrix);  file = os.path.splitext(file_name)

    create_dir(path_for_image_with_cor_matrix)
    create_dir(path_for_cor_matrix)

    path_for_image_with_cor_matrix = path_for_image_with_cor_matrix + '/' + file[0] + '.png'
    plt.savefig(path_for_image_with_cor_matrix)

    path_for_cor_matrix = path_for_cor_matrix + '/' + file[0] + '.txt'
    f = open(path_for_cor_matrix, 'w'); f.write(correlation_matrix.to_string(index=False));  f.close()