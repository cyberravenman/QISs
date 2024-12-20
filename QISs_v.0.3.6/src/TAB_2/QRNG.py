from datetime import datetime
from PyQt5.QtCore import QThread
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from src.TAB_0.QPU_Info import set_Num_of_Qubits
from datetime import date
import os
import math
import pathlib

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class QRNGLaunch(QThread):

    def __init__(self, parent=None):
        super(QRNGLaunch, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.backend_name = ""              
        self.ibm_channel = ""               

        self.full_path_for_NIST = ""        

        self.flag_radio_button = False      
        self.num_of_qubits = 0              
        self.num_of_qubits_max = 0          

        self.alpha = 0.0                    
        self.shots = 0                      
        self.opt_level = 0                  

        self.list_widget_3_1 = None         

    def run(self):

        try:
            if self.flag_radio_button:

                self.full_path_for_NIST = Calc_QRNG(self.token_name, self.ibm_channel, self.backend_name,
                                                    int(self.shots), float(self.alpha),  int(self.opt_level),
                                                    self.num_of_qubits, 0)
            else:

                checked_qubits = []  

                for index in range(self.list_widget_3_1.count()):

                    if self.list_widget_3_1.item(index).checkState() == Qt.Checked:
                        checked_qubits.append(index)  

                if len(checked_qubits) != 0:
                    self.full_path_for_NIST = Calc_QRNG(self.token_name, self.ibm_channel, self.backend_name,
                                                        int(self.shots), float(self.alpha), int(self.opt_level),
                                                        self.num_of_qubits_max, checked_qubits)
                else:
                    print("Не выбран ни один кубит. Перепроверьте установочные данные."); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class QPUChangedComboBoxQRNG(QThread):

    def __init__(self, parent=None):
        super(QPUChangedComboBoxQRNG, self).__init__(parent)

        self.value = 0

        self.token_name = ""            
        self.ibm_channel = ""           
        self.ibm_instance = ""          
        self.backend_name = ""          

        self.slider_QRNG = None         
        self.list_widget_3_1 = None     

        self.spinBox_max_shots = None  

    def run(self):
        try:
            max_qubit, max_shots = set_Num_of_Qubits(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance)

            self.list_widget_3_1.clear()
            for i in range(0, max_qubit):
                item_3_1 = QtWidgets.QListWidgetItem(); item_3_1.setText(f'Кубит {i}'); item_3_1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_3_1.setCheckState(QtCore.Qt.Unchecked)  
                self.list_widget_3_1.addItem(item_3_1)

            self.slider_QRNG.setMaximum(max_qubit)
            self.slider_QRNG.setMinimum(1)  

            self.spinBox_max_shots.clear()                      
            self.spinBox_max_shots.setMaximum(max_shots)        
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class SliderQRNGChanged(QThread):

    def __init__(self, parent=None):
        super(SliderQRNGChanged, self).__init__(parent)

        self.value = 0

        self.list_widget_3_1 = None         
        self.current_value = 0              

    def run(self):
        try:

            for i in range(0, self.current_value):
                if self.list_widget_3_1.item(i).checkState() == Qt.Unchecked:
                    self.list_widget_3_1.item(i).setCheckState(QtCore.Qt.Checked)
        except: print("Что-то пошло не так...")

def Calc_QRNG(user_token, ibm_channel, backend_name,
              shots, alpha, opt_level,
              num_of_qubits, usr_qubits):
    print(f"\n-----КГСЧ: '{backend_name}'-----\n")

    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)

    USER_QPU = backend_name
    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    NUM_OF_QUBITS_ON_QPU = num_of_qubits

    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')

    if usr_qubits != 0:
        USER_QUBITS_AND_CLBITS = len(usr_qubits)

        reg_c = []
        for i in range(0, USER_QUBITS_AND_CLBITS):
            reg_c.append(ClassicalRegister(1, f'c{usr_qubits[i]}'))
        circuit = QuantumCircuit(reg_q, *reg_c)

    else:
        USER_QUBITS_AND_CLBITS = num_of_qubits

        reg_c = []
        for i in range(0, USER_QUBITS_AND_CLBITS):
            reg_c.append(ClassicalRegister(1, f'c{i}'))
        circuit = QuantumCircuit(reg_q, *reg_c)

    if usr_qubits != 0:
        for i in range(0, NUM_OF_QUBITS_ON_QPU):
            for j in range(0, USER_QUBITS_AND_CLBITS):
                if i == usr_qubits[j]:
                    circuit.h(reg_q[i])
                    circuit.measure(reg_q[i], reg_c[j])
                    break

    else:
        for i in range(0, NUM_OF_QUBITS_ON_QPU):
            circuit.h(reg_q[i])
            circuit.measure(reg_q[i], reg_c[i])

    machine_name = USER_QPU
    backend = service.least_busy(operational=True, simulator=False, name=machine_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)

    with Session(backend=backend) as session:

        sampler = Sampler(session, options={"default_shots": USER_SHOTS})

        job = sampler.run([isa_circuit])
        print(f"[+]: Идентификатор Job_ID: {job.job_id()}")

        tmp_date = job.metrics()["timestamps"]["created"]
        create_year = tmp_date.split('T')[0];   create_time = tmp_date.split('T')[1];   create_time = create_time.split('.')[0]

        tmp_date_finish = job.metrics()["estimated_start_time"]

        while tmp_date_finish == None:   tmp_date_finish = job.metrics()["estimated_start_time"]

        estimate_start_year = tmp_date_finish.split('T')[0];    estimate_start_time = tmp_date_finish.split('T')[1];    estimate_start_time = estimate_start_time.split('.')[0]
        print("\nОценка времени запуска:     " + estimate_start_year + "  " + estimate_start_time)
        print("Текущая позиция в очереди:    ", job.metrics()["position_in_queue"])
        print("Текущая позиция у провайдера: ", job.metrics()["position_in_provider"])

        PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/"
        create_dir(PATH_TO_PROJECT_QIS)
        file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID"
        csv_file_path_to_jbID = PATH_TO_PROJECT_QIS + "JobID.csv"
        file_jbid = open(file_path_to_jbID, "a")
        csv_file_jbid = open(csv_file_path_to_jbID, "a")
        jbid_str_1 = f"\n[QRNG]\n[CREATED]: {str(create_year)}" + "  " + str(create_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_2 = f"[STARTED]: {str(estimate_start_year)}" + "  " + str(estimate_start_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_3 = f"[SHOTS]:   {shots}\n[ALPHA]:   {alpha}\n\n"
        csv_str_1 = "Project_Type,Status,Date,Time,JobID,Backend,Shots,Alpha"
        csv_str_2 = f"\nQRNG,CREATED,{create_year},{create_time},{job.job_id()},{backend_name},{shots},{alpha}"
        file_jbid.write(jbid_str_1);    file_jbid.write(jbid_str_2);    file_jbid.write(jbid_str_3);    file_jbid.close()
        if os.stat(csv_file_path_to_jbID).st_size == 0:  csv_file_jbid.write(csv_str_1)
        csv_file_jbid.write(csv_str_2); csv_file_jbid.close()

        res = job.result()
        data_pub = res[0].data

        for i in range(0, USER_QUBITS_AND_CLBITS):

            now = datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S")

            if i == 0:
                tmp_date = job.metrics()["timestamps"]["running"]
                running_year = tmp_date.split('T')[0];  running_time = tmp_date.split('T')[1];  running_time = running_time.split('.')[0]

                USR_DIR_NAME_GOOD = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}/GOOD"
                USR_DIR_NAME_BAD = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}/BAD"
                create_dir(USR_DIR_NAME_GOOD)   
                create_dir(USR_DIR_NAME_BAD)    

                create_dir(PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + f"STATs_{str(backend_name)}")
                file_name_good_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + f"STATs_{str(backend_name)}" + "/good_qubits_stats"
                file_name_bad_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + f"STATs_{str(backend_name)}" + "/bad_qubits_stats"
                first_str = f"\n          Date    :: {str(running_year)}\n          Time    :: {str(running_time)} \
                            \n          Backend :: {str(backend_name)}\n          JobID   :: {str(job.job_id())}\n \
                            \n          Alpha   :: {str(alpha)}\n          Shots   :: {str(USER_SHOTS)}\n\n"
                file_good_q = open(file_name_good_q, "a");  file_bad_q = open(file_name_bad_q, "a")
                file_good_q.write("\n-----------------------------------------------------------");  file_good_q.write("\n-----------------------------------------------------------")
                file_bad_q.write("\n-----------------------------------------------------------");  file_bad_q.write("\n-----------------------------------------------------------")
                file_good_q.write(first_str);   file_bad_q.write(first_str)
                file_good_q.close();    file_bad_q.close()

                path_for_stats_counts = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}/"
                file_name_cnt_q_good = path_for_stats_counts + "cnt_stats_good"
                file_name_cnt_q_bad = path_for_stats_counts + "cnt_stats_bad"

                file_cnt_q_good = open(file_name_cnt_q_good, "a");   file_cnt_q_bad = open(file_name_cnt_q_bad, "a")
                file_cnt_q_good.write("\n-----------------------------------------------------------");  file_cnt_q_good.write("\n-----------------------------------------------------------")
                file_cnt_q_bad.write("\n-----------------------------------------------------------");  file_cnt_q_bad.write("\n-----------------------------------------------------------")
                file_cnt_q_good.write(first_str);   file_cnt_q_bad.write(first_str)
                file_cnt_q_good.close();    file_cnt_q_bad.close()

                csv_file_name_good_q = path_for_stats_counts + f"good_qubits_stats_{str(job.job_id())}.csv"
                csv_file_name_bad_q = path_for_stats_counts + f"bad_qubits_stats_{str(job.job_id())}.csv"
                csv_file_name_all_q = path_for_stats_counts + f"ALL_qubits_stats_{str(job.job_id())}.csv"
                csv_first_str = "Date,Backend,JobID,Shots,Alpha,Qubit,P_Value,Zero,One"
                csv_file_cnt_q_good = open(csv_file_name_good_q, "a");  csv_file_cnt_q_bad = open(csv_file_name_bad_q, "a")
                csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
                csv_file_cnt_q_good.write(csv_first_str);   csv_file_cnt_q_bad.write(csv_first_str)
                csv_file_cnt_q_all.write(csv_first_str)
                csv_file_cnt_q_good.close();    csv_file_cnt_q_bad.close(); csv_file_cnt_q_all.close()

                file_name_all_good_q = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + f"STATs_{str(backend_name)}" + "/_STATS_by_count.csv"
                csv_first_str = "Date,Backend,JobID,Shots,Alpha,cnt_of_GOOD,KEY_good(KB),cnt_of_BAD,KEY_bad(KB),quantum_sec,usage_sec,bss_seq"
                csv_file_cnt_q_all_good = open(file_name_all_good_q, "a")
                if os.stat(file_name_all_good_q).st_size == 0:  csv_file_cnt_q_all_good.write(csv_first_str)
                csv_file_cnt_q_all_good.close()

            if usr_qubits != 0:
                file_name = f'{usr_qubits[i]}_' + time + "_" + machine_name + ".txt"

                bitstring = "".join(getattr(data_pub, f'c{usr_qubits[i]}').get_bitstrings())

                counts = getattr(data_pub, f'c{usr_qubits[i]}').get_counts()

            else:
                file_name = f'{i}_' + time + "_" + machine_name + ".txt"

                bitstring = "".join(getattr(data_pub, f'c{i}').get_bitstrings())

                counts = getattr(data_pub, f'c{i}').get_counts()

            p_value = calculate_Pvalue(bitstring)

            try:    counts_zero = counts["0"]
            except Exception as ex: counts_zero = 0

            try:    counts_unity = counts["1"]
            except Exception as ex: counts_unity = 0

            csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
            if usr_qubits != 0:
                csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                         f"{shots},{alpha},{usr_qubits[i]},"
                                         f"{p_value},{counts_zero},{counts_unity}")
            else:
                csv_file_cnt_q_all.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                         f"{shots},{alpha},{i},"
                                         f"{p_value},{counts_zero},{counts_unity}")
            csv_file_cnt_q_all.close()

            if float(p_value) >= ALPHA:

                file_good_q = open(file_name_good_q, "a");  file_cnt_q_good = open(file_name_cnt_q_good, "a")

                csv_file_cnt_q_good = open(csv_file_name_good_q, "a")

                if usr_qubits != 0:
                    dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{usr_qubits[i]}') 
                    good_q_str = str(usr_qubits[i]) + " " 

                    file_cnt_q_good.write(f"Кубит {usr_qubits[i]} :: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                    csv_file_cnt_q_good.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                              f"{USER_SHOTS},{alpha},{usr_qubits[i]},"
                                              f"{p_value},{counts_zero},{counts_unity}")

                else:
                    dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{i}') 
                    good_q_str = str(i) + " " 

                    file_cnt_q_good.write(f"Кубит {i} :: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                    csv_file_cnt_q_good.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                              f"{USER_SHOTS},{alpha},{i},"
                                              f"{p_value},{counts_zero},{counts_unity}")
                file_good_q.write(good_q_str)
                file_good_q.close();    file_cnt_q_good.close();    csv_file_cnt_q_good.close()

            else:

                file_bad_q = open(file_name_bad_q, "a");    file_cnt_q_bad = open(file_name_cnt_q_bad, "a")

                csv_file_cnt_q_bad = open(csv_file_name_bad_q, "a")

                if usr_qubits != 0:
                    dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{usr_qubits[i]}')
                    bad_q_str = str(usr_qubits[i]) + " "  

                    file_cnt_q_bad.write(f"Кубит {usr_qubits[i]} :: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                    csv_file_cnt_q_bad.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                              f"{USER_SHOTS},{alpha},{usr_qubits[i]},"
                                              f"{p_value},{counts_zero},{counts_unity}")

                else:
                    dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{i}')
                    bad_q_str = str(i) + " "  

                    file_cnt_q_bad.write(f"Кубит {i} :: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n")
                    csv_file_cnt_q_bad.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                              f"{USER_SHOTS},{alpha},{i},"
                                              f"{p_value},{counts_zero},{counts_unity}")
                file_bad_q.write(bad_q_str)
                file_bad_q.close(); file_cnt_q_bad.close(); csv_file_cnt_q_bad.close()

            create_dir(dir_path)  

            path = os.path.join(dir_path, file_name)

            file_for_bitmap = os.path.join(dir_path, f'{i}_' + time + "_" + machine_name + ".png")
            bitmap_of_sequence(bitstring, file_for_bitmap)

            with open(path, 'w') as fd:
                fd.write(bitstring)
            fd.close()  

            print(f"\n[+]: Данные записаны в файл: '{file_name}'")

            print(f"[+]: '0' [{counts_zero}]")
            print(f"[+]: '1' [{counts_unity}]")
            print("[+]: p_value: ", p_value)

        path_to_all_qubits = PATH_TO_PROJECT_QIS + "QRNG/QPU_EXEC/" + str(running_year) + "/" + str(backend_name) + f"/{shots}_{alpha}_{str(job.job_id())}"
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
        qnt_seq = job.metrics()["usage"]["quantum_seconds"]
        usg_seq = job.metrics()["usage"]["seconds"]
        bss_seq = job.metrics()["bss"]["seconds"]
        len_KEY_good_KB = good_qubits_cnt * shots / 8 / 1000
        len_KEY_bad_KB = bad_qubits_cnt * shots / 8 / 1000
        csv_file_cnt_q_all_good.write(f"\n{running_year},{backend_name},{job.job_id()},"
                                      f"{shots},{alpha},{good_qubits_cnt},{round(len_KEY_good_KB, 3)},"
                                      f"{bad_qubits_cnt},{round(len_KEY_bad_KB, 3)},{qnt_seq},{usg_seq},{bss_seq}")
        csv_file_cnt_q_all_good.close()

        print("\nTime of QPU: ", qnt_seq)
        print("Time of usage: ", usg_seq)
        print("Final KEY length, (KB): ", len_KEY_good_KB)

        print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

        return pathlib.Path(USR_DIR_NAME_GOOD).parent.absolute()

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

    file_with_key = DIRECTORY + 'KEY.txt'

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
    bitmap_of_sequence(key_sequence, DIRECTORY + 'KEY.png')

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