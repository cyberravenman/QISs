from datetime import datetime
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

import os

import math

from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2

from datetime import date

import pathlib
from pathlib import Path

def Calc_QRNG_Simulator(user_token, num_of_qubits, ibm_channel, alpha, shots, opt_level):

    print("\n-----КГСЧ-СИМУЛЯТОР-----\n")

    user_time = datetime.now()
    current_time = user_time.strftime("%H:%M:%S")
    current_date = date.today()

    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    USR_DIR_NAME_GOOD = "./QRNG_SIMULATOR/" + str(current_date) + "/" + str(current_time) + "/GOOD"
    USR_DIR_NAME_BAD = "./QRNG_SIMULATOR/" + str(current_date) + "/" + str(current_time) + "/BAD"

    NUM_OF_QUBITS_ON_QPU = num_of_qubits
    USER_QUBITS_AND_CLBITS = num_of_qubits
    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)

    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')

    reg_c = []
    for i in range(0, USER_QUBITS_AND_CLBITS):
        locals()[f"reg_c{i}"] = ClassicalRegister(1, f'c{i}')
        reg_c.append(ClassicalRegister(1, f'c{i}'))
    circuit = QuantumCircuit(reg_q, *reg_c)

    for i in range(0, USER_QUBITS_AND_CLBITS):
        circuit.h(reg_q[i])
        circuit.measure(reg_q[i], reg_c[i])

    backend = FakeAlmadenV2()
    sampler = Sampler(backend, options={"default_shots": USER_SHOTS})
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)
    job = sampler.run([(isa_circuit)])
    res = job.result()
    data_pub = res[0].data

    create_dir(USR_DIR_NAME_GOOD)  
    create_dir(USR_DIR_NAME_BAD)  

    for i in range(0, USER_QUBITS_AND_CLBITS):

        now = datetime.now()
        time = now.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f'{i}_' + time + ".txt"

        bitstring = "".join(getattr(data_pub, f'c{i}').get_bitstrings())

        counts = getattr(data_pub, f'c{i}').get_counts()

        p_value = calculate_Pvalue(bitstring)

        if (float(p_value) >= ALPHA):

            dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{i}')
        else:

            dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{i}')

        create_dir(dir_path)  

        path = os.path.join(dir_path, file_name)

        with open(path, 'w') as fd:
            fd.write(bitstring)
        fd.close()  

        print(f"\n[+]: Данные записаны в файл: '{file_name}'")
        print(f"[+]: Соотношение '0' и '1': {counts}")
        print("[+]: p_value: ", p_value)

    print("\nКоличество устойчивых кубит:   ", concatenation_files(USR_DIR_NAME_GOOD))
    print("Количество ненадежных кубит: ", concatenation_files(USR_DIR_NAME_BAD))

    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

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

def concatenation_files(path_to_qubits):

    DIRECTORY = path_to_qubits + "/FINAL_KEY"

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
    return len(txt_files)