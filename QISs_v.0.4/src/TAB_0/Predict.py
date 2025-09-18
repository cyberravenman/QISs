import pandas as pd
import numpy as np
import statsmodels.api as sm
from src.TAB_2.QRNG import create_dir
from PyQt5.QtCore import QThread
import os
from os import path, listdir
class PredictValues(QThread):
    def __init__(self, parent=None):
        super(PredictValues, self).__init__(parent)
        self.value = 0
        self.path_to_csv = ""           
        self.path_to_result = ""        
        self.path_to_model = ""         
        self.name_of_result = ""        
        self.value_predict = ""         
        self.type_of_argument = False   
    def run(self):
        try:
            Predict_value(self.path_to_csv, self.path_to_model,
                          self.path_to_result, self.name_of_result,
                          self.value_predict,
                          self.type_of_argument)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def Predict_value(path_to_csv, path_to_model,
                   output_path, output_file,
                   argument,
                   type_of_argument):
    print(f"-----ПРЕДСКАЗАНИЕ РЕЗУЛЬТАТОВ РАБОТЫ КВУ ПО ЗАДАННЫМ ТТХ-----\n")
    argument_pred = argument + '_pred'
    df = pd.read_csv(path_to_csv, sep=',')
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('(', '')
    df.columns = df.columns.str.replace(')', '')
    df.columns = df.columns.str.replace(chr(8730), '')
    print(f'\n\nКолонки выбранного .csv файла: {df.columns}\n\n')
    try:
        load_model = sm.load(path_to_model)
    except Exception as ex:
        print(f"Ошибка загруженной модели. Не удалось распознать файл {path_to_model}")
        return
    print(f'Параметры модели: \n\n{load_model.params}')
    predicted_values = load_model.predict(df)
    print(f'\nПредсказанные значения: {predicted_values}')
    predict_variable = load_model.predict(df)
    if type_of_argument:
        df[argument_pred] = predict_variable.astype(int)
    else:
        df[argument_pred] = predict_variable
    df.loc[df[argument_pred] < 0, argument_pred] = 0
    print(f'\nКоэффициент детерминации: {load_model.rsquared}\n\n')
    df['RSE'] = (df[argument] - df[argument_pred]) ** 2
    RSEd = df.sum()['RSE']
    RSE = np.sqrt(RSEd / (len(df) - (len(load_model.params) -1) - 1))  
    one_mean = np.mean(df[argument])
    error = RSE / one_mean
    print(f'Стандартное отклонение: {RSE}\nСреднее значение: {one_mean}\nПогрешность: {int(error * 100)}%\n\n')
    print(f'Сводка по модели: \n\n{load_model.summary()}')
    output_file_txt = output_file.rpartition('.')[0]
    if not os.path.exists(output_path):
        create_dir(output_path)
        dst_path = path.join(output_path, output_file_txt)
        dst_path_csv = path.join(output_path, output_file)
    else:
        dst_path = path.join(output_path, output_file_txt)
        dst_path_csv = path.join(output_path, output_file)
        if path.isfile(dst_path):
            cnt_of_files_in_dir = len(listdir(output_path))
            new_name = str(int(cnt_of_files_in_dir / 3) + 1) + '_' + output_file_txt
            dst_path = path.join(output_path, new_name)
        if path.isfile(dst_path_csv):
            cnt_of_files_in_dir = len(listdir(output_path))
            new_name_csv = str(int(cnt_of_files_in_dir / 3) + 1) + '_' + output_file
            dst_path_csv = path.join(output_path, new_name_csv)
    try:
        with open(dst_path, 'w') as file_with_model:
            file_with_model.write(str(load_model.params))
            file_with_model.write(f'\n\nКоэффициент детерминации R2: {load_model.rsquared}')
            file_with_model.write(
                f'\n\nСтандартное отклонение: {RSE}\nСреднее значение: {one_mean}\nПогрешность: {int(error * 100)}%\n\n')
            content = str(load_model.summary())
            file_with_model.write(content)
    except Exception as ex:
        print('Не удалось сохранить некоторые файлы.\n', ex)
    try:
        with open(dst_path_csv, 'a') as file_csv:
            df.to_csv(file_csv, index=False)
    except Exception as ex:
        print('Не удалось сохранить некоторые файлы.\n', ex)
    file_with_model.close()
    file_csv.close()
    print(f"-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")