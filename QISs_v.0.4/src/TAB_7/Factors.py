import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from statsmodels.stats.outliers_influence import variance_inflation_factor
from src.TAB_2.QRNG import create_dir
from PyQt5.QtCore import QThread
import os
from os import path, listdir
from PyQt5.QtCore import Qt
from sklearn.svm import SVR
from sklearn.feature_selection import RFE
class Interrelation(QThread):
    def __init__(self, parent=None):
        super(Interrelation, self).__init__(parent)
        self.value = 0
        self.path_for_csv = ""          
        self.path_for_result = ""       
        self.name_of_file = ""          
        self.list_widget_csv = None     
    def run(self):
        print("-----ЗАВИСИМОСТЬ ДВУХ ФАКТОРОВ-----\n")
        try:
            factors = []
            for index in range(self.list_widget_csv.count()):
                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    factors.append(self.list_widget_csv.item(index).text())  
            if len(factors) == 2:   Calc_Interrelation(self.path_for_csv, self.path_for_result, self.name_of_file, factors)
            else:   print("Выберите 2 фактора для отображения зависимости.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class CorrVIF(QThread):
    def __init__(self, parent=None):
        super(CorrVIF, self).__init__(parent)
        self.value = 0
        self.path_for_csv = ""          
        self.path_for_result = ""       
        self.name_of_file_corr = ""     
        self.name_of_file_vif = ""      
        self.duplicate = False          
        self.list_widget_csv = None     
    def run(self):
        print("-----ПРОВЕРКА КОЭФФИЦИЕНТОВ КОРРЕЛЯЦИИ-----\n")
        try:
            factors = []
            for index in range(self.list_widget_csv.count()):
                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    factors.append(self.list_widget_csv.item(index).text())  
            Calc_Corr_VIF(self.path_for_csv,
                                 self.path_for_result, self.name_of_file_corr, self.name_of_file_vif,
                                 factors, self.duplicate)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class FactorsSignificance(QThread):
    def __init__(self, parent=None):
        super(FactorsSignificance, self).__init__(parent)
        self.value = 0
        self.path_for_csv = ""  
        self.features_to_select = 0     
        self.list_widget_csv_fac = None  
        self.list_widget_csv_arg = None  
    def run(self):
        print("-----ОПРЕДЕЛЕНИЕ ЗНАЧИМОСТИ ФАКТОРОВ-----\n")
        try:
            argument = []
            for index in range(self.list_widget_csv_arg.count()):
                if self.list_widget_csv_arg.item(index).checkState() == Qt.Checked:
                    argument.append(self.list_widget_csv_arg.item(index).text())  
            if len(argument) == 1:
                factors = []
                for index in range(self.list_widget_csv_fac.count()):
                    if self.list_widget_csv_fac.item(index).checkState() == Qt.Checked:
                        factors.append(self.list_widget_csv_fac.item(index).text())  
                if len(factors) != 0:
                    Calc_Factors_Significance(self.path_for_csv, argument, factors, self.features_to_select)
                else:
                    print("Выберите не менее одного фактора.")
            else:
                print("Выберите 1 аргумент.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def Calc_Interrelation(path_to_csv, output_path, output_file, factors):
    data = pd.read_csv(path_to_csv, sep=',')
    plt.style.use('seaborn-v0_8')
    plt.scatter(data[factors[0]], data[factors[1]], color='
    plt.title(f'Отношение {factors[0]} к {factors[1]}\nФайл: {path_to_csv}')
    plt.xlabel(f'{factors[0]}');    plt.ylabel(f'{factors[1]}')
    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file)
    else:
        dst_path = path.join(output_path, output_file)
        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path)) + 1) + '_' + output_file
            dst_path = path.join(output_path, new_name)
    try:
        plt.savefig(dst_path)   
        print(f'Изображение успешно сохранено в файл {dst_path}')
        plt.clf()  
    except Exception as ex:
        print("Не удалось сохранить изображение.\n", ex)
def Calc_Corr_VIF(path_to_csv,
                         output_path, output_file_corr, output_file_vif,
                         factors, duplicate):
    data = pd.read_csv(path_to_csv, sep=',', usecols=factors)
    matrix_with_corcoeff = data.corr()
    current_date = date.today()
    output_path_corr = output_path + "CorrCoef/" + str(current_date)
    output_path_vif = output_path + "VIF/" + str(current_date)
    if not os.path.exists(output_path_corr):
        create_dir(output_path_corr)
        dst_path = path.join(output_path_corr, output_file_corr)
    else:
        dst_path = path.join(output_path_corr, output_file_corr)
        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path_corr)) + 1) + '_' + output_file_corr
            dst_path = path.join(output_path_corr, new_name)
    first_str = f'Коэффициент корреляции для {factors[0]} и {factors[1]} успешно вычислен.\n'
    print(first_str)
    print(matrix_with_corcoeff)
    try:
        matrix_with_corcoeff.to_csv(dst_path, index=False)
        print(f'Результат успешно записан в файл {dst_path}')
    except Exception as ex:
        print('Не удалось сохранить результат.\n', ex)
    if duplicate:
        print("Duplicate: ", duplicate)
        try:
            with open(path_to_csv, 'a') as file_csv:
                file_csv.write("\n")
                file_csv.write("Correlation:\n")
            file_csv.close()
        except Exception as ex:
            print('Error.\n', ex)
        try:
            matrix_with_corcoeff.to_csv(path_to_csv, mode='a', index=False)
            print(f'Результат успешно сохранен в файл {dst_path}')
        except Exception as ex:
            print('Не удалось сохранить результат в файл.\n', ex)
    if not os.path.exists(output_path_vif):
        create_dir(output_path_vif)
        dst_path = path.join(output_path_vif, output_file_vif)
    else:
        dst_path = path.join(output_path_vif, output_file_vif)
        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path_vif)) + 1) + '_' + output_file_vif
            dst_path = path.join(output_path_vif, new_name)
    X = data[factors]
    vif_data = pd.DataFrame();  vif_data["Factors"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                       for i in range(len(X.columns))]
    first_str = f'Степень мультиколлинеарности для факторов {factors} успешно найдена.\n'
    print(first_str + '\n');    print(vif_data)
    try:
        vif_data.to_csv(dst_path, index=False)
        print(f'Результат успешно сохранен в файл {dst_path}')
    except Exception as ex:
        print('Не удалось сохранить результат в файл.\n', ex)
    if duplicate:
        try:
            with open(path_to_csv, 'a') as file_csv:
                file_csv.write("\n")
                file_csv.write("Variance_Inflation:\n")
            file_csv.close()
        except Exception as ex:
            print('Error.\n', ex)
        try:
            vif_data.to_csv(path_to_csv, mode='a', index=False)
            print(f'Результат успешно сохранен в файл {dst_path}')
        except Exception as ex:
            print('Не удалось сохранить результат в файл.\n', ex)
def Calc_Factors_Significance(path_to_csv, argument, factors, features_to_select):
    df = pd.read_csv(path_to_csv)
    X = df[factors]
    Y = df[argument]
    estimator = SVR(kernel="linear")
    selector = RFE(estimator, n_features_to_select=features_to_select, step=1)
    selector = selector.fit(X, Y.values.ravel())
    print(f'Факторы для анализа: {factors}')
    print(f'Рекомендуемые факторы для моделирования:\n{selector.support_}\n')
    print(f'Степень значимости факторов: {selector.ranking_}\n')