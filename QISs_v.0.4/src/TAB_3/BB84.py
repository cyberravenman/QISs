import re
from datetime import datetime
import pandas as pd
from pathlib import Path
import pathlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from PyQt5.QtCore import QThread
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from PyQt5.QtCore import Qt
import os
import math
from PyQt5 import QtWidgets, QtCore
from src.TAB_0.QPU_Info import set_Num_of_Qubits
class QKDBB84Start(QThread):
    def __init__(self, parent=None):
        super(QKDBB84Start, self).__init__(parent)
        self.value = 0
        self.token_name = ""        
        self.backend_name = ""      
        self.ibm_channel = ""       
        self.alpha = 0.0            
        self.shots = 0              
        self.opt_level = 0          
        self.timezone = 0           
        self.use_barriers = False   
        self.num_of_qubits_max = 0  
        self.file_config = ""       
        self.flag_eve = False       
    def run(self):
        if self.file_config == "":  return
        try:
            print(f"\n--------ККС ВРК ВВ84 '{self.backend_name}'--------\n")
            QKD_BB84(self.token_name, self.ibm_channel, self.backend_name,
                      self.shots, self.alpha, self.opt_level,
                      self.use_barriers, self.timezone, self.num_of_qubits_max,
                      self.file_config, self.flag_eve)
            print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
        except Exception as ex: print(f'Возникло исключение: {ex}')
def QKD_BB84(user_token, ibm_channel, backend_name,
             shots, alpha, opt_level,
             bool_barriers, time_delta, num_of_qubits,
             file_config, flag_eve):
    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)
    print(f"Присутствует нарушитель в Канале связи? :: {flag_eve}")
    USER_QPU = backend_name
    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    NUM_OF_QUBITS_ON_QPU = num_of_qubits
    list_dir_name_of_seq = []
    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')
    reg_c = []
    reg_measure = []
    had_Alc_1_list = []; had_Alc_2_list = []; had_Bob_1_list = []; had_Eve_1_list = []; qub_Alc_list = [];   qub_Bob_list = [];   qub_Eve_list = []
    with open(file_config, "r") as fp:
        lines = fp.readlines(); len_of_config_file = len(lines)
        for i in range(0, len_of_config_file):
            had_Alc_1 = "";    had_Alc_2 = "";    had_Bob_1 = "";    had_Eve_1 = "";    qub_Alc = "";  qub_Bob = "";  qub_Eve = ""
            try:
                had_Alc_1 = re.split("=|:", lines[i])[1]
                if lines[i].endswith('\n'):
                    for j in range(0, len(lines[i].strip('\n')) - 1)[::-1]:
                        symb = str(lines[i][j])
                        if symb.isdigit():  pass
                        else:
                            if str(lines[i].strip('\n')[-1]).isdigit(): last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                            else:   last_number_in_str = int((lines[i])[j + 1:-2].strip('\n')); break
                else:
                    for j in range(0, len(lines[i]) - 1)[::-1]:
                        symb = str(lines[i][j])
                        if symb.isdigit():  pass
                        else:   last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                if flag_eve:
                    if had_Alc_1 != str(last_number_in_str):
                        had_Alc_2 = re.split(":|;", lines[i])[1]
                        if had_Alc_2 != str(last_number_in_str):
                            had_Bob_1 = re.split(";|!", lines[i])[1]
                            if had_Bob_1 != str(last_number_in_str):
                                had_Eve_1 = re.split("!|\+", lines[i])[1]
                                if had_Eve_1 != str(last_number_in_str):
                                    qub_Alc = re.split("\+|/", lines[i])[1]
                                    if qub_Alc != str(last_number_in_str):
                                        qub_Bob = re.split("/|\*", lines[i])[1]
                                        if qub_Bob != str(last_number_in_str):
                                            qub_Eve = lines[i].split('*')[1].strip('\n')
                else:
                    if had_Alc_1 != str(last_number_in_str):
                        had_Alc_2 = re.split(":|;", lines[i])[1]
                        if had_Alc_2 != str(last_number_in_str):
                            had_Bob_1 = re.split(";|!", lines[i])[1]
                            if had_Bob_1 != str(last_number_in_str):
                                qub_Alc = re.split("\+|/", lines[i])[1]
                                if qub_Alc != str(last_number_in_str):
                                    qub_Bob = re.split("/|\*", lines[i])[1]
            except Exception as ex: print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
            if had_Alc_1 != "":
                reg_c.append(ClassicalRegister(1, f'c{had_Alc_1}'));    had_Alc_1_list.append(int(had_Alc_1));  reg_measure.append(int(had_Alc_1))
            else:   print("Не удалось идентифицировать все поля had_Alc_1. Проверьте конфигурационный файл");    return
            if had_Alc_2 != "":
                reg_c.append(ClassicalRegister(1, f'c{had_Alc_2}'));    had_Alc_2_list.append(int(had_Alc_2));  reg_measure.append(int(had_Alc_2))
            else:   print("Не удалось идентифицировать все поля had_Alc_2. Проверьте конфигурационный файл");    return
            if had_Bob_1 != "":
                reg_c.append(ClassicalRegister(1, f'c{had_Bob_1}'));    had_Bob_1_list.append(int(had_Bob_1));  reg_measure.append(int(had_Bob_1))
            else:   print("Не удалось идентифицировать все поля had_Bob_1. Проверьте конфигурационный файл");    return
            if (had_Eve_1 != "") & (flag_eve == True):
                reg_c.append(ClassicalRegister(1, f'c{had_Eve_1}'));    had_Eve_1_list.append(int(had_Eve_1));  reg_measure.append(int(had_Eve_1))
            else:
                if flag_eve:    print("Не удалось идентифицировать все поля had_Eve_1. Проверьте конфигурационный файл");    return
            if qub_Alc != "":
                reg_c.append(ClassicalRegister(1, f'c{qub_Alc}'));  qub_Alc_list.append(int(qub_Alc));  reg_measure.append(int(qub_Alc))
            else:   print("Не удалось идентифицировать все поля qub_Alc. Проверьте конфигурационный файл");    return
            if (qub_Eve != "") & (flag_eve == True):
                reg_c.append(ClassicalRegister(1, f'c{qub_Eve}'));  qub_Eve_list.append(int(qub_Eve));  reg_measure.append(int(qub_Eve))
            else:
                if flag_eve:    print("Не удалось идентифицировать все поля qub_Eve. Проверьте конфигурационный файл");    return
            if qub_Bob != "":
                reg_c.append(ClassicalRegister(1, f'c{qub_Bob}'));  qub_Bob_list.append(int(qub_Bob));  reg_measure.append(int(qub_Bob))
            else:   print("Не удалось идентифицировать все поля qub_Bob. Проверьте конфигурационный файл");    return
    USER_QUBITS_AND_CLBITS = len(reg_measure)
    circuit = QuantumCircuit(reg_q, *reg_c)
    for i in range(0, NUM_OF_QUBITS_ON_QPU):
        for j in range(0, len(had_Alc_1_list)):
            if (i == had_Alc_1_list[j]) & (flag_eve == True):
                circuit.reset(reg_q[i])
                circuit.h(reg_q[i])
                circuit.measure(reg_q[i], reg_c[j*7]);  print(f"\n\nALC_HAD_1 : {reg_q[i]} -- MEASURE : {reg_c[j*7]}")
                index_Alc_2 = int(had_Alc_2_list[j])
                circuit.reset(reg_q[index_Alc_2])
                circuit.h(reg_q[index_Alc_2])
                circuit.measure(reg_q[index_Alc_2], reg_c[j*7+1]);  print(f"ALC_HAD_2 : {reg_q[index_Alc_2]} -- MEASURE : {reg_c[j*7+1]}")
                index_Bob_1 = int(had_Bob_1_list[j])
                circuit.reset(reg_q[index_Bob_1])
                circuit.h(reg_q[index_Bob_1])
                circuit.measure(reg_q[index_Bob_1], reg_c[j*7+2]);  print(f"BOB_HAD_1 : {reg_q[index_Bob_1]} -- MEASURE : {reg_c[j*7+2]}")
                index_Eve_1 = int(had_Eve_1_list[j])
                circuit.reset(reg_q[index_Eve_1])
                circuit.h(reg_q[index_Eve_1])
                circuit.measure(reg_q[index_Eve_1], reg_c[j*7+3]);  print(f"EVE_HAD_1 : {reg_q[index_Eve_1]} -- MEASURE : {reg_c[j*7+3]}")
                index_Alice_qub = int(qub_Alc_list[j])
                circuit.reset(reg_q[index_Alice_qub]);  print(f"QUB_ALC : {reg_q[index_Alice_qub]} -- MEASURE : {reg_c[j*7+4]}")
                circuit.x(reg_q[index_Alice_qub]).c_if(reg_c[j*7], 1)
                circuit.h(reg_q[index_Alice_qub]).c_if(reg_c[j*7+1], 1)
                index_Eve_qub = int(qub_Eve_list[j])
                circuit.swap(reg_q[index_Alice_qub], reg_q[index_Eve_qub])
                circuit.barrier(*reg_q)
                circuit.h(reg_q[index_Eve_qub]).c_if(reg_c[j*7+3], 1)
                circuit.measure(reg_q[index_Eve_qub], reg_c[j*7+5]);    print(f"QUB_EVE : {reg_q[index_Eve_qub]} -- MEASURE : {reg_c[j*7+5]}")
                circuit.reset(reg_q[index_Eve_qub])
                circuit.x(reg_q[index_Eve_qub]).c_if(reg_c[j*7+5], 1)
                circuit.h(reg_q[index_Eve_qub]).c_if(reg_c[j*7+3], 1)
                index_Bob_qub = int(qub_Bob_list[j])
                circuit.swap(reg_q[index_Eve_qub], reg_q[index_Bob_qub])
                circuit.barrier(*reg_q)
                circuit.h(reg_q[index_Bob_qub]).c_if(reg_c[j*7+2], 1)
                circuit.measure(reg_q[index_Bob_qub], reg_c[j*7+6])
                print(f"QUB_BOB : {reg_q[index_Bob_qub]} -- MEASURE : {reg_c[j*7+6]}")
                if bool_barriers:   circuit.barrier(*reg_q)
                break
            elif (i == had_Alc_1_list[j]) & (flag_eve == False):
                circuit.reset(reg_q[i])
                circuit.h(reg_q[i])
                circuit.measure(reg_q[i], reg_c[j*5]);  print(f"\n\nALC_HAD_1 : {reg_q[i]} -- MEASURE : {reg_c[j*5]}")
                index_Alc_2 = int(had_Alc_2_list[j])
                circuit.reset(reg_q[index_Alc_2])
                circuit.h(reg_q[index_Alc_2])
                circuit.measure(reg_q[index_Alc_2], reg_c[j*5+1]);  print(f"ALC_HAD_2 : {reg_q[index_Alc_2]} -- MEASURE : {reg_c[j*5+1]}")
                index_Bob_1 = int(had_Bob_1_list[j])
                circuit.reset(reg_q[index_Bob_1])
                circuit.h(reg_q[index_Bob_1])
                circuit.measure(reg_q[index_Bob_1], reg_c[j*5+2]);  print(f"BOB_HAD_1 : {reg_q[index_Bob_1]} -- MEASURE : {reg_c[j*5+2]}")
                index_Alice_qub = int(qub_Alc_list[j])
                circuit.reset(reg_q[index_Alice_qub])
                print(f"QUB_ALC : {reg_q[index_Alice_qub]} -- MEASURE : {reg_c[j*5+3]}")
                circuit.x(reg_q[index_Alice_qub]).c_if(reg_c[j*5], 1)
                circuit.h(reg_q[index_Alice_qub]).c_if(reg_c[j*5+1], 1)
                index_Bob_qub = int(qub_Bob_list[j])
                circuit.swap(reg_q[index_Alice_qub], reg_q[index_Bob_qub])
                print(f"QUB_BOB : {reg_q[index_Bob_qub]} -- MEASURE : {reg_c[j*5+4]}")
                circuit.barrier(*reg_q)
                circuit.h(reg_q[index_Bob_qub]).c_if(reg_c[j*5+2], 1)
                circuit.measure(reg_q[index_Bob_qub], reg_c[j*5+4])
                if bool_barriers:   circuit.barrier(*reg_q)
                break
    print("\n\n")
    machine_name = USER_QPU
    backend = service.least_busy(operational=True, simulator=False, name=machine_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)
    with Session(backend=backend) as session:
        sampler = Sampler(session, options={"default_shots": USER_SHOTS})
        job = sampler.run([isa_circuit])
        print(f"\n[+]: Идентификатор Job_ID: {job.job_id()}")
        tmp_date = pd.Timestamp(job.metrics()["timestamps"]["created"]) + pd.Timedelta(hours=time_delta)
        create_year = tmp_date.strftime("%Y-%m-%d");    create_time = '{:%H:%M:%S}'.format(tmp_date)
        tmp_date_finish = job.metrics()["estimated_start_time"]
        while tmp_date_finish == None:   tmp_date_finish = job.metrics()["estimated_start_time"]
        tmp_date = pd.Timestamp(job.metrics()["estimated_start_time"]) + pd.Timedelta(hours=time_delta)
        estimate_start_year = tmp_date.strftime("%Y-%m-%d");    estimate_start_time = '{:%H:%M:%S}'.format(tmp_date)
        print("\nОценка времени запуска:     " + estimate_start_year + "  " + estimate_start_time)
        print("Текущая позиция в очереди:    ", job.metrics()["position_in_queue"])
        print("Текущая позиция у провайдера: ", job.metrics()["position_in_provider"])
        PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/"
        create_dir(PATH_TO_PROJECT_QIS)
        file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID"
        csv_file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID.csv"
        file_jbid = open(file_path_to_jbID, "a")
        csv_file_jbid = open(csv_file_path_to_jbID, "a")
        jbid_str_1 = f"\n[QKD_BB84]\n[CREATED]: {str(create_year)}" + "  " + str(create_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_2 = f"[STARTED]: {str(estimate_start_year)}" + "  " + str(estimate_start_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_3 = f"[SHOTS]:   {shots}\n[ALPHA]:   {alpha}\n\n"
        csv_str_1 = "Project_Type,Status,Date,Time,JobID,Backend,Shots,Alpha"
        csv_str_2 = f"\nQKD_BB84,CREATED,{create_year},{create_time},{job.job_id()},{backend_name},{shots},{alpha}"
        file_jbid.write(jbid_str_1);    file_jbid.write(jbid_str_2);    file_jbid.write(jbid_str_3);    file_jbid.close()
        if os.stat(csv_file_path_to_jbID).st_size == 0:  csv_file_jbid.write(csv_str_1)
        csv_file_jbid.write(csv_str_2); csv_file_jbid.close()
        res = job.result()
        data_pub = res[0].data
        for i in range(0, USER_QUBITS_AND_CLBITS):
            now = datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S")
            tmp_date = pd.Timestamp(job.metrics()["timestamps"]["running"]) + pd.Timedelta(hours=time_delta)
            running_year = tmp_date.strftime("%Y-%m-%d");   running_time = '{:%H:%M:%S}'.format(tmp_date)
            if flag_eve:    num_of_exp = i // 7;    eva_spy = "Alice_Eva_Bob"
            else:   num_of_exp = i // 5;    eva_spy = "Alice_Bob"
            USR_DIR_NAME = PATH_TO_PROJECT_QIS + "QKD/BB84/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{eva_spy}/{shots}_{alpha}_{str(job.job_id())}" + f"/BB84_{num_of_exp}"
            create_dir(USR_DIR_NAME)
            if i == 0:
                path_for_stats_counts = PATH_TO_PROJECT_QIS + "QKD/BB84/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{eva_spy}/{shots}_{alpha}_{str(job.job_id())}/"
                csv_file_name_all_q = path_for_stats_counts + f"ALL_qubits_stats_{str(job.job_id())}.csv"
                csv_first_str = "Date,Backend,JobID,Shots,Alpha,Qubit,Meaning,P_Value,Zero,One,Quality,Divergence"
                csv_file_cnt_q_all = open(csv_file_name_all_q, "a");    csv_file_cnt_q_all.write(csv_first_str);    csv_file_cnt_q_all.close()
            index = int(reg_measure[i])
            file_name = f'{index}_' + time + "_" + machine_name + ".txt"
            bitstring = "".join(getattr(data_pub, f'c{index}').get_bitstrings())
            counts = getattr(data_pub, f'c{index}').get_counts()
            p_value = calculate_Pvalue(bitstring)
            quality_of_seq = 0
            if float(p_value) >= ALPHA:    quality_of_seq = 1
            try:    counts_zero = counts["0"]
            except Exception as ex: counts_zero = 0
            try:    counts_unity = counts["1"]
            except Exception as ex: counts_unity = 0
            path = os.path.join(USR_DIR_NAME, file_name)  
            with open(path, 'w') as fd: fd.write(bitstring)
            fd.close()  
            file_for_bitmap = os.path.join(USR_DIR_NAME + '/', f'{index}_' + time + "_" + machine_name + ".png")
            bitmap_of_sequence(bitstring, file_for_bitmap)
            divergence = "NaN"
            meaning = ""
            if flag_eve:
                for item in had_Alc_1_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "ALC_1_had";  break
                for item in had_Alc_2_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "ALC_2_had";  break
                for item in had_Bob_1_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "BOB_1_had";  break
                for item in had_Eve_1_list:
                    if int(item) == index:  meaning = "EVE_1_had";  break
                for item in qub_Alc_list:
                    if int(item) == index:  meaning = "ALC_qub";    break
                for item in qub_Eve_list:
                    if int(item) == index:  meaning = "EVE_qub";    break
                for item in qub_Bob_list:
                    if int(item) == index:
                        meaning = "BOB_qub"
                        list_dir_name_of_seq.append(path)
                        divergence = Clear_sequences_by_basis(list_dir_name_of_seq[0], list_dir_name_of_seq[1],
                                                              list_dir_name_of_seq[2], list_dir_name_of_seq[3],
                                                              USR_DIR_NAME, csv_file_name_all_q, ALPHA,
                                                              running_year, backend_name, job.job_id(), shots)
                        list_dir_name_of_seq = []
                        break
            else:
                for item in had_Alc_1_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "ALC_1_had";  break
                for item in had_Alc_2_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "ALC_2_had";  break
                for item in had_Bob_1_list:
                    if int(item) == index:  list_dir_name_of_seq.append(path);  meaning = "BOB_1_had";  break
                for item in qub_Alc_list:
                    if int(item) == index:  meaning = "ALC_qub";    break
                for item in qub_Bob_list:
                    if int(item) == index:
                        meaning = "BOB_qub"
                        list_dir_name_of_seq.append(path)
                        divergence = Clear_sequences_by_basis(list_dir_name_of_seq[0], list_dir_name_of_seq[1],
                                                              list_dir_name_of_seq[2], list_dir_name_of_seq[3],
                                                              USR_DIR_NAME, csv_file_name_all_q, ALPHA,
                                                              running_year, backend_name, job.job_id(), shots)
                        list_dir_name_of_seq = []
                        break
            csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
            csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                     f"{shots},{alpha},{str(reg_measure[i])},{meaning},"
                                     f"{p_value},{counts_zero},{counts_unity},{str(quality_of_seq)},{divergence}")
            csv_file_cnt_q_all.close()
            print(f"\n[+]: Данные записаны в файл: '{file_name}'"); print(f"[+]: '0' [{counts_zero}]"); print(f"[+]: '1' [{counts_unity}]")
        df = pd.read_csv(csv_file_name_all_q);  df['Divergence'].fillna(method='backfill', inplace=True);   df.to_csv(csv_file_name_all_q)
        qnt_seq = job.metrics()["usage"]["quantum_seconds"];    usg_seq = job.metrics()["usage"]["seconds"]
        print("\nTime of QPU: ", qnt_seq);  print("Time of usage: ", usg_seq)
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
def Clear_sequences_by_basis(file1, file2, file3, file4, path_to_result, csv_path, alpha,
                             year, backend, job_id, shots):
    bit_string_1 = ""  
    bit_string_2 = ""  
    bit_string_3 = ""  
    bit_string_4 = ""  
    with open(file1, 'r', encoding='utf-8') as file_1:
        while True:
            bit1 = file_1.read(1)
            if not bit1:    break
            if bit1.isdigit():  bit_string_1 += str(bit1)
    file_1.close()
    with open(file2, 'r', encoding='utf-8') as file_2:
        while True:
            bit2 = file_2.read(1)
            if not bit2:    break
            if bit2.isdigit():  bit_string_2 += str(bit2)
    file_2.close()
    with open(file3, 'r', encoding='utf-8') as file_3:
        while True:
            bit3 = file_3.read(1)
            if not bit3:    break
            if bit3.isdigit():  bit_string_3 += str(bit3)
    file_3.close()
    with open(file4, 'r', encoding='utf-8') as file_4:
        while True:
            bit4 = file_4.read(1)
            if not bit4:    break
            if bit4.isdigit():  bit_string_4 += str(bit4)
    file_4.close()
    lst_not_common = []  
    bit_substring_1 = bit_string_1[0:10];   print(f"\nINIT Alice     :: {bit_substring_1}")
    bit_substring_2 = bit_string_2[0:10];   print(f"Hadamard Alice :: {bit_substring_2}")
    bit_substring_3 = bit_string_3[0:10];   print(f"Hadamard Bob   :: {bit_substring_3}")
    bit_substring_4 = bit_string_4[0:10];   print(f"Result Bob     :: {bit_substring_4}\n")
    print(f"\nlen_of_bitstring :: {len(bit_string_2)}\n")
    for k in range(0, len(bit_string_2)):
        if bit_string_2[k] != bit_string_3[k]:
            lst_not_common.append(int(k))
    print(f"len_of_dismatch :: {len(lst_not_common)}")
    for k in range(len(lst_not_common) - 1, -1, -1):
        bit_string_1 = bit_string_1[:lst_not_common[k]] + bit_string_1[lst_not_common[k] + 1:]
        bit_string_2 = bit_string_2[:lst_not_common[k]] + bit_string_2[lst_not_common[k] + 1:]
        bit_string_3 = bit_string_3[:lst_not_common[k]] + bit_string_3[lst_not_common[k] + 1:]
        bit_string_4 = bit_string_4[:lst_not_common[k]] + bit_string_4[lst_not_common[k] + 1:]
    path_to_result_1 = path_to_result + '/' + os.path.splitext(os.path.basename(file1))[0] + '_clear.txt'
    with open(path_to_result_1, 'w') as fd: fd.write(bit_string_1)
    fd.close()  
    file_for_bitmap_1 = os.path.join(path_to_result + '/', os.path.splitext(os.path.basename(file1))[0] + '_clear.png')
    bitmap_of_sequence(bit_string_1, file_for_bitmap_1)
    p_value = calculate_Pvalue(bit_string_1)
    quality_of_seq = 0
    if float(p_value) >= alpha:    quality_of_seq = 1
    cnt_unity_1 = sum([int(x) if x.isdigit() else x for x in bit_string_1])
    cnt_zero_1 = len(bit_string_1) - cnt_unity_1
    qubit_number = os.path.splitext(os.path.basename(file1))[0].split('_')[0]
    csv_file_cnt_q_all = open(csv_path, "a")
    csv_file_cnt_q_all.write(f"\n{year},{backend},{job_id},"
                             f"{shots},{alpha},{str(qubit_number)},ALC_RES,"
                             f"{p_value},{cnt_zero_1},{cnt_unity_1},{str(quality_of_seq)},NaN")
    csv_file_cnt_q_all.close()
    path_to_result_4 = path_to_result + '/' + os.path.splitext(os.path.basename(file4))[0] + '_clear.txt'
    with open(path_to_result_4, 'w') as fd: fd.write(bit_string_4)
    fd.close()  
    file_for_bitmap_4 = os.path.join(path_to_result + '/', os.path.splitext(os.path.basename(file4))[0] + '_clear.png')
    bitmap_of_sequence(bit_string_4, file_for_bitmap_4)
    p_value = calculate_Pvalue(bit_string_4)
    quality_of_seq = 0
    if float(p_value) >= alpha:    quality_of_seq = 1
    cnt_unity_4 = sum([int(x) if x.isdigit() else x for x in bit_string_4])
    cnt_zero_4 = len(bit_string_4) - cnt_unity_4
    qubit_number = os.path.splitext(os.path.basename(file4))[0].split('_')[0]
    csv_file_cnt_q_all = open(csv_path, "a")
    csv_file_cnt_q_all.write(f"\n{year},{backend},{job_id},"
                             f"{shots},{alpha},{str(qubit_number)},BOB_RES,"
                             f"{p_value},{cnt_zero_4},{cnt_unity_4},{str(quality_of_seq)},NaN")
    csv_file_cnt_q_all.close()
    SIZE_OF_BITSTRING = len(bit_string_4)  
    print(f"len_of all_match :: {len(bit_string_1)}")
    xor_list = []  
    for j in range(0, SIZE_OF_BITSTRING):
        xor_res = int(bit_string_1[j]) ^ int(bit_string_4[j])
        xor_list.append(xor_res)
    print(f"len_of_common :: {sum(xor_list)}\n")
    divergence = sum(xor_list) / SIZE_OF_BITSTRING * 100
    print(f"Divergence :: {divergence}\n")
    return divergence