import os
from qiskit_ibm_runtime import QiskitRuntimeService
import math

import pathlib
from pathlib import Path

def Job_Status(token_name, ibm_channel, jobID):
    print(f"\n-----ПРОВЕРКА СТАТУСА РАБОТЫ [ID: '{jobID}']-----\n")

    service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
    job_check = service.job(jobID)

    print("КВУ: ", str(job_check.backend()).split("\'")[1])
    print("Версия Qiskit: ", job_check.metrics()["qiskit_version"])
    print(f"Выполняется? : {job_check.running()}")
    print(f"Статус выполнения: {job_check.status()}")

    tmp_date = job_check.metrics()["timestamps"]["created"]
    create_year = tmp_date.split('T')[0];    create_time = tmp_date.split('T')[1];    create_time = create_time.split('.')[0]
    print("Время создания программы:   " + create_year + "  " + create_time)

    if job_check.status() == "INITIALIZING":
        print("\nПРОГРАММА НА СТАДИИ ПРЕДВАРИТЕЛЬНОЙ ИНИЦИАЛИЗАЦИИ.\nОжидайте. ['INITIALIZING']")

    if job_check.status() == "QUEUED":
        print("\nПРОГРАММА НАХОДИТСЯ В ОЧЕРЕДИ. ['QUEUED']")

        tmp_date = job_check.metrics()["estimated_start_time"]
        estimate_start_year = tmp_date.split('T')[0]; estimate_start_time = tmp_date.split('T')[1]; estimate_start_time = estimate_start_time.split('.')[0]
        print("\nОценка времени запуска:     " + estimate_start_year + "  " + estimate_start_time)

        tmp_date = job_check.metrics()["estimated_completion_time"]
        estimate_complete_year = tmp_date.split('T')[0]; estimate_complete_time = tmp_date.split('T')[1]; estimate_complete_time = estimate_complete_time.split('.')[0]
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

        tmp_date = job_check.metrics()["timestamps"]["running"]
        running_year = tmp_date.split('T')[0];    running_time = tmp_date.split('T')[1];    running_time = running_time.split('.')[0]
        print("\nВремя фактического запуска: " + running_year + "  " + running_time)

        tmp_date = job_check.metrics()["timestamps"]["finished"]
        finished_year = tmp_date.split('T')[0];  finished_time = tmp_date.split('T')[1];  finished_time = finished_time.split('.')[0]
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

    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Job_Cancel(token_name, ibm_channel, jobID):
    print(f"\n-----ОТМЕНА ПРОГРАММЫ [ID: '{jobID}']-----\n")

    try:
        service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
        job_check = service.job(jobID)
        job_check.cancel()
        print("Программа успешно отменена.")
    except Exception as ex: print(ex)

    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Job_Download(token_name, ibm_channel, jobID, alpha):
    print("\n-----ПОПЫТКА СКАЧАТЬ ДАННЫЕ-----\n")

    service = QiskitRuntimeService(channel=ibm_channel, token=token_name)
    job_res = service.job(jobID)

    if job_res.status() == "DONE":
        res = job_res.result()
        data_pub = res[0].data

        tmp_date = job_res.metrics()["timestamps"]["finished"]
        finished_year = tmp_date.split('T')[0]
        backend_name = str(job_res.backend()).split("\'")[1]

        USR_DIR_NAME_GOOD = "./QRNG/Downloaded/" + str(finished_year) + "/" + str(backend_name) + '_' + str(job_res.job_id()) + "/GOOD"
        USR_DIR_NAME_BAD = "./QRNG/Downloaded/" + str(finished_year) + "/" + str(backend_name) + '_' + str(job_res.job_id()) + "/BAD"
        ALPHA = alpha

        finished_time = tmp_date.split('T')[1]
        finished_time = finished_time.split('.')[0]

        for exp in data_pub:

            file_name = exp + "_" + finished_time + str(backend_name) + ".txt"

            bitstring = "".join(data_pub[exp].get_bitstrings())

            counts = data_pub[exp].get_counts()

            p_value = calculate_Pvalue(bitstring)

            if float(p_value) >= ALPHA:

                dir_path = os.path.join(USR_DIR_NAME_GOOD + '/' + f'{exp}')
            else:

                dir_path = os.path.join(USR_DIR_NAME_BAD + '/' + f'{exp}')

            create_dir(dir_path)  

            path = os.path.join(dir_path, file_name)

            with open(path, "w") as fd:
                fd.write(bitstring)
            fd.close()  
            print(f"\n[+]: Данные записаны в файл: '{file_name}'")
            print(f"[+]: Соотношение '0' и '1': {counts}")
            print("[+]: p_value: ", p_value)

        print("\nКоличество устойчивых кубит:   ", concatenation_files(USR_DIR_NAME_GOOD))
        print("Количество ненадежных кубит: ", concatenation_files(USR_DIR_NAME_BAD))

    else:
        print("\nУбедитесь, что статус выполнения программы : 'DONE'.")

    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

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