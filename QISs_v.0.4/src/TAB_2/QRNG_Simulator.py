from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
from datetime import date
from pathlib import Path
import pathlib
import os
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
class QRNGSimulatorLaunch(QThread):
    def __init__(self, parent=None):
        super(QRNGSimulatorLaunch, self).__init__(parent)
        self.value = 0
        self.token_name = ""                
        self.ibm_channel = ""               
        self.num_of_qubits = 0              
        self.num_of_qubits_max = 0          
        self.alpha = 0.0                    
        self.full_path_for_NIST = ""        
        self.shots = 0                      
        self.opt_level = 0                  
        self.flag_radio_button = False      
        self.list_widget_3_2 = None         
    def run(self):
        try:
            if self.flag_radio_button:
                self.full_path_for_NIST = Calc_QRNG_Simulator(self.token_name, self.ibm_channel, int(self.shots), float(self.alpha), int(self.opt_level), self.num_of_qubits, 0)
            else:
                checked_qubits = []  
                for index in range(self.list_widget_3_2.count()):
                    if self.list_widget_3_2.item(index).checkState() == Qt.Checked:
                        checked_qubits.append(index)  
                self.full_path_for_NIST = Calc_QRNG_Simulator(self.token_name, self.ibm_channel, int(self.shots), float(self.alpha), int(self.opt_level), self.num_of_qubits_max, checked_qubits)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class SliderQRNGSimChanged(QThread):
    def __init__(self, parent=None):
        super(SliderQRNGSimChanged, self).__init__(parent)
        self.value = 0
        self.list_widget_3_2 = None         
        self.current_value = 0              
    def run(self):
        try:
            for i in range(0, self.current_value):
                if self.list_widget_3_2.item(i).checkState() == Qt.Unchecked:
                    self.list_widget_3_2.item(i).setCheckState(QtCore.Qt.Checked)
        except: print("Что-то пошло не так...")
def Calc_QRNG_Simulator(user_token, ibm_channel, shots, alpha, opt_level, num_of_qubits, usr_qubits):
    print("\n-----КГСЧ-СИМУЛЯТОР-----\n")
    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)
    user_time = datetime.now()
    current_time = user_time.strftime("%H:%M:%S")
    current_date = date.today()
    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    NUM_OF_QUBITS_ON_QPU = num_of_qubits
    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')
    if usr_qubits != 0:
        USER_QUBITS_AND_CLBITS = len(usr_qubits)
        reg_c = []
        for i in range(0, USER_QUBITS_AND_CLBITS):
            locals()[f"reg_c{i}"] = ClassicalRegister(1, f'c{usr_qubits[i]}')
            reg_c.append(ClassicalRegister(1, f'c{usr_qubits[i]}'))
        circuit = QuantumCircuit(reg_q, *reg_c)
    else:
        USER_QUBITS_AND_CLBITS = num_of_qubits
        reg_c = []
        for i in range(0, USER_QUBITS_AND_CLBITS):
            locals()[f"reg_c{i}"] = ClassicalRegister(1, f'c{i}')
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
    backend = FakeAlmadenV2()
    sampler = Sampler(backend, options={"default_shots": USER_SHOTS})
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)
    job = sampler.run([(isa_circuit)])
    res = job.result()
    data_pub = res[0].data
    for i in range(0, USER_QUBITS_AND_CLBITS):
        now = datetime.now()
        time = now.strftime("%Y-%m-%d_%H-%M-%S")
        if i == 0:
            PATH_TO_PROJECT_QIS = os.path.expanduser("~") + "/Documents/QISs/"
            create_dir(PATH_TO_PROJECT_QIS)
            USR_DIR_NAME_GOOD = PATH_TO_PROJECT_QIS + "QRNG/QRNG_SIMULATOR/" + str(current_date) + "/" + str(current_time) + "/GOOD"
            USR_DIR_NAME_BAD = PATH_TO_PROJECT_QIS + "QRNG/QRNG_SIMULATOR/" + str(current_date) + "/" + str(current_time) + "/BAD"
            create_dir(USR_DIR_NAME_GOOD)  
            create_dir(USR_DIR_NAME_BAD)  
            file_name_good_q = PATH_TO_PROJECT_QIS + "QRNG/QRNG_SIMULATOR/good_qubits"
            file_name_bad_q = PATH_TO_PROJECT_QIS + "QRNG/QRNG_SIMULATOR/bad_qubits"
            first_str = f"\n          Date    :: {str(current_date)}" + f"\n          Time    :: {str(current_time)}" + f"\n\n          Alpha   :: {str(alpha)}\n          Shots   :: {str(USER_SHOTS)}\n\n"
            file_good_q = open(file_name_good_q, "a")
            file_bad_q = open(file_name_bad_q, "a")
            file_good_q.write("\n-----------------------------------------------------------"); file_good_q.write("\n-----------------------------------------------------------")
            file_good_q.write(first_str)
            file_bad_q.write("\n-----------------------------------------------------------"); file_bad_q.write("\n-----------------------------------------------------------")
            file_bad_q.write(first_str)
            file_good_q.close()
            file_bad_q.close()
            path_for_stats_counts = PATH_TO_PROJECT_QIS + "QRNG/QRNG_SIMULATOR/" + str(current_date) + "/" + str(current_time) + "/"
            file_name_cnt_q = path_for_stats_counts + "cnt_stats"
            file_cnt_q = open(file_name_cnt_q, "a")
            file_cnt_q.write("\n-----------------------------------------------------------"); file_cnt_q.write("\n-----------------------------------------------------------")
            file_cnt_q.write(first_str)
            file_cnt_q.close()
        if usr_qubits != 0:
            file_name = f'{usr_qubits[i]}_' + time + ".txt"
            bitstring = "".join(getattr(data_pub, f'c{usr_qubits[i]}').get_bitstrings())
            counts = getattr(data_pub, f'c{usr_qubits[i]}').get_counts()
        else:
            file_name = f'{i}_' + time + ".txt"
            bitstring = "".join(getattr(data_pub, f'c{i}').get_bitstrings())
            counts = getattr(data_pub, f'c{i}').get_counts()
        p_value = calculate_Pvalue(bitstring)
        if float(p_value) >= ALPHA:
            file_good_q = open(file_name_good_q, "a")
            if usr_qubits != 0:
                dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{usr_qubits[i]}') 
                good_q_str = str(usr_qubits[i]) + " " 
            else:
                dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{i}') 
                good_q_str = str(i) + " " 
            file_good_q.write(good_q_str)
            file_good_q.close()
        else:
            file_bad_q = open(file_name_bad_q, "a")
            if usr_qubits != 0:
                dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{usr_qubits[i]}') 
                bad_q_str = " " + str(usr_qubits[i]) + " " 
            else:
                dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{i}') 
                bad_q_str = " " + str(i) + " " 
            file_bad_q.write(bad_q_str)
            file_bad_q.close()
        create_dir(dir_path)  
        path = os.path.join(dir_path, file_name)
        file_for_bitmap = os.path.join(dir_path, f'{i}_' + time + ".png")
        bitmap_of_sequence(bitstring, file_for_bitmap)
        with open(path, 'w') as fd:
            fd.write(bitstring)
        fd.close()  
        print(f"\n[+]: Данные записаны в файл: '{file_name}'")
        print(f"[+]: Соотношение '0' и '1': {counts}")
        print("[+]: p_value: ", p_value)
        file_cnt_q = open(file_name_cnt_q, "a")
        file_cnt_q.write(f"Кубит {i} :: Соотношение : {counts}      :: p_value : {p_value}\n");    file_cnt_q.close()
    print("\nКоличество устойчивых кубит:   ", concatenation_files(USR_DIR_NAME_GOOD))
    print("Количество ненадежных кубит: ", concatenation_files(USR_DIR_NAME_BAD))
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
def sort_sequences(directory_name):
    txt_files_no_path = []
    path_to_txt_files = []
    txt_sorted_result = []
    dic = {}
    pth = Path(directory_name)
    for file_name in pth.rglob('*.[tT][xX][tT]'):
        txt_files_no_path.append(file_name.name)
        path_to_txt_files.append(os.path.dirname(os.path.abspath(file_name)))
    txt_files_no_path.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    path_to_txt_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if (len(txt_files_no_path) == len(path_to_txt_files)):
        for i in range(0, len(txt_files_no_path)):
            txt_sorted_result.append((path_to_txt_files[i] + '/' + txt_files_no_path[i]))
    return txt_sorted_result
def concatenation_files(path_to_qubits):
    DIRECTORY = path_to_qubits + "/FINAL_KEY"
    txt_files = sort_sequences(path_to_qubits)
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
    size_of_bitmap_max = 4096 * 4096
    if len_of_sequence > size_of_bitmap_max:
        len_of_sequence = 4096 ** 2;    x_axis = 4096;  y_axis = 4096
    else:
        len_of_sequence = math.floor(math.sqrt(len_of_sequence))
        x_axis = len_of_sequence;   y_axis = len_of_sequence;   len_of_sequence = len_of_sequence ** 2
    sequence_slice = sequence[0:len_of_sequence]
    plt.imsave(name_of_bitmap, np.array(sequence_slice).reshape(x_axis, y_axis), cmap=cm.gray)
    plt.clf()