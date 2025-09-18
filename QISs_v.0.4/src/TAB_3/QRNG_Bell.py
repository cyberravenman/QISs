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
class QPUChangedComboBoxTAB4(QThread):
    def __init__(self, parent=None):
        super(QPUChangedComboBoxTAB4, self).__init__(parent)
        self.value = 0
        self.token_name = ""            
        self.ibm_channel = ""           
        self.ibm_instance = ""          
        self.backend_name = ""          
        self.list_widget_QRNG_Bell = None       
        self.list_widget_QKD_BB84 = None        
        self.spinBox_max_shots = None     
    def run(self):
        try:
            max_qubit, max_shots = set_Num_of_Qubits(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance)
            self.list_widget_QRNG_Bell.clear()
            self.list_widget_QKD_BB84.clear()
            for i in range(0, max_qubit):
                item = QtWidgets.QListWidgetItem(); item.setText(f'Кубит {i}'); item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item.setCheckState(QtCore.Qt.Unchecked)
                self.list_widget_QRNG_Bell.addItem(item)
                item_2 = QtWidgets.QListWidgetItem();   item_2.setText(f'Кубит {i}'); item_2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_2.setCheckState(QtCore.Qt.Unchecked)
                self.list_widget_QKD_BB84.addItem(item_2)
            self.spinBox_max_shots.clear()                  
            self.spinBox_max_shots.setMaximum(max_shots)    
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class QRNGBellStart(QThread):
    def __init__(self, parent=None):
        super(QRNGBellStart, self).__init__(parent)
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
    def run(self):
        if self.file_config == "":  return
        try:
            print(f"\n--------КГСЧ ПО БЕЛЛУ '{self.backend_name}'--------\n")
            QRNG_Bell(self.token_name, self.ibm_channel, self.backend_name,
                      self.shots, self.alpha, self.opt_level,
                      self.use_barriers, self.timezone, self.num_of_qubits_max,
                      self.file_config)
            print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
        except Exception as ex: print(f'Возникло исключение: {ex}')
def QRNG_Bell(user_token, ibm_channel, backend_name,
                shots, alpha, opt_level,
                bool_barriers, time_delta, num_of_qubits,
                file_config):
    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)
    USER_QPU = backend_name
    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    NUM_OF_QUBITS_ON_QPU = num_of_qubits
    list_dir_name_of_seq = []
    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')
    reg_c = []
    reg_q_hadamard = [];    reg_q_cnot = [];    reg_measure = []
    with open(file_config, "r") as fp:
        lines = fp.readlines(); len_of_config_file = len(lines)
        for i in range(0, len_of_config_file):
            had_in_file = lines[i].split('=')[1].split(':')[0]
            cnot_in_file = lines[i].split('=')[1].split(':')[1].strip('\n')
            if had_in_file != "":
                reg_c.append(ClassicalRegister(1, f'c{had_in_file}'))
                reg_q_hadamard.append(int(had_in_file))
                reg_measure.append(int(had_in_file))
            else:   print("Не удалось идентифицировать все поля HADAMARD. Проверьте конфигурационный файл");    return
            if cnot_in_file != "":
                reg_c.append(ClassicalRegister(1, f'c{cnot_in_file}'))
                reg_q_cnot.append(int(cnot_in_file))
                reg_measure.append(int(cnot_in_file))
            else:   print("Не удалось идентифицировать все поля CNOT. Проверьте конфигурационный файл");    return
    USER_QUBITS_AND_CLBITS = len(reg_measure)
    circuit = QuantumCircuit(reg_q, *reg_c)
    for i in range(0, NUM_OF_QUBITS_ON_QPU):
        for j in range(0, len(reg_q_hadamard)):
            if i == reg_q_hadamard[j]:
                circuit.h(reg_q[i])
                index = int(reg_q_cnot[j])
                circuit.cx(reg_q[i], reg_q[index])
                circuit.measure(reg_q[i], reg_c[j*2])
                circuit.measure(reg_q[index], reg_c[j*2+1])
                if bool_barriers:
                    circuit.barrier(*reg_q)
                break
    machine_name = USER_QPU
    backend = service.least_busy(operational=True, simulator=False, name=machine_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)
    with Session(backend=backend) as session:
        sampler = Sampler(session, options={"default_shots": USER_SHOTS})
        job = sampler.run([isa_circuit])
        print(f"[+]: Идентификатор Job_ID: {job.job_id()}")
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
        jbid_str_1 = f"\n[QRNG_BELL]\n[CREATED]: {str(create_year)}" + "  " + str(create_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_2 = f"[STARTED]: {str(estimate_start_year)}" + "  " + str(estimate_start_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_3 = f"[SHOTS]:   {shots}\n[ALPHA]:   {alpha}\n\n"
        csv_str_1 = "Project_Type,Status,Date,Time,JobID,Backend,Shots,Alpha"
        csv_str_2 = f"\nQRNG_BELL,CREATED,{create_year},{create_time},{job.job_id()},{backend_name},{shots},{alpha}"
        file_jbid.write(jbid_str_1);    file_jbid.write(jbid_str_2);    file_jbid.write(jbid_str_3);    file_jbid.close()
        if os.stat(csv_file_path_to_jbID).st_size == 0:  csv_file_jbid.write(csv_str_1)
        csv_file_jbid.write(csv_str_2); csv_file_jbid.close()
        res = job.result()
        data_pub = res[0].data
        dirlist = []
        for i in range(0, USER_QUBITS_AND_CLBITS):
            now = datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S")
            if i == 0:
                tmp_date = pd.Timestamp(job.metrics()["timestamps"]["running"]) + pd.Timedelta(hours=time_delta)
                running_year = tmp_date.strftime("%Y-%m-%d");   running_time = '{:%H:%M:%S}'.format(tmp_date)
                USR_DIR_NAME = PATH_TO_PROJECT_QIS + "QKD/QRNG_BELL/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}"
                create_dir(USR_DIR_NAME)
                path_for_stats_counts = PATH_TO_PROJECT_QIS + "QKD/QRNG_BELL/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}/"
                csv_file_name_all_q = path_for_stats_counts + f"ALL_qubits_stats_{str(job.job_id())}.csv"
                csv_first_str = "Date,Backend,JobID,Shots,Alpha,BellPair,Qubit,P_Value,Zero,One,Quality,Divergence"
                csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
                csv_file_cnt_q_all.write(csv_first_str)
                csv_file_cnt_q_all.close()
                for k in range(0, len(reg_q_hadamard)):
                    dir_path = os.path.join(USR_DIR_NAME + '/' + f'{reg_q_hadamard[k]}:{reg_q_cnot[k]}')  
                    create_dir(dir_path)
                    dirlist = [item for item in os.listdir(USR_DIR_NAME) if os.path.isdir(os.path.join(USR_DIR_NAME, item))]
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
            try:
                for k in range(0, len(dirlist)):
                    for l in range(0, len(reg_measure)):
                        had_name = int(dirlist[k].split(':')[0])
                        cnot_name = int(dirlist[k].split(':')[1].strip('\n'))
                        if (index == had_name) | (index == cnot_name):
                            dir_path = os.path.join(USR_DIR_NAME + '/' + dirlist[k], file_name)
                            with open(dir_path, 'w') as fd: fd.write(bitstring)
                            fd.close()  
                            file_for_bitmap = os.path.join(USR_DIR_NAME + '/' + dirlist[k], f'{index}_' + time + "_" + machine_name + ".png")
                            bitmap_of_sequence(bitstring, file_for_bitmap)
                            list_dir_name_of_seq.append(dir_path)
                            break
            except Exception as ex:   print("EXCEPTION: ", ex)
            if i % 2 == 0:
                bell_pair = str(reg_measure[i]) + ':' + str(reg_measure[i+1])
                divergence = "NaN"
            else:
                bell_pair = str(reg_measure[i-1]) + ':' + str(reg_measure[i])
                divergence = Fcorr_easy(list_dir_name_of_seq[0], list_dir_name_of_seq[1])
                list_dir_name_of_seq = []
            csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
            csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                     f"{shots},{alpha},{bell_pair},{str(reg_measure[i])},"
                                     f"{p_value},{counts_zero},{counts_unity},{str(quality_of_seq)},{str(divergence)}")
            csv_file_cnt_q_all.close()
            print(f"\n[+]: Данные записаны в файл: '{file_name}'")
            print(f"[+]: '0' [{counts_zero}]")
            print(f"[+]: '1' [{counts_unity}]")
        df = pd.read_csv(csv_file_name_all_q)
        df['Divergence'].fillna(method='backfill', inplace=True)
        df.to_csv(csv_file_name_all_q)
        qnt_seq = job.metrics()["usage"]["quantum_seconds"]
        usg_seq = job.metrics()["usage"]["seconds"]
        print("\nTime of QPU: ", qnt_seq)
        print("Time of usage: ", usg_seq)
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
def Fcorr_easy(file1, file2):
    bit_string_1 = []           
    bit_string_2 = []           
    with open(file1, 'r', encoding='utf-8') as file_1:
        while True:
            bit1 = file_1.read(1)
            if not bit1:    break
            if bit1.isdigit():  bit_string_1.append(int(bit1))
    file_1.close()
    with open(file2, 'r', encoding='utf-8') as file_2:
        while True:
            bit2 = file_2.read(1)
            if not bit2:    break
            if bit2.isdigit():  bit_string_2.append(int(bit2))
    file_2.close()
    SIZE_OF_BITSTRING = len(bit_string_2)  
    xor_list = []  
    for j in range(0, SIZE_OF_BITSTRING):
        xor_res = bit_string_1[j] ^ bit_string_2[j]
        xor_list.append(xor_res)
    divergence = sum(xor_list) / SIZE_OF_BITSTRING * 100
    return divergence