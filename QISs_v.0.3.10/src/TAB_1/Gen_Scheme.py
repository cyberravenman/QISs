from datetime import datetime
import pandas as pd
from PyQt5.QtCore import QThread
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from PyQt5.QtCore import Qt
import os
import math

class GenerateScheme(QThread):

    def __init__(self, parent=None):
        super(GenerateScheme, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.backend_name = ""              
        self.ibm_channel = ""               

        self.alpha = 0.0                    
        self.shots = 0                      
        self.opt_level = 0                  

        self.timezone = 0                   

        self.flag_radio_button_2_1 = False  
        self.flag_radio_button_2_2 = False  
        self.flag_radio_button_2_3 = False  
        self.list_widget_2_1 = None         
        self.list_widget_2_2 = None         
        self.list_widget_2_3 = None         

        self.num_of_qubits_max = 0          
        self.use_barriers = False           

        self.slider_current_2_1 = 0         
        self.slider_current_2_2 = 0         
        self.slider_current_2_3 = 0         

    def run(self):

        try:
            checked_qubits_2_1 = []  
            checked_qubits_2_2 = []  
            checked_qubits_2_3 = []  

            if self.flag_radio_button_2_1:

                for i in range (0, self.slider_current_2_1):
                    checked_qubits_2_1.append(i)                
            elif not self.flag_radio_button_2_1:

                for index in range(self.list_widget_2_1.count()):

                    if self.list_widget_2_1.item(index).checkState() == Qt.Checked:
                        checked_qubits_2_1.append(index)        

            if self.flag_radio_button_2_2:

                for i in range(0, self.slider_current_2_2):
                    checked_qubits_2_2.append(i)                
            elif not self.flag_radio_button_2_2:

                for index in range(self.list_widget_2_2.count()):

                    if self.list_widget_2_2.item(index).checkState() == Qt.Checked:
                        checked_qubits_2_2.append(index)        

            if self.flag_radio_button_2_3:

                for i in range(0, self.slider_current_2_3):
                    checked_qubits_2_3.append(i)                
            elif not self.flag_radio_button_2_3:

                for index in range(self.list_widget_2_3.count()):

                    if self.list_widget_2_3.item(index).checkState() == Qt.Checked:
                        checked_qubits_2_3.append(index)        

            if len(checked_qubits_2_1) != 0:
                Idle_Init_X(self.token_name, self.ibm_channel, self.backend_name,
                            int(self.shots), float(self.alpha), int(self.opt_level),
                            int(self.num_of_qubits_max), self.use_barriers,
                            checked_qubits_2_1, checked_qubits_2_2, checked_qubits_2_3,
                            self.timezone)
            else:
                print("Не выбран ни один кубит. Перепроверьте установочные данные.");   print("\n--------------- ОШИБКА --------------");   print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def Idle_Init_X(user_token, ibm_channel, backend_name,
                shots, alpha, opt_level,
                max_qubits, bool_barriers,
                usr_qubits_IDLE_2_1, usr_qubits_INIT_2_2, usr_qubits_X_2_3,
                time_delta):
    print(f"\n-----IDLE_INIT_X: '{backend_name}'-----\n")

    use_IDLE = True     
    use_INIT = False
    use_X = False

    IDLE_INIT_or = list(set(usr_qubits_IDLE_2_1 + usr_qubits_INIT_2_2));    IDLE_INIT_result = list(set(IDLE_INIT_or) ^ set(usr_qubits_IDLE_2_1))
    if len(IDLE_INIT_result) != 0:
        print("Количество кубит ['INIT'] не должно выходить за границы выбранных ['IDLE'] кубит."); return

    IDLE_X_or = list(set(usr_qubits_IDLE_2_1 + usr_qubits_X_2_3));  IDLE_X_result = list(set(IDLE_X_or) ^ set(usr_qubits_IDLE_2_1))
    if len(IDLE_X_result) != 0:
        print("Количество кубит ['X'] не должно выходить за границы выбранных ['IDLE'] кубит.");    return

    service = QiskitRuntimeService(channel=ibm_channel, token=user_token)
    USER_QPU = backend_name
    USER_SHOTS = shots
    USER_OPTIMISATION_LEVEL = opt_level
    ALPHA = alpha
    NUM_OF_QUBITS_ON_QPU = max_qubits
    USER_QUBITS_AND_CLBITS = len(usr_qubits_IDLE_2_1)

    reg_q = QuantumRegister(NUM_OF_QUBITS_ON_QPU, 'q')

    reg_c = []
    for i in range(0, USER_QUBITS_AND_CLBITS):
        reg_c.append(ClassicalRegister(1, f'c{usr_qubits_IDLE_2_1[i]}'))
    circuit = QuantumCircuit(reg_q, *reg_c)

    if len(usr_qubits_INIT_2_2) != 0:
        use_INIT = True

        for i in range(0, len(usr_qubits_IDLE_2_1)):
            for j in range(0, len(usr_qubits_INIT_2_2)):
                if usr_qubits_INIT_2_2[j] == usr_qubits_IDLE_2_1[i]:    circuit.reset(reg_q[usr_qubits_INIT_2_2[j]])

        if bool_barriers:
            circuit.barrier(*reg_q)

    if len(usr_qubits_X_2_3) != 0:
        use_X = True

        for i in range(0, len(usr_qubits_IDLE_2_1)):
            for j in range(0, len(usr_qubits_X_2_3)):
                if usr_qubits_X_2_3[j] == usr_qubits_IDLE_2_1[i]:   circuit.x(reg_q[usr_qubits_X_2_3[j]])

        if bool_barriers:
            circuit.barrier(*reg_q)

    for i in range(0, NUM_OF_QUBITS_ON_QPU):
        for j in range(0, USER_QUBITS_AND_CLBITS):
            if i == usr_qubits_IDLE_2_1[j]: circuit.measure(reg_q[i], reg_c[j])

    machine_name = USER_QPU
    backend = service.least_busy(operational=True, simulator=False, name=machine_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=USER_OPTIMISATION_LEVEL)
    isa_circuit = pm.run(circuit)

    with Session(backend=backend) as session:

        sampler = Sampler(session, options={"default_shots": USER_SHOTS})

        job = sampler.run([isa_circuit])
        print(f"[+]: Идентификатор Job_ID: {job.job_id()}")

        tmp_date = pd.Timestamp(job.metrics()["timestamps"]["created"]) + pd.Timedelta(hours=time_delta)
        create_year = tmp_date.strftime("%Y-%m-%d");   create_time = '{:%H:%M:%S}'.format(tmp_date)

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
        jbid_str_1 = f"\n[IDLE_INIT_X]\n[CREATED]:  {str(create_year)}" + "  " + str(create_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_2 = f"[ESTIMATE]: {str(estimate_start_year)}" + "  " + str(estimate_start_time) + "  " + job.job_id() + "  " + str(backend_name) + "\n"
        jbid_str_3 = f"[SHOTS]:   {shots}\n[ALPHA]:   {alpha}\n[IDLE]:   {str(use_IDLE)}\n[INIT]:   {str(use_INIT)}\n[XNOT]:   {str(use_X)}\n\n"
        csv_str_1 = "Project_Type,Status,Date,Time,JobID,Backend,Shots,Alpha,IDLE,INIT,XNOT"
        csv_str_2 = f"\nIDLE_INIT_X,CREATED,{create_year},{create_time},{job.job_id()},{backend_name},{shots},{alpha},{use_IDLE},{use_INIT},{use_X}"
        file_jbid.write(jbid_str_1);    file_jbid.write(jbid_str_2);    file_jbid.write(jbid_str_3);    file_jbid.close()
        if os.stat(csv_file_path_to_jbID).st_size == 0:  csv_file_jbid.write(csv_str_1)
        csv_file_jbid.write(csv_str_2); csv_file_jbid.close()

        res = job.result()
        data_pub = res[0].data

        qnt_seq = job.metrics()["usage"]["quantum_seconds"]
        usg_seq = job.metrics()["usage"]["seconds"]
        bss_seq = job.metrics()["bss"]["seconds"]

        for i in range(0, USER_QUBITS_AND_CLBITS):

            use_IDLE_local = True
            use_INIT_local = False
            use_X_local = False

            if usr_qubits_IDLE_2_1[i] in usr_qubits_INIT_2_2:
                use_INIT_local = True
            if usr_qubits_IDLE_2_1[i] in usr_qubits_X_2_3:
                use_X_local = True

            now = datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S")

            if i == 0:
                tmp_date = pd.Timestamp(job.metrics()["timestamps"]["running"]) + pd.Timedelta(hours=time_delta)
                running_year = tmp_date.strftime("%Y-%m-%d");  running_time = '{:%H:%M:%S}'.format(tmp_date)

                if (use_INIT == False) and (use_X == False):
                    USR_DIR_NAME_RESULT = PATH_TO_PROJECT_QIS + "IDLE_INIT_X/EXEC/" + str(running_year) + "/" + str(backend_name) + f"/IDLE/{shots}_{alpha}_{str(job.job_id())}"
                elif (use_INIT == True) and (use_X == False):
                    USR_DIR_NAME_RESULT = PATH_TO_PROJECT_QIS + "IDLE_INIT_X/EXEC/" + str(running_year) + "/" + str(backend_name) + f"/IDLE_INIT/{shots}_{alpha}_{str(job.job_id())}"
                elif (use_INIT == True) and (use_X == True):
                    USR_DIR_NAME_RESULT = PATH_TO_PROJECT_QIS + "IDLE_INIT_X/EXEC/" + str(running_year) + "/" + str(backend_name) + f"/IDLE_INIT_X/{shots}_{alpha}_{str(job.job_id())}"
                create_dir(USR_DIR_NAME_RESULT)  

                path_for_stats = PATH_TO_PROJECT_QIS + "IDLE_INIT_X/EXEC/" + f"STATs_{str(backend_name)}/"
                create_dir(path_for_stats)

                file_name_cnt_q = path_for_stats + "cnt_stats"
                first_str = (f"\n          Date    :: {str(running_year)}\n          Time    :: {str(running_time)} \
                            \n          Backend :: {str(backend_name)}\n          JobID   :: {str(job.job_id())}\n \
                            \n          Alpha   :: {str(alpha)}\n          Shots   :: {str(USER_SHOTS)}\n \
                            \n          [IDLE]   :: {str(use_IDLE)}\n          [INIT]   :: {str(use_INIT)}\n          [XNOT]   :: {str(use_X)}\n\n")
                file_cnt_q = open(file_name_cnt_q, "a")
                file_cnt_q.write("\n-----------------------------------------------------------");  file_cnt_q.write("\n-----------------------------------------------------------")
                file_cnt_q.write(first_str);    file_cnt_q.close()

                file_name_cnt_q_csv = path_for_stats + "cnt_stats.csv"
                if not os.path.exists(file_name_cnt_q_csv):
                    first_str_csv = "Date,Backend,JobID,Shots,Alpha,Qubit,P_Value,Zero,One,IDLE,INIT,XNOT,quantum_sec,usage_sec,bss_seq"
                    file_cnt_q_csv = open(file_name_cnt_q_csv, "a"); file_cnt_q_csv.write(first_str_csv)
                    file_cnt_q_csv.close()

                csv_file_local_by_type = '/'.join(USR_DIR_NAME_RESULT.split('/')[:-1]) + '/' + 'stats_local.csv'
                if not os.path.exists(csv_file_local_by_type):
                    first_str_csv = "Date,Backend,JobID,Shots,Alpha,Qubit,P_Value,Zero,One,IDLE,INIT,XNOT,quantum_sec,usage_sec,bss_seq"
                    file_cnt_q_csv = open(csv_file_local_by_type, "a"); file_cnt_q_csv.write(first_str_csv)
                    file_cnt_q_csv.close()

                csv_file_name_all_q = (USR_DIR_NAME_RESULT + f"/ALL_qubits_stats_{str(job.job_id())}.csv")
                csv_first_str = "Date,Backend,JobID,Shots,Alpha,Qubit,P_Value,Zero,One,IDLE,INIT,XNOT,quantum_sec,usage_sec,bss_seq"
                csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
                if os.stat(csv_file_name_all_q).st_size == 0:  csv_file_cnt_q_all.write(csv_first_str)
                csv_file_cnt_q_all.close()

            file_name = f'{usr_qubits_IDLE_2_1[i]}_' + time + "_" + machine_name + ".txt"

            bitstring = "".join(getattr(data_pub, f'c{usr_qubits_IDLE_2_1[i]}').get_bitstrings())

            counts = getattr(data_pub, f'c{usr_qubits_IDLE_2_1[i]}').get_counts()

            p_value = calculate_Pvalue(bitstring)

            try:    counts_zero = counts["0"]
            except Exception as ex: counts_zero = 0

            try:    counts_unity = counts["1"]
            except Exception as ex: counts_unity = 0

            csv_file_cnt_q_all = open(csv_file_name_all_q, "a")
            str_result = f"\n{running_year},{backend_name},{job.job_id()},"\
                                     f"{shots},{alpha},{usr_qubits_IDLE_2_1[i]},"\
                                     f"{p_value},{counts_zero},{counts_unity},"\
                                     f"{str(use_IDLE_local)},{str(use_INIT_local)},{str(use_X_local)},"\
                                      f"{qnt_seq},{usg_seq},{bss_seq}"
            csv_file_cnt_q_all.write(str_result)
            csv_file_cnt_q_all.close()

            dir_path = os.path.join(USR_DIR_NAME_RESULT + '/' + f'{usr_qubits_IDLE_2_1[i]}')   

            create_dir(dir_path)                        
            path = os.path.join(dir_path, file_name)    

            with open(path, 'w') as fd:
                fd.write(bitstring)
            fd.close()  

            file_cnt_q_csv = open(file_name_cnt_q_csv, "a");    file_cnt_q_csv.write(str_result)
            file_cnt_q_csv.close()

            file_cnt_q_csv = open(csv_file_local_by_type, "a");    file_cnt_q_csv.write(str_result)
            file_cnt_q_csv.close()

            print(f"\n[+]: Данные записаны в файл: '{file_name}'")

            print(f"[+]: '0' [{counts_zero}]")
            print(f"[+]: '1' [{counts_unity}]")
            print("[+]: p_value: ", p_value)

            file_cnt_q = open(file_name_cnt_q, "a")
            file_cnt_q.write(f"Кубит {usr_qubits_IDLE_2_1[i]} :: '0' : [{counts_zero}] :: '1' : [{counts_unity}]      :: p_value : {p_value}\n");   file_cnt_q.close()

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