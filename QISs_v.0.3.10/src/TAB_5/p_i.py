import matplotlib
matplotlib.use('SVG')
from PyQt5.QtCore import QThread
import pandas as pd
import os
from os import path
import statistics

FREQUENCY = " Frequency\n";FREQUENCY_WEIGHT = 99 / 8464
BLOCK_FREQUENCY = " BlockFrequency\n";BLOCK_FREQUENCY_WEIGHT = 95 / 8464
CUMULATIVE_SUMS = " CumulativeSums\n";CUMULATIVE_SUMS_WEIGHT = 85 / 8464
RUNS = " Runs\n";RUNS_WEIGHT = 80 / 8464
LONGEST_RUN = " LongestRun\n";LONGEST_RUN_WEIGHT = 75 / 8464
RANK = " Rank\n";RANK_WEIGHT = 80 / 8464
FFT = " FFT\n";FFT_WEIGHT = 90 / 8464
NON_OVERLAPPING_TEMPLATE = " NonOverlappingTemplate\n";NON_OVERLAPPING_TEMPLATE_WEIGHT = 50 / 8464
OVERLAPPING_TEMPLATE = " OverlappingTemplate\n";OVERLAPPING_TEMPLATE_WEIGHT = 50 / 8464

APPROXIMATE_ENTROPY = " ApproximateEntropy\n";APPROXIMATE_ENTROPY_WEIGHT = 75 / 8464

SERIAL = " Serial\n";SERIAL_WEIGHT = 80 / 8464
LINEAR_COMPLEXITY = " LinearComplexity\n";LINEAR_COMPLEXITY_WEIGHT = 90 / 8464

NAME_OF_RESULT_P_i = 'p_i.txt'
NAME_OF_RESULT_P_i_AVRG = 'p_i_avrg.txt'

class CalcPi(QThread):

    def __init__(self, parent=None):
        super(CalcPi, self).__init__(parent)

        self.value = 0

        self.path_to_reports = ""           
        self.path_to_csv_distination = ""   
        self.name_of_file_csv = ""          

    def run(self):
        print("-----ВЫЧИСЛЕНИЕ P_i-----\n")

        try:
            full_path_to_csv = self.path_to_csv_distination + '/' + self.name_of_file_csv

            calculate_p_i(self.path_to_reports)

            save_all_p_i_in_csv(self.path_to_reports, full_path_to_csv)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def calculate_p_i(path_to_reports):
    p_i = 0

    for dirs, folder, files in os.walk(path_to_reports):

        for file_with_report in files:
            file_path = dirs + '/' + file_with_report

            with open(file_path, 'r', encoding='utf-8') as file:
                while True:
                    line = file.readline()

                    if not line: break

                    line = line.replace('*', ' ')

                    if line.endswith(FREQUENCY):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += FREQUENCY_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(BLOCK_FREQUENCY):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += BLOCK_FREQUENCY_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(CUMULATIVE_SUMS):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += CUMULATIVE_SUMS_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(RUNS):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += RUNS_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(LONGEST_RUN):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += LONGEST_RUN_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(RANK):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += RANK_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(FFT):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += FFT_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(NON_OVERLAPPING_TEMPLATE):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += NON_OVERLAPPING_TEMPLATE_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(OVERLAPPING_TEMPLATE):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += OVERLAPPING_TEMPLATE_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break

                    elif line.endswith(APPROXIMATE_ENTROPY):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += APPROXIMATE_ENTROPY_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break

                    elif line.endswith(SERIAL):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += SERIAL_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                    elif line.endswith(LINEAR_COMPLEXITY):
                        if "0/1" in line:p_i += 0
                        elif "1/1" in line:p_i += LINEAR_COMPLEXITY_WEIGHT
                        else:print("Проведите серию тестов с параметром 'bitstream'=1"); break
                file.close()

                path_p_i = path.join(dirs, NAME_OF_RESULT_P_i)

                f = open(path_p_i, 'a');    f.write(str(p_i) + '\n');   f.close()
                p_i = 0

def save_all_p_i_in_csv(path_to_reports, path_to_csv):
    f = open(path_to_csv, 'a'); f.write("Qubit,p_i");   f.close()

    for dirs, folder, files in os.walk(path_to_reports):
        for file_with_p_i in files:

            if file_with_p_i == NAME_OF_RESULT_P_i:

                file_path = dirs + '/' + file_with_p_i

                file_with_p_i_abs = open(file_path)

                mas_with_p_i = []

                for line in file_with_p_i_abs.readlines():
                    mas_with_p_i.append(float(line))

                file_with_p_i_abs.close()

                path_p_i_avrg = dirs + '/' + NAME_OF_RESULT_P_i_AVRG
                p_i_average = statistics.mean(mas_with_p_i)
                f = open(path_p_i_avrg, 'w');   f.write(str(p_i_average));  f.close()

                str_for_csv = '\n' + dirs.split('/')[-1] + ',' + str(p_i_average)
                f = open(path_to_csv, 'a'); f.write(str_for_csv);   f.close()

    df = pd.read_csv(path_to_csv, delimiter=',')
    df.sort_values("Qubit", axis=0, ascending=True,
                   inplace=True, na_position='first')
    df.to_csv(path_to_csv, ',', index=False)