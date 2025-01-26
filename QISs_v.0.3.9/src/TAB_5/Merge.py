from src.TAB_2.QRNG import create_dir
import matplotlib
matplotlib.use('SVG')
from PyQt5.QtCore import QThread
import pandas as pd
import os
from os import path, listdir
import shutil
from pathlib import Path
from PyQt5.QtCore import Qt

class MergeFileSequences(QThread):

    def __init__(self, parent=None):
        super(MergeFileSequences, self).__init__(parent)

        self.value = 0

        self.path_for_sequences = ""        
        self.path_for_distination = ""      
        self.save_in_common_folder = False  

        self.Seq_BAD = True                 
        self.Seq_GOOD = False               
        self.Seq_ALL = False                
        self.Seq_USER = -1                   

    def run(self):
        print("-----ОБЪЕДИНЕНИЕ ФАЙЛОВ ЭКСПЕРИМЕНТОВ СП-----\n")

        if self.Seq_USER != -1:
            name_of_seq = self.Seq_USER
        else:
            if self.Seq_BAD:    name_of_seq = "BAD"
            elif self.Seq_GOOD: name_of_seq = "GOOD"
            else:   name_of_seq = "ALL"

        try:
            merge_files_with_seq(self.path_for_sequences, self.path_for_distination,
                                 self.save_in_common_folder,
                                 name_of_seq)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class MergeFileReportsNIST(QThread):

    def __init__(self, parent=None):
        super(MergeFileReportsNIST, self).__init__(parent)

        self.value = 0

        self.path_to_reports = ""           
        self.path_for_distination = ""      
        self.save_in_common_folder = False  

        self.report_name = ""               

    def run(self):
        print("-----ОБЪЕДИНЕНИЕ ФАЙЛОВ NIST ОТЧЕТОВ-----\n")

        try:
            merge_files_with_report(self.path_to_reports, self.path_for_distination, self.report_name, self.save_in_common_folder)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class MergeCsv(QThread):

    def __init__(self, parent=None):
        super(MergeCsv, self).__init__(parent)

        self.value = 0

        self.list_widget_csv_1 = None  
        self.list_widget_csv_2 = None  

        self.csv_path_1 = ""        
        self.csv_path_2 = ""        
        self.csv_output_path = ""   
        self.csv_output_name = ""   

        self.parameter_on = ""      
        self.parameter_how = ""   
        self.parameter_index = ""   

    def run(self):
        print("-----ОБЪЕДИНЕНИЕ ФАЙЛОВ .csv-----\n")

        csv_columns_1 = []; csv_columns_2 = []

        for index in range(self.list_widget_csv_1.count()):

            if self.list_widget_csv_1.item(index).checkState() == Qt.Checked:
                csv_columns_1.append(index)  
        for index in range(self.list_widget_csv_2.count()):

            if self.list_widget_csv_2.item(index).checkState() == Qt.Checked:
                csv_columns_2.append(index)  

        try:
            pass
            merge_csv(self.csv_path_1, self.csv_path_2, self.csv_output_path, self.csv_output_name,
                      csv_columns_1, csv_columns_2,
                      self.parameter_on, self.parameter_how, self.parameter_index)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def merge_files_with_seq(path_for_sequences, path_for_distination,
                         save_in_common_folder,
                         name_of_seq):

    DIR_OF_QISs = os.getcwd()

    if not save_in_common_folder:

        if not os.path.exists(path_for_distination):
            create_dir(path_for_distination)

        else:
            tmp = Path(path_for_distination).parent                         
            l = len(next(os.walk(tmp))[1])                                  
            path_for_distination = path_for_distination + '_' + str(l + 1)  
            create_dir(path_for_distination)                                
    else:
        tmp = Path(path_for_distination).parent  
        path_for_distination = str(tmp) + '/' + 'common'

    for dirs, folder, files in os.walk(path_for_sequences):

        os.chdir(dirs)

        current_dir = os.path.split(os.getcwd())

        if name_of_seq != "ALL":

            if current_dir[1] == str(name_of_seq):

                for dirs2, folder2, files2 in os.walk(os.getcwd()):

                    for file_with_seq in files2:

                        file_path = dirs2 + '/' + file_with_seq

                        if file_with_seq.endswith(".txt") and os.stat(file_path).st_size != 0:

                            dst_path = path_for_distination + '/' + dirs2.split('/')[-1]
                            create_dir(dst_path)

                            shutil.copy2(file_path, dst_path)
        else:

            if (current_dir[1] == "GOOD") or (current_dir[1] == "BAD"):

                for dirs2, folder2, files2 in os.walk(os.getcwd()):

                    for file_with_seq in files2:

                        file_path = dirs2 + '/' + file_with_seq

                        if file_with_seq.endswith(".txt") and os.stat(file_path).st_size != 0:

                            dst_path = path_for_distination + '/' + dirs2.split('/')[-1]
                            create_dir(dst_path)

                            shutil.copy2(file_path, dst_path)

    os.chdir(DIR_OF_QISs)

def merge_files_with_report(path_to_reports, distination_path, name, save_to_one_place):

    if not save_to_one_place:

        if not os.path.exists(distination_path):
            create_dir(distination_path)

        else:
            tmp = Path(distination_path).parent  
            l = len(next(os.walk(tmp))[1])  
            distination_path = distination_path + '_' + str(l + 1)  
            create_dir(distination_path)  
    else:
        tmp = Path(distination_path).parent  
        distination_path = str(tmp) + '/' + 'common'

    for dirs, folder, files in os.walk(path_to_reports):

        for file_with_report in files:
            if file_with_report == name:

                file_path = dirs + '/' + file_with_report

                dst_path = distination_path + '/' + dirs.split('/')[-2]

                create_dir(dst_path)

                copypath = path.join(dst_path, name)
                if path.isfile(copypath):
                    new_name = str(len(listdir(dst_path)) + 1) + '_' + name
                    copypath = path.join(dst_path, new_name)

                shutil.copy2(file_path, copypath)

def merge_csv(csv_path_1, csv_path_2, csv_output_path, csv_output_name,
              csv_columns_1, csv_columns_2,
              parameter_on, parameter_how, parameter_index):

    if not os.path.exists(csv_output_path):
        create_dir(csv_output_path)
    csv_output = csv_output_path + '/' + csv_output_name

    if (len(csv_columns_2) == 0) and (len(csv_columns_1) == 0):
        print("Выберите csv файл(ы).")
    elif len(csv_columns_1) == 0:

        df2 = pd.read_csv(csv_path_2, usecols=csv_columns_2)

        if parameter_index == "False":
            df2.to_csv(csv_output, index=False)  
        elif parameter_index == "True":
            df2.to_csv(csv_output, index=True)  
    elif len(csv_columns_2) == 0:

        df = pd.read_csv(csv_path_1, usecols=csv_columns_1)

        if parameter_index == "False":
            df.to_csv(csv_output, index=False)  
        elif parameter_index == "True":
            df.to_csv(csv_output, index=True)  
    else:

        df = pd.read_csv(csv_path_1, usecols=csv_columns_1)
        df2 = pd.read_csv(csv_path_2, usecols=csv_columns_2)

        if parameter_how == "outer":
            result = pd.merge(df, df2, how=parameter_how)  

            sorted_result = result.sort_values(by=[parameter_on], ascending=True)

            if parameter_index == "False":
                sorted_result.to_csv(csv_output, index=False)  
            elif parameter_index == "True":
                sorted_result.to_csv(csv_output, index=True)  
        elif parameter_how == "inner":
            result = pd.merge(df, df2, on=parameter_on, how=parameter_how)  

            if parameter_index == "False":
                result.to_csv(csv_output, index=False)  
            elif parameter_index == "True":
                result.to_csv(csv_output, index=True)