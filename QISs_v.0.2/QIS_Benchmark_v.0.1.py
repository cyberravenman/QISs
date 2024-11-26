from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog
from debugpy.launcher import channel
from qiskit.pulse import qubit_channels
from sympy.abc import alpha
from PyQt5.QtWidgets import QFileDialog, QDialog

from src.QRNG import *
from src.QRNG_Simulator import *
from src.QPU_Info import *
from src.JobID import *

import subprocess

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread
from src.Test import Ui_MainWindow  
import sys

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))

class QPUBaseInfo1(QThread):

    def __init__(self, parent=None):
        super(QPUBaseInfo1, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.ibm_instance = ""              
        self.combo_box_Dynamic_INFO = None  
        self.combo_box_Dynamic_QRNG = None  

    def run(self):
        try:
            available_QPU_list = QPU_Available(self.ibm_channel, self.ibm_instance, self.token_name)
            for i in range(0, len(available_QPU_list)):
                self.combo_box_Dynamic_QRNG.addItem(str(available_QPU_list[i]).split("\'")[1])
                self.combo_box_Dynamic_INFO.addItem(str(available_QPU_list[i]).split("\'")[1])
        except Exception as ex: print(ex)
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
        QPU_More_Info(self.ibm_channel, self.ibm_instance, self.token_name, self.backend_name)
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
        Qubit_Info(self.ibm_channel, self.ibm_instance, self.token_name, self.backend_name, self.qubit_number)
class QPUSetMaxValueINFO(QThread):

    def __init__(self, parent=None):
        super(QPUSetMaxValueINFO, self).__init__(parent)

        self.value = 0

        self.token_name = ""        
        self.ibm_channel = ""       
        self.ibm_instance = ""      
        self.backend_name = ""      
        self.slider_INFO = None     

    def run(self):
        max_qubit = set_Num_of_Qubits(self.ibm_channel, self.ibm_instance, self.token_name, self.backend_name)
        self.slider_INFO.setMaximum(max_qubit-1)

class QRNGLaunch(QThread):

    def __init__(self, parent=None):
        super(QRNGLaunch, self).__init__(parent)

        self.value = 0

        self.token_name = ""        
        self.backend_name = ""      
        self.ibm_channel = ""       
        self.num_of_qubits = 0      
        self.alpha = 0.0            
        self.full_path_for_NIST = ""
        self.shots = 0              
        self.opt_level = 0          

    def run(self):
        try:
            self.full_path_for_NIST = Calc_QRNG(self.token_name, self.num_of_qubits, self.backend_name, self.ibm_channel, float(self.alpha), int(self.shots), int(self.opt_level))
            pass
        except:
            print("Что-то пошло не так. Программа не выполнена.")
class QRNGSimulatorLaunch(QThread):

    def __init__(self, parent=None):
        super(QRNGSimulatorLaunch, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.num_of_qubits = 0              
        self.alpha = 0.0                    
        self.full_path_for_NIST = ""        
        self.shots = 0                      
        self.opt_level = 0                  

    def run(self):
        self.full_path_for_NIST = Calc_QRNG_Simulator(self.token_name, self.num_of_qubits, self.ibm_channel, float(self.alpha), int(self.shots), int(self.opt_level))

class CheckJobStatus(QThread):
    def __init__(self, parent=None):
        super(CheckJobStatus, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     

    def run(self):
        try:
            Job_Status(self.token_name, self.ibm_channel, self.jobID)
        except:
            print("!!!Проверьте корректность введенных данных!!!")
class JobCancel(QThread):
    def __init__(self, parent=None):
        super(JobCancel, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     

    def run(self):
        try:
            Job_Cancel(self.token_name, self.ibm_channel, self.jobID)
            print(f"\nВыполнение программы '{self.jobID}' отменено.")
        except:
            print("\nОтмена не состоялась. Проверьте корректность введенных данных.")
class JobDownload(QThread):
    def __init__(self, parent=None):
        super(JobDownload, self).__init__(parent)

        self.value = 0

        self.token_name = ""                
        self.ibm_channel = ""               
        self.jobID = ""                     
        self.alpha = 0.0                    

    def run(self):
        try:
            Job_Download(self.token_name, self.ibm_channel, self.jobID, float(self.alpha))
            print(f"\nСкачивание результатов '{self.jobID}' завершено.")
        except:
            print("\nНе удалось скачать данные. Проверьте корректность введенных данных.")

class QPUSetMaxValueQRNG(QThread):

    def __init__(self, parent=None):
        super(QPUSetMaxValueQRNG, self).__init__(parent)

        self.value = 0

        self.token_name = ""    
        self.ibm_channel = ""   
        self.ibm_instance = ""  
        self.backend_name = ""  
        self.slider_QRNG = None 

    def run(self):
        max_qubit = set_Num_of_Qubits(self.ibm_channel, self.ibm_instance, self.token_name, self.backend_name)
        self.slider_QRNG.setMaximum(max_qubit)
        self.slider_QRNG.setMinimum(1)

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        sys.stdout = Stream(newText=self.onUpdateText)
        sys.stderr = Stream(newText=self.onUpdateText)

        self.ui.lineEdit_API_Token.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.lineEdit_API_Token.setText(
            "")
        self.ui.lineEdit_Channel.setText("ibm_quantum")
        self.ui.lineEdit_Instance.setText("ibm-q/open/main")

        self.ui.frame_QRNG_Simulator.setEnabled(False)
        self.ui.frame_NIST.setEnabled(False)

        self.ui.radioButton_QRNG_Check.clicked.connect(self.rdQRNG)
        self.ui.radioButton_QRNG_Simulator_Check.clicked.connect(self.rdQRNGSim)
        self.ui.radioButton_NIST_Check.clicked.connect(self.rdNIST)

        self.ui.pushButton_QPU_Available.clicked.connect(self.btnClicked_QPU_Available)
        self.QPU_info = QPUBaseInfo1() 

        self.ui.comboBox_INFO_QPU_List.activated[str].connect(self.combobox_INFO_QPU_Changed)
        self.QPU_INFO_Change_Value = QPUSetMaxValueINFO()

        self.ui.pushButton_QPU_Characteristics.clicked.connect(self.btnClicked_QPU_Characteristics)
        self.QPU_info_2 = QPUBaseInfo2() 

        self.ui.pushButton_INFO_Get_Info_on_Qubit.clicked.connect(self.btnClicked_INFO_on_Qubit)
        self.QPU_Qubit_Info = QPUQubitInfo() 

        self.ui.comboBox_QRNG_QPU_List.activated[str].connect(self.combobox_QRNG_QPU_Changed)
        self.QPU_QRNG_Change_Value = QPUSetMaxValueQRNG()

        self.ui.pushButton_QRNG_Start.clicked.connect(self.btnClicked_QRNG_Start)
        self.QRNG_process = QRNGLaunch() 

        self.ui.pushButton_QRNG_SIMULATO_Start.clicked.connect(self.btnClicked_QRNG_SIMULATOR_Start)
        self.QRNG_Simulator_process = QRNGSimulatorLaunch() 

        self.ui.pushButton_QRNG_JobID_Check.clicked.connect(self.btnClicked_QRNG_JobID_Check)
        self.Check_JobID = CheckJobStatus()

        self.ui.pushButton_QRNG_JobID_Cancel.clicked.connect(self.btnClicked_QRNG_JobID_Cancel)
        self.Cancel_JobID = JobCancel()

        self.ui.pushButton_QRNG_JobID_Download.clicked.connect(self.btnClicked_QRNG_JobID_Download)
        self.Download_JobID = JobDownload()

        self.ui.pushButton_Path_for_NIST_Dialog.clicked.connect(self.btnClicked_NIST_Path_to_File)

        self.ui.pushButton_NIST_Start.clicked.connect(self.btnClicked_NIST_Start)

    def onUpdateText(self, text):
        self.ui.textEdit_QRNG_Output.insertPlainText(text)
        self.ui.textEdit_QRNG_Output.moveCursor(QtGui.QTextCursor.End) 

        self.ui.textEdit_Console_Output.insertPlainText(text)
        self.ui.textEdit_Console_Output.moveCursor(QtGui.QTextCursor.End)  
    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def combobox_INFO_QPU_Changed(self):

        self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
        self.ui.pushButton_QPU_Available.setEnabled(False)              
        self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
        self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.QPU_INFO_Change_Value.slider_INFO = self.ui.horizontalSlider_INFO_Num_of_Qubits    
        self.QPU_INFO_Change_Value.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()  
        self.QPU_INFO_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_INFO_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_INFO_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_QRNG_Output.clear()            
        self.QPU_INFO_Change_Value.finished.connect(self.INFO_combobox_onFinished)      
        self.QPU_INFO_Change_Value.start()                                              

    def INFO_combobox_onFinished(self):  
        self.ui.comboBox_INFO_QPU_List.setEnabled(True)                 
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(True)      
        self.ui.pushButton_QPU_Available.setEnabled(True)               
        self.ui.pushButton_QPU_Characteristics.setEnabled(True)         
        self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             

    def btnClicked_QPU_Available(self):

        self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
        self.ui.pushButton_QPU_Available.setEnabled(False)              
        self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
        self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.QPU_info.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_info.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_info.token_name = self.ui.lineEdit_API_Token.text()               
        self.QPU_info.combo_box_Dynamic_INFO = self.ui.comboBox_INFO_QPU_List      
        self.QPU_info.combo_box_Dynamic_QRNG = self.ui.comboBox_QRNG_QPU_List      

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_QRNG_Output.clear()            
        self.QPU_info.finished.connect(self.INFO_onFinished)      
        self.QPU_info.start()                                     

    def btnClicked_QPU_Characteristics(self):
        if self.ui.comboBox_INFO_QPU_List.currentText() != "":

            self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
            self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
            self.ui.pushButton_QPU_Available.setEnabled(False)              
            self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
            self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   
            self.ui.tab_QRNG.setEnabled(False)                              
            self.ui.tab_QKD.setEnabled(False)                               
            self.ui.tab_Fourie.setEnabled(False)                            

            self.QPU_info_2.ibm_channel = self.ui.lineEdit_Channel.text()               
            self.QPU_info_2.ibm_instance = self.ui.lineEdit_Instance.text()             
            self.QPU_info_2.token_name = self.ui.lineEdit_API_Token.text()              
            self.QPU_info_2.backend_name = self.ui.comboBox_INFO_QPU_List.currentText() 

            self.ui.textEdit_Console_Output.clear()  
            self.ui.textEdit_QRNG_Output.clear()  
            self.QPU_info_2.finished.connect(self.INFO_onFinished)      
            self.QPU_info_2.start()                                     
        else:
            print("Выберите КВУ.")

    def btnClicked_INFO_on_Qubit(self):
        if self.ui.comboBox_INFO_QPU_List.currentText() != "":

            self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
            self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
            self.ui.pushButton_QPU_Available.setEnabled(False)              
            self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
            self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   
            self.ui.tab_QRNG.setEnabled(False)                              
            self.ui.tab_QKD.setEnabled(False)                               
            self.ui.tab_Fourie.setEnabled(False)                            

            self.QPU_Qubit_Info.ibm_channel = self.ui.lineEdit_Channel.text()  
            self.QPU_Qubit_Info.ibm_instance = self.ui.lineEdit_Instance.text()  
            self.QPU_Qubit_Info.token_name = self.ui.lineEdit_API_Token.text()  
            self.QPU_Qubit_Info.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()  
            self.QPU_Qubit_Info.qubit_number = self.ui.horizontalSlider_INFO_Num_of_Qubits.value()

            self.ui.textEdit_Console_Output.clear()  
            self.ui.textEdit_QRNG_Output.clear()  
            self.QPU_Qubit_Info.finished.connect(self.INFO_onFinished)  
            self.QPU_Qubit_Info.start()                                 

        else:
            print("Выберите КВУ.")

    def INFO_onFinished(self):
        self.ui.comboBox_INFO_QPU_List.setEnabled(True)                 
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(True)      
        self.ui.pushButton_QPU_Available.setEnabled(True)               
        self.ui.pushButton_QPU_Characteristics.setEnabled(True)         
        if self.ui.comboBox_INFO_QPU_List.currentText() != "": self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(True)    
        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.tab_QRNG.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             

    def rdQRNG(self):
        self.ui.frame_NIST.setEnabled(False)
        self.ui.frame_QRNG_Simulator.setEnabled(False)
        self.ui.frame_QRNG.setEnabled(True)

        if self.ui.comboBox_QRNG_QPU_List.currentText() != "":
            self.ui.pushButton_QRNG_Start.setEnabled(True)
    def rdQRNGSim(self):
        self.ui.frame_NIST.setEnabled(False)
        self.ui.frame_QRNG_Simulator.setEnabled(True)
        self.ui.frame_QRNG.setEnabled(False)
    def rdNIST(self):
        self.ui.frame_NIST.setEnabled(True)
        self.ui.frame_QRNG_Simulator.setEnabled(False)
        self.ui.frame_QRNG.setEnabled(False)

    def combobox_QRNG_QPU_Changed(self):

        self.ui.comboBox_QRNG_QPU_List.setEnabled(False)                
        self.ui.pushButton_QRNG_Start.setEnabled(False)                 
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(False)        
        self.ui.pushButton_NIST_Start.setEnabled(False)                 
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)   
        self.ui.tab_Init.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.QPU_QRNG_Change_Value.slider_QRNG = self.ui.horizontalSlider_QRNG_Num_of_Qubits    
        self.QPU_QRNG_Change_Value.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()  
        self.QPU_QRNG_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_QRNG_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_QRNG_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_QRNG_Output.clear()            
        self.QPU_QRNG_Change_Value.finished.connect(self.QRNG_comboBox_onFinished)      
        self.QPU_QRNG_Change_Value.start()                                     

    def QRNG_comboBox_onFinished(self):  
        self.ui.pushButton_NIST_Start.setEnabled(True)                  
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)    
        self.ui.pushButton_QRNG_Start.setEnabled(True)                  
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(True)         
        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.tab_Init.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             

    def btnClicked_QRNG_Start(self):

        self.ui.comboBox_QRNG_QPU_List.setEnabled(False)                
        self.ui.pushButton_QRNG_Start.setEnabled(False)                 
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(False)        
        self.ui.pushButton_NIST_Start.setEnabled(False)                 
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)   
        self.ui.tab_Init.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.QRNG_process.token_name = self.ui.lineEdit_API_Token.text()                        
        self.QRNG_process.ibm_channel = self.ui.lineEdit_Channel.text()                         
        self.QRNG_process.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()           
        self.QRNG_process.num_of_qubits = self.ui.horizontalSlider_QRNG_Num_of_Qubits.value()   
        self.QRNG_process.alpha = self.ui.lineEdit_ALPHA.text()                                 
        self.QRNG_process.shots = self.ui.lineEdit_QRNG_Shots.text()                            
        self.QRNG_process.opt_level = self.ui.lineEdit_QRNG_OptLevel.text()                     

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_QRNG_Output.clear()            

        self.QRNG_process.finished.connect(self.QRNG_onFinished)      
        self.QRNG_process.start()                                     

    def QRNG_onFinished(self):  
        self.ui.pushButton_NIST_Start.setEnabled(True)                  
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)    
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(True)         
        self.ui.pushButton_QRNG_Start.setEnabled(True)                  
        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.tab_Init.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_process.full_path_for_NIST))  

    def btnClicked_QRNG_SIMULATOR_Start(self):

        self.ui.comboBox_QRNG_QPU_List.setEnabled(False)                
        self.ui.pushButton_QRNG_Start.setEnabled(False)                 
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(False)        
        self.ui.pushButton_NIST_Start.setEnabled(False)                 
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)   
        self.ui.tab_Init.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.QRNG_Simulator_process.token_name = self.ui.lineEdit_API_Token.text()                          
        self.QRNG_Simulator_process.ibm_channel = self.ui.lineEdit_Channel.text()                           
        self.QRNG_Simulator_process.num_of_qubits = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.value()   
        self.QRNG_Simulator_process.alpha = self.ui.lineEdit_ALPHA.text()                                   
        self.QRNG_Simulator_process.shots = self.ui.lineEdit_QRNG_Shots.text()                              
        self.QRNG_Simulator_process.opt_level = self.ui.lineEdit_QRNG_OptLevel.text()                       

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_QRNG_Output.clear()            
        self.QRNG_Simulator_process.finished.connect(self.QRNG_Simulator_onFinished)      
        self.QRNG_Simulator_process.start()                                     

    def QRNG_Simulator_onFinished(self):  
        self.ui.pushButton_NIST_Start.setEnabled(True)                  
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)    
        self.ui.pushButton_QRNG_Start.setEnabled(True)                  
        self.ui.pushButton_QRNG_SIMULATO_Start.setEnabled(True)         
        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.tab_Init.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_Simulator_process.full_path_for_NIST)) 

    def btnClicked_QRNG_JobID_Check(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Check_JobID.token_name = self.ui.lineEdit_API_Token.text()                        
        self.Check_JobID.ibm_channel = self.ui.lineEdit_Channel.text()                         
        self.Check_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()                            

        self.Check_JobID.finished.connect(self.JobID_onFinished)
        self.Check_JobID.start()

    def btnClicked_QRNG_JobID_Cancel(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Cancel_JobID.token_name = self.ui.lineEdit_API_Token.text()  
        self.Cancel_JobID.ibm_channel = self.ui.lineEdit_Channel.text()  
        self.Cancel_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()  

        self.Cancel_JobID.finished.connect(self.JobID_onFinished)
        self.Cancel_JobID.start()

    def btnClicked_QRNG_JobID_Download(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Download_JobID.token_name = self.ui.lineEdit_API_Token.text()  
        self.Download_JobID.ibm_channel = self.ui.lineEdit_Channel.text()   
        self.Download_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()      
        self.Download_JobID.alpha = self.ui.lineEdit_ALPHA.text()           

        self.Download_JobID.finished.connect(self.JobID_onFinished)
        self.Download_JobID.start()

    def JobID_onFinished(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(True)            
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(True)    
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(True)   
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(True) 

    def btnClicked_NIST_Path_to_File(self):

        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Select", options=QtWidgets.QFileDialog.DontUseNativeDialog)

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(folder_path))

        flag = False
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_size = os.path.getsize(os.path.join(root, file))
                    self.ui.lineEdit_NIST_Key_Length.setText(str(file_size))
                    flag = True; break
            if flag: break

    def btnClicked_NIST_Start(self):
        self.ui.textEdit_Console_Output.clear()     
        self.ui.textEdit_QRNG_Output.clear()        

        print("-----ПРОВЕРКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ ТЕСТАМИ NIST STS-----\n")

        bash_command = "./NIST/auto_test_v.2.1.sh"
        arg1 = self.ui.lineEdit_NIST_Directory_to_Dataset.text()    
        arg2 = self.ui.lineEdit_NIST_Key_Length.text()              
        arg3 = self.ui.lineEdit_NIST_Tests_Supplys.text()           
        arg4 = self.ui.lineEdit_NIST_Parameters_on_Default.text()   
        arg5 = self.ui.lineEdit_NIST_Num_of_Bitstream.text()        
        arg6 = self.ui.lineEdit_NIST_Format_of_Data.text()          
        args = [arg1, arg2, arg3, arg4, arg5, arg6]                 

        try:
            result = subprocess.run([bash_command] + args, capture_output=True, text=True)

            print(result.stdout)
            print(result.stderr)
        except:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.")
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
