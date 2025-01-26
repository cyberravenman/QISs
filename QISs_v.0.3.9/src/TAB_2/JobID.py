import os
import pandas as pd
from PyQt5.QtCore import QThread
from qiskit_ibm_runtime import QiskitRuntimeService
import math
from datetime import datetime
from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class CheckJobStatus(QThread):
    def __init__(self, parent=None):
        super(CheckJobStatus, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     

        self.timezone = 0                   

    def run(self):
        try:
            Job_Status(self.token_name, self.ibm_channel, self.jobID, self.timezone)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class JobCancel(QThread):
    def __init__(self, parent=None):
        super(JobCancel, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     

        self.timezone = 0                   

    def run(self):
        try:
            Job_Cancel(self.token_name, self.ibm_channel, self.jobID, self.timezone)
            print(f"\nВыполнение программы '{self.jobID}' отменено.")
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class JobDownload(QThread):
    def __init__(self, parent=None):
        super(JobDownload, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     
        self.alpha = 0.0                    

        self.timezone = 0                   

    def run(self):
        try:
            Job_Download(self.token_name, self.ibm_channel, self.jobID, float(self.alpha), self.timezone)
            print(f"\nСкачивание результатов '{self.jobID}' завершено.")
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Job_Status(token_name, ibm_channel, jobID, time_delta):
    print(f"\n\n-----ПРОВЕРКА СТАТУСА РАБОТЫ [ID: '{jobID}']-----\n")

    service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
    job_check = service.job(jobID)

    print("КВУ: ", str(job_check.backend()).split("\'")[1])
    print("Версия Qiskit: ", job_check.metrics()["qiskit_version"])
    print(f"Выполняется? : {job_check.running()}")
    print(f"Статус выполнения: {job_check.status()}")

    tmp_date = pd.Timestamp(job_check.metrics()["timestamps"]["created"]) + pd.Timedelta(hours=time_delta)
    create_year = tmp_date.strftime("%Y-%m-%d");    create_time = '{:%H:%M:%S}'.format(tmp_date)
    print("Время создания программы:   " + create_year + "  " + create_time)

    if job_check.status() == "INITIALIZING":
        print("\nПРОГРАММА НА СТАДИИ ПРЕДВАРИТЕЛЬНОЙ ИНИЦИАЛИЗАЦИИ.\nОжидайте. ['INITIALIZING']")

    if job_check.status() == "QUEUED":
        print("\nПРОГРАММА НАХОДИТСЯ В ОЧЕРЕДИ. ['QUEUED']")

        tmp_date = job_check.metrics()["estimated_start_time"]
        if tmp_date is None:    print("Оценка завершения работы:     Рассчитывается...")
        else:
            tmp_date = pd.Timestamp(job_check.metrics()["estimated_start_time"]) + pd.Timedelta(hours=time_delta)
            estimate_start_year = tmp_date.strftime("%Y-%m-%d");   estimate_start_time = '{:%H:%M:%S}'.format(tmp_date)
            print("\nОценка времени запуска:     " + estimate_start_year + "  " + estimate_start_time)

            tmp_date = pd.Timestamp(job_check.metrics()["estimated_completion_time"]) + pd.Timedelta(hours=time_delta)
            estimate_complete_time = '{:%H:%M:%S}'.format(tmp_date);  estimate_complete_year = tmp_date.strftime("%Y-%m-%d")
            print("Оценка завершения работы:     " + estimate_complete_year + "  " + estimate_complete_time)

        print("Текущая позиция в очереди:    ", job_check.metrics()["position_in_queue"])
        print("Текущая позиция у провайдера: ", job_check.metrics()["position_in_provider"])

    if job_check.status() == "VALIDATING":
        print("\nПРОГРАММА ПРОХОДИТ ВАЛИДАЦИЮ. ['VALIDATING']\nСкоро отправят на выполнение.")

    if job_check.status() == "RUNNING":
        print("\nПРОГРАММА УСПЕШНО ВЫПОЛНЯЕТСЯ. ['RUNNING']")

    if job_check.status() == "CANCELLED":
        print("\nПРОГРАММА БЫЛА ОТМЕНЕНА. ['CANCELLED']")

    if job_check.status() == "DONE":
        print("\nПРОГРАММА УСПЕШНО ВЫПОЛНЕНА. ['DONE']")

        tmp_date = pd.Timestamp(job_check.metrics()["timestamps"]["running"]) + pd.Timedelta(hours=time_delta)
        running_time = '{:%H:%M:%S}'.format(tmp_date);  running_year = tmp_date.strftime("%Y-%m-%d")
        print("\nВремя фактического запуска: " + running_year + "  " + running_time)

        tmp_date = pd.Timestamp(job_check.metrics()["timestamps"]["finished"]) + pd.Timedelta(hours=time_delta)
        finished_time = '{:%H:%M:%S}'.format(tmp_date);  finished_year = tmp_date.strftime("%Y-%m-%d")
        print("Время завершения работы:     " + finished_year + "  " + finished_time)

        print("\nВремя работы КВУ (сек):      ", job_check.metrics()["usage"]["quantum_seconds"])
        print("Время работы КВУ (кв. сек):  ", job_check.metrics()["usage"]["seconds"])
        print("Время работы КВУ (bss, сек): ", job_check.metrics()["bss"]["seconds"])

        print("\nКоличество запусков (shots): ", job_check.metrics()["executions"])
        print("Количество квантовых схем (circuits): ", job_check.metrics()["num_circuits"])
        print("Количество задействованных кубит: ", job_check.metrics()["num_qubits"])
        print("Глубина квантовой схемы: ", job_check.metrics()["circuit_depths"])

    if job_check.status() == "ERROR":
        print("\nОШИБКА КОМПИЛЯЦИИ/ВЫПОЛНЕНИЯ ПРОГРАММЫ. ['ERROR']")

    print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def Job_Cancel(token_name, ibm_channel, jobID, time_delta):
    print(f"\n-----ОТМЕНА ПРОГРАММЫ [ID: '{jobID}']-----\n")

    try:
        service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
        job_check = service.job(jobID)

        tmp_date = pd.Timestamp(job_check.metrics()["timestamps"]["created"]) + pd.Timedelta(hours=time_delta)
        create_year = tmp_date.strftime("%Y-%m-%d");   create_time = '{:%H:%M:%S}'.format(tmp_date)
        backend_name = str(job_check.backend()).split("\'")[1]
    except Exception as ex: print("\nНеверно введен идентификатор, либо работа была удалена.\n", ex); return

    user_time = datetime.now(); current_time = user_time.strftime("%H:%M:%S");  current_date = date.today()

    try:
        job_check.cancel()

        PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/"
        create_dir(PATH_TO_PROJECT_QIS)
        file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID"
        csv_file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID.csv"
        file_jbid = open(file_path_to_jbID, "a")
        csv_file_jbid = open(csv_file_path_to_jbID, "a")
        jbid_str_0 = "\n----------------------------CANCELLED--------------------------------"
        jbid_str_1 = f"\n[QRNG]\n[CREATED]: {str(create_year)}" + "  " + str(create_time) + "  " + job_check.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_2 = f"[CANCELL]: {str(current_date)}" + "  " + str(current_time) + "  " + job_check.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_3 = "---------------------------------------------------------------------\n\n"
        csv_str_1 = "Project_Type,Status,Date,Time,JobID,Backend,Shots,Alpha"
        csv_str_2 = f"\nQRNG,CANCELLED,{current_date},{current_time},{job_check.job_id()},{backend_name},None,None"
        file_jbid.write(jbid_str_0);    file_jbid.write(jbid_str_1);    file_jbid.write(jbid_str_2);    file_jbid.write(jbid_str_3);    file_jbid.close()
        if os.stat(csv_file_path_to_jbID).st_size == 0:  csv_file_jbid.write(csv_str_1)
        csv_file_jbid.write(csv_str_2); csv_file_jbid.close()

        print("Программа успешно отменена.")
        print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    except Exception as ex: print(ex)
def Job_Download(token_name, ibm_channel, jobID, alpha, time_delta):
    print("\n-----ПОПЫТКА СКАЧАТЬ ДАННЫЕ-----\n")

    service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
    job_res = service.job(jobID)

    if job_res.status() == "DONE":
        res = job_res.result()
        data_pub = res[0].data

        shots = job_res.metrics()["executions"]

        tmp_date = pd.Timestamp(job_res.metrics()["timestamps"]["running"]) + pd.Timedelta(hours=time_delta)
        running_year = tmp_date.strftime("%Y-%m-%d"); running_time = '{:%H:%M:%S}'.format(tmp_date)

        backend_name = str(job_res.backend()).split("\'")[1]

        PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/"
        create_dir(PATH_TO_PROJECT_QIS)

        USR_DIR_NAME_GOOD = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job_res.job_id())}/GOOD"
        USR_DIR_NAME_BAD = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job_res.job_id())}/BAD"
        create_dir(USR_DIR_NAME_GOOD)
        create_dir(USR_DIR_NAME_BAD)

        create_dir(PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + f"STATs_{str(backend_name)}")
        file_name_good_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + f"STATs_{str(backend_name)}" + "/good_qubits_stats"
        file_name_bad_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + f"STATs_{str(backend_name)}" + "/bad_qubits_stats"

        first_str = f"\n          Date    :: {str(running_year)}\n          Time    :: {str(running_time)} \
                    \n          Backend :: {str(backend_name)}\n          JobID   :: {str(job_res.job_id())}\n \
                    \n          Alpha   :: {str(alpha)}\n          Shots   :: {str(shots)}\n\n"
        file_good_q = open(file_name_good_q, "a")
        file_bad_q = open(file_name_bad_q, "a")
        file_good_q.write("\n-----------------------------------------------------------"); file_good_q.write("\n-----------------------------------------------------------")
        file_good_q.write(first_str)
        file_bad_q.write("\n-----------------------------------------------------------");  file_bad_q.write("\n-----------------------------------------------------------")
        file_bad_q.write(first_str)
        file_good_q.close();    file_bad_q.close()

        path_for_stats_counts = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job_res.job_id())}/"
        file_name_cnt_q_good = path_for_stats_counts + "cnt_stats_good"
        file_name_cnt_q_bad = path_for_stats_counts + "cnt_stats_bad"

        file_cnt_q_good = open(file_name_cnt_q_good, "a");  file_cnt_q_bad = open(file_name_cnt_q_bad, "a")
        file_cnt_q_good.write("\n-----------------------------------------------------------"); file_cnt_q_good.write("\n-----------------------------------------------------------")
        file_cnt_q_bad.write("\n-----------------------------------------------------------");  file_cnt_q_bad.write("\n-----------------------------------------------------------")
        file_cnt_q_good.write(first_str);   file_cnt_q_bad.write(first_str)
        file_cnt_q_good.close();    file_cnt_q_bad.close()

        csv_file_name_good_q = path_for_stats_counts + f"good_qubits_stats_{str(job_res.job_id())}.csv"
        csv_file_name_bad_q = path_for_stats_counts + f"bad_qubits_stats_{str(job_res.job_id())}.csv"
        csv_file_name_all_q = path_for_stats_counts + f"ALL_qubits_stats_{str(job_res.job_id())}.csv"
        csv_first_str = "Date,Backend,JobID,Shots,Alpha,Qubit,P_Value,Zero,One,Quality"
        csv_file_cnt_q_good = open(csv_file_name_good_q, "a");  csv_file_cnt_q_bad = open(csv_file_name_bad_q, "a")
        csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
        csv_file_cnt_q_good.write(csv_first_str);   csv_file_cnt_q_bad.write(csv_first_str)
        csv_file_cnt_q_all.write(csv_first_str)
        csv_file_cnt_q_good.close();    csv_file_cnt_q_bad.close(); csv_file_cnt_q_all.close()

        file_name_all_good_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + f"STATs_{str(backend_name)}" + "/_STATS_by_count.csv"
        csv_first_str = "Date,Backend,JobID,Shots,Alpha,cnt_of_GOOD,KEY_good(KB),cnt_of_BAD,KEY_bad(KB),quantum_sec,usage_sec,bss_seq"
        csv_file_cnt_q_all_good = open(file_name_all_good_q, "a")
        if os.stat(file_name_all_good_q).st_size == 0:  csv_file_cnt_q_all_good.write(csv_first_str)
        csv_file_cnt_q_all_good.close()

        ALPHA = alpha

        for exp in data_pub:

            file_name = str(exp).split('c')[1] + "_" + running_time + str(backend_name) + ".txt"

            bitstring = "".join(data_pub[exp].get_bitstrings())

            counts = data_pub[exp].get_counts()

            p_value = calculate_Pvalue(bitstring)

            try:    counts_zero = counts["0"]
            except Exception as ex: counts_zero = 0

            try:    counts_unity = counts["1"]
            except Exception as ex: counts_unity = 0

            if float(p_value) >= ALPHA:

                file_good_q = open(file_name_good_q, "a");  file_cnt_q_good = open(file_name_cnt_q_good, "a")

                csv_file_cnt_q_good = open(csv_file_name_good_q, "a")

                dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + str(exp).split('c')[1])
                good_q_str = str(exp).split('c')[1] + " "  
                file_good_q.write(good_q_str);  file_cnt_q_good.write(f"Кубит {good_q_str}:: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                csv_file_cnt_q_good.write(f"\n{running_year},{backend_name},{job_res.job_id()},"
                                          f"{shots},{alpha},{exp.split('c')[1]},"
                                          f"{p_value},{counts_zero},{counts_unity},1")
                file_good_q.close();    file_cnt_q_good.close();    csv_file_cnt_q_good.close()

                csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
                csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job_res.job_id()},"
                                         f"{shots},{alpha},{exp.split('c')[1]},"
                                         f"{p_value},{counts_zero},{counts_unity},1")
                csv_file_cnt_q_all.close()
            else:

                file_bad_q = open(file_name_bad_q, "a");  file_cnt_q_bad = open(file_name_cnt_q_bad, "a")

                csv_file_cnt_q_bad = open(csv_file_name_bad_q, "a")

                dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + str(exp).split('c')[1])
                bad_q_str = str(exp).split('c')[1] + " "  

                file_bad_q.write(bad_q_str);    file_cnt_q_bad.write(f"Кубит {bad_q_str}:: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                csv_file_cnt_q_bad.write(f"\n{running_year},{backend_name},{job_res.job_id()},"
                                         f"{shots},{alpha},{exp.split('c')[1]},"
                                         f"{p_value},{counts_zero},{counts_unity},0")
                file_bad_q.close(); file_cnt_q_bad.close(); csv_file_cnt_q_bad.close()

                csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
                csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job_res.job_id()},"
                                         f"{shots},{alpha},{exp.split('c')[1]},"
                                         f"{p_value},{counts_zero},{counts_unity},0")
                csv_file_cnt_q_all.close()

            create_dir(dir_path)  

            path = os.path.join(dir_path, file_name)

            file_for_bitmap = os.path.join(dir_path, str(exp).split('c')[1] + "_" + running_time + str(backend_name) + ".png")
            bitmap_of_sequence(bitstring, file_for_bitmap)

            with open(path, "w") as fd:
                fd.write(bitstring)
            fd.close()  
            print(f"\n[+]: Данные записаны в файл: '{file_name}'")

            print(f"[+]: '0' [{counts_zero}]")
            print(f"[+]: '1' [{counts_unity}]")
            print("[+]: p_value: ", p_value)

        path_to_all_qubits = PATH_TO_PROJECT_QIS + "QRNG/QPU_Downloaded/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job_res.job_id())}"
        good_qubits_cnt = concatenation_files(path_to_all_qubits, 1)
        bad_qubits_cnt = concatenation_files(path_to_all_qubits, 0)

        print("\nКоличество устойчивых кубит:   ", good_qubits_cnt)
        file_good_q = open(file_name_good_q, "a"); file_cnt_q_good = open(file_name_cnt_q_good, "a")
        total_good_q = "\n\n:: " + f"[TOTAL: {good_qubits_cnt}]" + " ::\n\n"
        file_good_q.write(total_good_q); file_cnt_q_good.write(total_good_q)
        file_good_q.close();    file_cnt_q_good.close()

        print("Количество ненадежных кубит: ", bad_qubits_cnt)
        file_bad_q = open(file_name_bad_q, "a");    file_cnt_q_bad = open(file_name_cnt_q_bad, "a")
        total_bad_q = "\n\n:: " + f"[TOTAL: {bad_qubits_cnt}]" + " ::\n\n"
        file_bad_q.write(total_bad_q);  file_cnt_q_bad.write(total_bad_q)
        file_bad_q.close(); file_cnt_q_bad.close()

        csv_file_cnt_q_all_good = open(file_name_all_good_q, "a")
        qnt_seq = job_res.metrics()["usage"]["quantum_seconds"]
        usg_seq = job_res.metrics()["usage"]["seconds"]
        bss_seq = job_res.metrics()["bss"]["seconds"]
        len_KEY_good_KB = good_qubits_cnt * shots / 8 / 1000
        len_KEY_bad_KB = bad_qubits_cnt * shots / 8 / 1000
        csv_file_cnt_q_all_good.write(f"\n{running_year},{backend_name},{job_res.job_id()},"
                                         f"{shots},{alpha},{good_qubits_cnt},{round(len_KEY_good_KB, 3)},"
                                      f"{bad_qubits_cnt},{round(len_KEY_bad_KB, 3)},{qnt_seq},{usg_seq},{bss_seq}")
        csv_file_cnt_q_all_good.close()

        print("\nTime of QPU: ", qnt_seq)
        print("Time of usage: ", usg_seq)
        print("Final KEY length, (KB): ", len_KEY_good_KB)

    else:
        print("\nУбедитесь, что статус выполнения программы : 'DONE'.")

    print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def create_dir(dir_name):
    dir_path = os.path.join(dir_name)
    try:
        os.makedirs(dir_path)
    except OSError:
        pass  

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

def concatenation_files(path_to_qubits, good_or_bad):

    if good_or_bad == 1:
        DIRECTORY = path_to_qubits + "/_FINAL_KEY_GOOD/"
        path_to_qubits = path_to_qubits + "/GOOD"
    else:
        DIRECTORY = path_to_qubits + "/_FINAL_KEY_BAD/"
        path_to_qubits = path_to_qubits + "/BAD"

    txt_files = list(Path(path_to_qubits).rglob("*.[tT][xX][tT]"))

    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    else:

        pass

    file_with_key = DIRECTORY + '/KEY.txt'

    with open(file_with_key, 'w+') as outfile:
        for file_name in txt_files:
            with open(file_name) as infile:
                outfile.write(infile.read())

    key_sequence = []

    with open(file_with_key, 'r', encoding='utf-8') as file:
        while True:
            bit1 = file.read(1)
            if not bit1:
                break
            if bit1.isdigit():
                key_sequence.append(int(bit1))
    bitmap_of_sequence(key_sequence, DIRECTORY + '/KEY.png')

    return len(txt_files)

def bitmap_of_sequence(random_sequence, name_of_bitmap):
    sequence = [];  len_of_sequence = len(random_sequence)

    if len_of_sequence == 0:    return

    for i in range(0, len_of_sequence):
        sequence.append(int(random_sequence[i]))

    len_of_sequence = len(sequence)
    if len_of_sequence > 2 ** 20:
        len_of_sequence = 1024 ** 2;    x_axis = 1024;  y_axis = 1024
    else:
        len_of_sequence = math.floor(math.sqrt(len_of_sequence))
        x_axis = len_of_sequence;   y_axis = len_of_sequence;   len_of_sequence = len_of_sequence ** 2

    sequence_slice = sequence[0:len_of_sequence]

    plt.imsave(name_of_bitmap, np.array(sequence_slice).reshape(x_axis, y_axis), cmap=cm.gray)

    plt.clf()