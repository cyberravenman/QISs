from qiskit_ibm_runtime import QiskitRuntimeService

import inspect

from datetime import date

import os

def QPU_Available(channel, instance, token):
    print("\n-----ПОИСК ДОСТУПНЫХ КВУ-----\n")
    print("\nНаправляю запрос в IBM Quantum Platform на предмет поиска доступных КВУ."
          "\nПо готовности сообщу...")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    list_of_qpu = service.backends()
    print("Проверьте выпадающий список.\n")
    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

    return list_of_qpu

def Qubit_Info(channel, instance, token, backend_name, qubit_number):
    print(f"\n-----СВЕДЕНИЯ ПО КУБИТУ: {qubit_number} -----\n")
    print(f"Уточняю информацию по {qubit_number} кубиту...\n")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    backend = service.backend(backend_name)
    print(
        f"КВУ: '{backend.name}'\n"

    )
    print("\nНомер кубита: "+ str(qubit_number))
    print(backend.qubit_properties(qubit_number))
    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def QPU_More_Info(channel, instance, token, backend_name):
    print("\n-----ИНФОРМАЦИЯ О КВУ-----\n")
    print("Запрашиваю доступ на детальную информацию о КВУ. По готовности сообщу...\n")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    backend = service.backend(backend_name)
    print(
        f"КВУ: {backend.name}\n"
        f"Версия: {backend.version}\n"
        f"Количество кубит [всего]: {backend.num_qubits}\n"
    )

    try:

        file_name = backend.name + '_' + str(date.today()) + ".txt"
        folder_path = "QPU_Info/"

        filepath = os.path.join(folder_path, file_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(filepath, 'w') as file:
            for name, value in inspect.getmembers(backend):
                if not name.startswith('__'):
                    file.write(f"{name}: {value}\n")

        file.close()
        print(f"\nДетальная информация о КВУ: '{backend.name}' сохранена в файл: ./{filepath}.\n")
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    except:
        print("\nНепредвиденная ошибка.")

def set_Num_of_Qubits(channel, instance, token, backend_name):
    print("\n-----РАЗМЕР РЕГИСТРА КВУ-----\n")
    print("Уточняю максимально-возможное количество кубит на КВУ...\n")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    backend = service.backend(backend_name)

    print(f"КВУ: '{backend.name}' имеет [{backend.num_qubits}] кубит\n")
    print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    return backend.num_qubits