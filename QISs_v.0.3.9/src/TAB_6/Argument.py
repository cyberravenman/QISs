import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.genmod import families
from src.TAB_2.QRNG import create_dir
from PyQt5.QtCore import QThread
import os
from os import path, listdir
from PyQt5.QtCore import Qt

class CountArgument(QThread):

    def __init__(self, parent=None):
        super(CountArgument, self).__init__(parent)

        self.value = 0

        self.path_for_csv = ""  
        self.path_for_result = ""  
        self.name_of_file = ""  
        self.list_widget_csv = None  

    def run(self):
        print("-----ПРОВЕРКА ПАРАМЕТРОВ НА КОЛЛИНЕАРНОСТЬ-----\n")

        try:
            argument = []

            for index in range(self.list_widget_csv.count()):

                if self.list_widget_csv.item(index).checkState() == Qt.Checked:
                    argument.append(self.list_widget_csv.item(index).text())  

            if len(argument) == 1:
                Calc_CountArgument(self.path_for_csv, self.path_for_result, self.name_of_file, argument)
            else:
                print("Выберите 1 аргумент для определения частоты встречаемости.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class BinomialModeling(QThread):

    def __init__(self, parent=None):
        super(BinomialModeling, self).__init__(parent)

        self.value = 0

        self.path_for_csv = ""          

        self.path_for_result = ""       
        self.name_of_file = ""          

        self.MLE_or_IRLS = False        

        self.list_widget_csv_fac = None 
        self.list_widget_csv_arg = None 

    def run(self):
        print("-----ПОСТРОЕНИЕ МОДЕЛИ ЛОГИСТИЧЕСКОЙ РЕГРЕССИИ-----\n")

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
                    Fit_Binomial_Model(self.path_for_csv, self.path_for_result, self.name_of_file,
                                       argument, factors,
                                       self.MLE_or_IRLS)
                else:
                    print("Выберите не менее одного фактора.")
            else:
                print("Выберите 1 аргумент.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Calc_CountArgument(path_to_csv, output_path, output_file, argument):
    data = pd.read_csv(path_to_csv, sep=',')

    plt.style.use('seaborn-v0_8')

    ax = data[argument[0]].value_counts().plot(kind='bar')
    ax.set_title(f'Пропорция положительных и отрицательных исходов\nФайл: {path_to_csv}')
    ax.set_xlabel('Исход'); ax.set_ylabel('Количество')

    ax = plt.gca(); p = ax.patches
    height_of_one = p[0].get_height();  print("height_of_one:  ", height_of_one)
    height_of_zero = p[1].get_height(); print("height_of_zero:  ", height_of_zero)

    rects = ax.patches

    height = rects[0].get_height()
    ax.text(rects[0].get_x() + rects[0].get_width() / 2, height + 1, height_of_one, ha="center", va="bottom")

    height = rects[1].get_height()
    ax.text(rects[1].get_x() + rects[1].get_width() / 2, height + 1, height_of_zero, ha="center", va="bottom")

    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file)

    else:

        dst_path = path.join(output_path, output_file)

        if path.isfile(dst_path):
            new_name = str(len(listdir(output_path)) + 1) + '_' + output_file
            dst_path = path.join(output_path, new_name)

    plt.savefig(dst_path)
    plt.clf()

def Fit_Binomial_Model(path_to_csv, output_path, output_file,
                       argument, factors,
                       MLE_or_IRLS):

    data = pd.read_csv(path_to_csv, sep=',')

    if MLE_or_IRLS:
        logit_model = sm.GLM(
            data[argument],
            data[factors],
            family=families.Binomial(),
        ).fit()

        print("Логистическая регрессия. Метод: IRLS.\n[Iteratively reweighted least squares]\n\n")

        name_for_model = os.path.splitext(output_file)[0] + "_IRLS.txt"
        name_for_model_csv = os.path.splitext(output_file)[0] + "_IRLS.csv"
        name_for_Cook = os.path.splitext(output_file)[0] + "_Cook_dst_IRLS.png"
    else:
        logit_model = sm.Logit(
            data[argument],
            data[factors]
        ).fit()

        print("\n\nЛогистическая регрессия. Метод: MLE\n[Maximum likelihood estimation]\n\n")

        name_for_model = os.path.splitext(output_file)[0] + "_MLE.txt"
        name_for_model_csv = os.path.splitext(output_file)[0] + "_MLE.csv"
        name_for_Cook = os.path.splitext(output_file)[0] + "_Cook_dst_MLE.png"

    print(logit_model.summary())

    model_odds = pd.DataFrame(np.exp(logit_model.params), columns=['ODDS RATIO'])
    print("\n\nODDS RATIO: \n\n", model_odds)

    infl = logit_model.get_influence()  
    fig = infl.plot_index(y_var="cooks")  
    fig.tight_layout()

    if not os.path.exists(output_path):

        create_dir(output_path)

        dst_path = path.join(output_path, name_for_model)
        dst_path_csv = path.join(output_path, name_for_model_csv)

        dst_path_Cook = path.join(output_path, name_for_Cook)

    else:

        dst_path = path.join(output_path, name_for_model)
        dst_path_Cook = path.join(output_path, name_for_Cook)
        dst_path_csv = path.join(output_path, name_for_model_csv)

        if path.isfile(dst_path):
            cnt_of_files_in_dir = len(listdir(output_path))
            new_name = str(int(cnt_of_files_in_dir/3) + 1) + '_' + name_for_model
            dst_path = path.join(output_path, new_name)
        if path.isfile(dst_path_csv):
            cnt_of_files_in_dir = len(listdir(output_path))
            new_name_csv = str(int(cnt_of_files_in_dir / 3) + 1) + '_' + name_for_model_csv
            dst_path_csv = path.join(output_path, new_name_csv)
        if path.isfile(dst_path_Cook):
            cnt_of_files_in_dir = len(listdir(output_path))
            new_name_Cook = str(int(cnt_of_files_in_dir/3) + 1) + '_' + name_for_Cook
            dst_path_Cook = path.join(output_path, new_name_Cook)

    with open(dst_path, 'w') as file_with_model:
        content = str(logit_model.summary())
        file_with_model.write(content)

        file_with_model.write("\n\n-----------------ODDS RATIO-----------------\n")
        content_odds = str(model_odds)
        file_with_model.write(content_odds)
        file_with_model.close()

    try:
        with open(dst_path_csv, 'a') as file_csv:

            file_csv.write(logit_model.summary().as_csv())

            file_csv.write("\n\n")
            content = str(model_odds)
            file_csv.write(content)

        plt.savefig(dst_path_Cook)
    except Exception as ex:
        print('Не удалось сохранить некоторые файлы.\n', ex)

    file_with_model.close()
    file_csv.close()
    plt.clf()