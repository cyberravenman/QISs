import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from src.TAB_2.QRNG import create_dir
from PyQt5.QtCore import QThread
import os
from os import path, listdir
from PyQt5.QtCore import Qt

class Multicolleniarnost(QThread):

    def __init__(self, parent=None):
        super(Multicolleniarnost, self).__init__(parent)

        self.value = 0

        self.path_for_csv = ""          
        self.path_for_result = ""       
        self.name_of_file = ""          
        self.list_widget_csv = None     

    def run(self):
        print("-----ПРОВЕРКА ПАРАМЕТРОВ НА КОЛЛИНЕАРНОСТЬ-----\n")

        try:
            factors = []

            for index in range(self.list_widget_csv.count()):

                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    factors.append(self.list_widget_csv.item(index).text())  

            if len(factors) == 2:   Calc_Multicolleniarnost(self.path_for_csv, self.path_for_result, self.name_of_file, factors)
            else:   print("Выберите 2 фактора для расчета мультиколлинеарности.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class Corrcoefficient(QThread):

    def __init__(self, parent=None):
        super(Corrcoefficient, self).__init__(parent)

        self.value = 0

        self.path_for_csv = ""  
        self.path_for_result = ""  
        self.name_of_file = ""  
        self.list_widget_csv = None  

    def run(self):
        print("-----ПРОВЕРКА КОЭФФИЦИЕНТОВ КОРРЕЛЯЦИИ-----\n")

        try:
            factors = []

            for index in range(self.list_widget_csv.count()):

                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    factors.append(self.list_widget_csv.item(index).text())  

            if len(factors) == 2:
                Calc_Corrcoefficient(self.path_for_csv, self.path_for_result, self.name_of_file, factors)
            else:
                print("Выберите 2 фактора для расчета коэффициентов корреляции.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class VIF(QThread):

    def __init__(self, parent=None):
        super(VIF, self).__init__(parent)

        self.value = 0

        self.path_for_csv = ""  
        self.path_for_result = ""  
        self.name_of_file = ""  
        self.list_widget_csv = None  

    def run(self):
        print("-----ПРОВЕРКА КОЭФФИЦИЕНТОВ КОРРЕЛЯЦИИ-----\n")

        try:
            factors = []

            for index in range(self.list_widget_csv.count()):

                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    factors.append(self.list_widget_csv.item(index).text())  

            Calc_VIF(self.path_for_csv, self.path_for_result, self.name_of_file, factors)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Calc_Multicolleniarnost(path_to_csv, output_path, output_file, factors):

    data = pd.read_csv(path_to_csv, sep=',')

    plt.style.use('seaborn-v0_8')
    plt.scatter(data[factors[0]], data[factors[1]], color='#7e1e9c')
    plt.title(f'Отношение {factors[0]} к {factors[1]}\nФайл: {path_to_csv}')
    plt.xlabel(f'{factors[0]}')
    plt.ylabel(f'{factors[1]}')

    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file)

    else:

        dst_path = path.join(output_path, output_file)

        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path)) + 1) + '_' + output_file
            dst_path = path.join(output_path, new_name)

    plt.savefig(dst_path)  

def Calc_Corrcoefficient(path_to_csv, output_path, output_file, factors):

    data = pd.read_csv(path_to_csv, sep=',')

    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file)

    else:

        dst_path = path.join(output_path, output_file)

        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path)) + 1) + '_' + output_file
            dst_path = path.join(output_path, new_name)

    matrix_with_corcoeff = np.corrcoef(data[factors[0]], data[factors[1]])

    first_str = f'Коэффициент корреляции для {factors[0]} и {factors[1]} успешно вычислен.\n'
    print(first_str)
    print(matrix_with_corcoeff)

    with open(dst_path, 'w') as file_with_coefcorr:
        file_with_coefcorr.write(first_str+'\n')
        content = str(matrix_with_corcoeff)
        file_with_coefcorr.write(content)
    file_with_coefcorr.close()

def Calc_VIF(path_to_csv, output_path, output_file, factors):

    data = pd.read_csv(path_to_csv, sep=',')

    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file)

    else:

        dst_path = path.join(output_path, output_file)

        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path)) + 1) + '_' + output_file
            dst_path = path.join(output_path, new_name)

    X = data[factors]

    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns

    vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                       for i in range(len(X.columns))]

    first_str = f'Степень мультиколлинеарности для факторов {factors} успешно найдена.\n'
    print(first_str + '\n')
    print(vif_data)

    with open(dst_path, 'w') as file_with_vif:
        file_with_vif.write(first_str+'\n')
        content = str(vif_data)
        file_with_vif.write(content)
    file_with_vif.close()