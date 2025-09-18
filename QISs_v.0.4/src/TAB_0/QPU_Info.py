from qiskit_ibm_runtime import QiskitRuntimeService
from datetime import date
from PyQt5.QtCore import QThread
import inspect
import os
class QPUBaseInfo1(QThread):
    def __init__(self, parent=None):
        super(QPUBaseInfo1, self).__init__(parent)
        self.value = 0
        self.token_name = ""                        
        self.ibm_channel = ""                       
        self.ibm_instance = ""                      
        self.combo_box_Dynamic_INFO = None          
        self.combo_box_Dynamic_INIT_IDLE_H = None   
        self.combo_box_Dynamic_QRNG = None          
        self.combo_box_Dynamic_QRNG_Bell = None     
    def run(self):
        try:
            available_QPU_list = QPU_Available(self.token_name, self.ibm_channel, self.ibm_instance)
            for i in range(0, len(available_QPU_list)):
                self.combo_box_Dynamic_QRNG.addItem(str(available_QPU_list[i]).split("\'")[1])
                self.combo_box_Dynamic_INFO.addItem(str(available_QPU_list[i]).split("\'")[1])
                self.combo_box_Dynamic_INIT_IDLE_H.addItem(str(available_QPU_list[i]).split("\'")[1])
                self.combo_box_Dynamic_QRNG_Bell.addItem(str(available_QPU_list[i]).split("\'")[1])
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class QPUBaseInfo2(QThread):
    def __init__(self, parent=None):
        super(QPUBaseInfo2, self).__init__(parent)
        self.value = 0
        self.token_name = ""                
        self.ibm_channel = ""               
        self.ibm_instance = ""              
        self.backend_name = ""              
        self.combo_box_Dynamic = None       
    def run(self):
        try:    QPU_More_Info(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class QPUQubitInfo(QThread):
    def __init__(self, parent=None):
        super(QPUQubitInfo, self).__init__(parent)
        self.value = 0
        self.token_name = ""        
        self.ibm_channel = ""       
        self.ibm_instance = ""      
        self.backend_name = ""      
        self.qubit_number = 0       
    def run(self):
        try:    Qubit_Info(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance, self.qubit_number)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
class QPUChangedComboBoxINFO(QThread):
    def __init__(self, parent=None):
        super(QPUChangedComboBoxINFO, self).__init__(parent)
        self.value = 0
        self.token_name = ""        
        self.ibm_channel = ""       
        self.ibm_instance = ""      
        self.backend_name = ""      
        self.slider_INFO = None          
    def run(self):
        try:
            max_qubit, max_shots = set_Num_of_Qubits(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance)
            self.slider_INFO.setMaximum(max_qubit-1)
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def QPU_Available(token, channel, instance):
    print("\n-----ПОИСК ДОСТУПНЫХ КВУ-----\n")
    print("\nНаправляю запрос в IBM Quantum Platform на предмет поиска доступных КВУ."
          "\nПо готовности сообщу...")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    list_of_qpu = service.backends()
    print("Проверьте выпадающий список.")
    print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    return list_of_qpu
def Qubit_Info(token, channel, backend_name, instance, qubit_number):
    print(f"\n-----СВЕДЕНИЯ ПО КУБИТУ: {qubit_number} -----\n")
    print(f"Уточняю информацию по {qubit_number} кубиту...\n")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    backend = service.backend(backend_name)
    print(
        f"КВУ: '{backend.name}'\n"
    )
    print("\nНомер кубита: "+ str(qubit_number))
    print(backend.qubit_properties(qubit_number))
    print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
def QPU_More_Info(token, channel, backend_name, instance):
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
        file_name = backend.name + '_' + str(date.today())
        folder_path = os.path.expanduser("~") + "/Documents/QISs/QPU_Info"
        filepath = os.path.join(folder_path, file_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(filepath, 'w') as file:
            for name, value in inspect.getmembers(backend):
                if not name.startswith('__'):
                    file.write(f"{name}: {value}\n")
        file.close()
        print(f"\nДетальная информация о КВУ: '{backend.name}' сохранена в файл: ./{filepath}.")
        print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    except:
        print("\nНепредвиденная ошибка.")
def set_Num_of_Qubits(token, channel, backend_name, instance):
    print("\n-----РАЗМЕР РЕГИСТРА КВУ-----\n")
    print("Уточняю максимально-возможное количество кубит на КВУ...\n")
    service = QiskitRuntimeService(channel=channel, instance=instance, token=token)
    backend = service.backend(backend_name)
    print(f"КВУ: '{backend.name}' имеет [{backend.num_qubits}] кубит.")
    print("\n--------------- УСПЕШНО -------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")
    return backend.num_qubits, backend.max_shots