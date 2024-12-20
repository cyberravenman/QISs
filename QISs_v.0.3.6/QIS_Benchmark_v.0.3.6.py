import time

from IPython.external.qt_for_kernel import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog, QApplication

from src.TAB_1.Gen_Scheme import GenerateScheme
from src.TAB_2.NIST_STS import NISTLaunch
from src.TAB_5.Bitmap import BitmapLaunch
from src.TAB_5.Fcorrelation import FCorrEasy, FCorrProfi
from src.gui import Ui_MainWindow
from src.TAB_0.QPU_Info import *
from src.TAB_1.IDLE_INIT_H import *
from src.TAB_1.JobID import *
from src.TAB_2.QRNG import *
from src.TAB_2.QRNG_Simulator import *
from src.TAB_2.JobID import *
import sys
import matplotlib.pyplot as plt
from scipy import special
import subprocess

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        sys.stdout = Stream(newText=self.onUpdateText)
        sys.stderr = Stream(newText=self.onUpdateText)

        self.ui.radioButton_BASE.clicked.connect(self.rdBASE)
        self.ui.radioButton_PROFESSIONAL.clicked.connect(self.rdPROFI)

        self.ui.tabWidget_PARENT.setTabVisible(1, False)
        self.ui.tabWidget_PARENT.setTabVisible(2, False)
        self.ui.tabWidget_PARENT.setTabVisible(3, False)
        self.ui.tabWidget_PARENT.setTabVisible(4, False)
        self.ui.tabWidget_PARENT.setTabVisible(5, False)

        self.ui.lineEdit_API_Token.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.lineEdit_API_Token.setText("")
        self.ui.lineEdit_Channel.setText("ibm_quantum")
        self.ui.lineEdit_Instance.setText("ibm-q/open/main")

        self.ui.pushButton_QPU_Available.clicked.connect(self.btnClicked_QPU_Available)
        self.QPU_info = QPUBaseInfo1() 

        self.ui.pushButton_QPU_Characteristics.clicked.connect(self.btnClicked_QPU_Characteristics)
        self.QPU_info_2 = QPUBaseInfo2() 

        self.ui.pushButton_INFO_Get_Info_on_Qubit.clicked.connect(self.btnClicked_INFO_on_Qubit)
        self.QPU_Qubit_Info = QPUQubitInfo() 

        self.ui.comboBox_INFO_QPU_List.activated[str].connect(self.combobox_INFO_QPU_Changed)
        self.QPU_INFO_Change_Value = QPUChangedComboBoxINFO()

        self.ui.comboBox_TAB2_QPU_List.activated[str].connect(self.combobox_TAB2_QPU_Changed)
        self.QPU_TAB2_Change_Value = QPUChangedComboBoxTAB2()

        self.ui.radioButton_TAB2_Slider_1_OK.clicked.connect(self.rdTAB2_Slider_2_1)
        self.ui.radioButton_TAB2_ListWidget_1_OK.clicked.connect(self.rdTAB2_listWidget_2_1)

        self.ui.radioButton_TAB2_Slider_2_OK.clicked.connect(self.rdTAB2_Slider_2_2)
        self.ui.radioButton_TAB2_ListWidget_2_OK.clicked.connect(self.rdTAB2_listWidget_2_2)

        self.ui.radioButton_TAB2_Slider_3_OK.clicked.connect(self.rdTAB2_Slider_2_3)
        self.ui.radioButton_TAB2_ListWidget_3_OK.clicked.connect(self.rdTAB2_listWidget_2_3)

        self.ui.horizontalSlider_TAB2_IDLE.valueChanged.connect(self.slider_TAB2_Changed_1)
        self.Slider_TAB2_Change_Value_1 = SliderTAB2Changed()

        self.ui.horizontalSlider_TAB2_INIT.valueChanged.connect(self.slider_TAB2_Changed_2)
        self.Slider_TAB2_Change_Value_2 = SliderTAB2Changed()

        self.ui.horizontalSlider_TAB2_H.valueChanged.connect(self.slider_TAB2_Changed_3)
        self.Slider_TAB2_Change_Value_3 = SliderTAB2Changed()

        self.ui.pushButton_TAB2_Generate_Scheme.clicked.connect(self.btnClicked_TAB2_Gen_Scheme)
        self.TAB2_Generate_Scheme = GenerateScheme()

        self.ui.pushButton_TAB2_JobID_Info.clicked.connect(self.btnClicked_TAB2_JobID_Check)
        self.Check_JobID_TAB2 = CheckJobStatusTAB2()

        self.ui.pushButton_TAB2_JobID_Cancell.clicked.connect(self.btnClicked_TAB2_JobID_Cancel)
        self.Cancel_JobID_TAB2 = JobCancelTAB2()

        self.ui.pushButton_TAB2_JobID_Result.clicked.connect(self.btnClicked_TAB2_JobID_Download)
        self.Download_JobID_TAB2 = JobDownloadTAB2()

        self.ui.frame_QRNG_Simulator.setEnabled(False)
        self.ui.frame_NIST.setEnabled(False)

        self.ui.radioButton_QRNG_Check.clicked.connect(self.rdQRNG)
        self.ui.radioButton_QRNG_Simulator_Check.clicked.connect(self.rdQRNGSim)
        self.ui.radioButton_NIST_Check.clicked.connect(self.rdNIST)

        self.ui.radioButton_QRNG_Slider_OK.clicked.connect(self.rdQRNGSlider)
        self.ui.radioButton_QRNG_listWidget_OK.clicked.connect(self.rdQRNGListWidget)

        self.ui.radioButton_QRNG_Sim_Slider_OK.clicked.connect(self.rdQRNGSimSlider)
        self.ui.radioButton_QRNG_Sim_listWidget_OK.clicked.connect(self.rdQRNGSimListWidget)

        for i in range(0, self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.maximum()):
            item_3_2 = QtWidgets.QListWidgetItem(); item_3_2.setText(f'Кубит {i}'); item_3_2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_3_2.setCheckState(QtCore.Qt.Unchecked) 
            self.ui.listWidget_QRNG_Sim_Check_Qubits.addItem(item_3_2)
        self.ui.listWidget_QRNG_Sim_Check_Qubits.item(0).setCheckState(QtCore.Qt.Checked)

        self.ui.pushButton_QRNG_Start.clicked.connect(self.btnClicked_QRNG_Start)
        self.QRNG_process = QRNGLaunch() 

        self.ui.comboBox_QRNG_QPU_List.activated[str].connect(self.combobox_QRNG_QPU_Changed)
        self.QPU_QRNG_Change_Value = QPUChangedComboBoxQRNG()

        self.ui.horizontalSlider_QRNG_Num_of_Qubits.valueChanged.connect(self.slider_QRNG_Changed)
        self.Slider_QRNG_Change_Value = SliderQRNGChanged()

        self.ui.pushButton_QRNG_JobID_Check.clicked.connect(self.btnClicked_QRNG_JobID_Check)
        self.Check_JobID = CheckJobStatus()

        self.ui.pushButton_QRNG_JobID_Cancel.clicked.connect(self.btnClicked_QRNG_JobID_Cancel)
        self.Cancel_JobID = JobCancel()

        self.ui.pushButton_QRNG_JobID_Download.clicked.connect(self.btnClicked_QRNG_JobID_Download)
        self.Download_JobID = JobDownload()

        self.ui.pushButton_QRNG_SIMULATO_Start.clicked.connect(self.btnClicked_QRNG_SIMULATOR_Start)
        self.QRNG_Simulator_process = QRNGSimulatorLaunch()  

        self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.valueChanged.connect(self.slider_QRNG_Sim_Changed)
        self.Slider_QRNG_Sim_Change_Value = SliderQRNGSimChanged()

        self.ui.pushButton_NIST_Start.clicked.connect(self.btnClicked_NIST_Start)
        self.NIST_process = NISTLaunch()

        self.ui.pushButton_Path_for_NIST_Dialog.clicked.connect(self.btnClicked_NIST_Path_to_File)

        self.ui.pushButton_TAB5_Path_for_Bitmap_DIALOG.clicked.connect(self.btnClicked_BITMAP_Path_to_File)
        self.ui.pushButton_TAB5_Calculate_Bitmap.clicked.connect(self.btnClicked_BITMAP_Start)
        self.Bitmap_process = BitmapLaunch()

        self.ui.pushButton_TAB5_Seq1_Dialog_easy.clicked.connect(self.btnClicked_Fcorr_Seq1_easy)
        self.ui.pushButton_TAB5_Seq2_Dialog_easy.clicked.connect(self.btnClicked_Fcorr_Seq2_easy)

        self.ui.pushButton_TAB5_Fcorrelation_easy.clicked.connect(self.btnClicked_Fcorr_calculate_easy)
        self.FCorrEasy_process = FCorrEasy()

        self.ui.pushButton_TAB5_Seq1_Dialog_profi.clicked.connect(self.btnClicked_Fcorr_Seq1_profi)
        self.ui.pushButton_TAB5_Seq2_Dialog_profi.clicked.connect(self.btnClicked_Fcorr_Seq2_profi)

        self.ui.pushButton_TAB5_Fcorrelation_profi.clicked.connect(self.btnClicked_Fcorr_calculate_profi)
        self.FCorrProfi_process = FCorrProfi()

    def onUpdateText(self, text):
        self.ui.textEdit_QRNG_Output.insertPlainText(text)
        self.ui.textEdit_QRNG_Output.moveCursor(QtGui.QTextCursor.End) 

        self.ui.textEdit_TAB2.insertPlainText(text)
        self.ui.textEdit_TAB2.moveCursor(QtGui.QTextCursor.End) 

        self.ui.textEdit_Console_Output.insertPlainText(text)
        self.ui.textEdit_Console_Output.moveCursor(QtGui.QTextCursor.End)  

        self.ui.textEdit_TAB5.insertPlainText(text)
        self.ui.textEdit_TAB5.moveCursor(QtGui.QTextCursor.End)  
    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def rdBASE(self):
        if self.ui.radioButton_BASE.isChecked():
            self.ui.tabWidget_PARENT.setTabVisible(1, False)
            self.ui.tabWidget_PARENT.setTabVisible(2, False)
            self.ui.tabWidget_PARENT.setTabVisible(3, False)
            self.ui.tabWidget_PARENT.setTabVisible(4, False)
            self.ui.tabWidget_PARENT.setTabVisible(5, True)

    def rdPROFI(self):
        if self.ui.radioButton_PROFESSIONAL.isChecked():
            self.ui.tabWidget_PARENT.setTabVisible(1, True)
            self.ui.tabWidget_PARENT.setTabVisible(2, True)
            self.ui.tabWidget_PARENT.setTabVisible(3, True)
            self.ui.tabWidget_PARENT.setTabVisible(4, True)
            self.ui.tabWidget_PARENT.setTabVisible(5, True)

    def btnClicked_QPU_Available(self):

        self.ui.comboBox_INFO_QPU_List.clear()
        self.ui.comboBox_QRNG_QPU_List.clear()
        self.ui.comboBox_TAB2_QPU_List.clear()

        self.ui.horizontalSlider_INFO_Num_of_Qubits.setMaximum(0)
        self.ui.horizontalSlider_TAB2_IDLE.setMaximum(0)
        self.ui.horizontalSlider_TAB2_INIT.setMaximum(0)
        self.ui.horizontalSlider_TAB2_H.setMaximum(0)
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setMaximum(0)

        self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
        self.ui.pushButton_QPU_Available.setEnabled(False)              
        self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
        self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   

        self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            
        self.ui.tab_Instruments.setEnabled(False)                       

        self.QPU_info.ibm_channel = self.ui.lineEdit_Channel.text()                         
        self.QPU_info.ibm_instance = self.ui.lineEdit_Instance.text()                       
        self.QPU_info.token_name = self.ui.lineEdit_API_Token.text()                        
        self.QPU_info.combo_box_Dynamic_INFO = self.ui.comboBox_INFO_QPU_List               
        self.QPU_info.combo_box_Dynamic_INIT_IDLE_H = self.ui.comboBox_TAB2_QPU_List        
        self.QPU_info.combo_box_Dynamic_QRNG = self.ui.comboBox_QRNG_QPU_List               

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_TAB2.clear()                   
        self.ui.textEdit_QRNG_Output.clear()            
        self.ui.textEdit_TAB5.clear()                   

        self.QPU_info.finished.connect(self.onFinished_INFO)      
        self.QPU_info.start()  

    def btnClicked_QPU_Characteristics(self):
        if self.ui.comboBox_INFO_QPU_List.currentText() != "":

            self.ui.comboBox_INFO_QPU_List.setEnabled(False)                
            self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)     
            self.ui.pushButton_QPU_Available.setEnabled(False)              
            self.ui.pushButton_QPU_Characteristics.setEnabled(False)        
            self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)   

            self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
            self.ui.tab_QRNG.setEnabled(False)                              
            self.ui.tab_QKD.setEnabled(False)                               
            self.ui.tab_Fourie.setEnabled(False)                            
            self.ui.tab_Instruments.setEnabled(False)                       

            self.QPU_info_2.ibm_channel = self.ui.lineEdit_Channel.text()               
            self.QPU_info_2.ibm_instance = self.ui.lineEdit_Instance.text()             
            self.QPU_info_2.token_name = self.ui.lineEdit_API_Token.text()              
            self.QPU_info_2.backend_name = self.ui.comboBox_INFO_QPU_List.currentText() 

            self.ui.textEdit_Console_Output.clear()                     
            self.ui.textEdit_TAB2.clear()                               
            self.ui.textEdit_QRNG_Output.clear()                        
            self.ui.textEdit_TAB5.clear()                               

            self.QPU_info_2.finished.connect(self.onFinished_INFO)      
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

            self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
            self.ui.tab_QRNG.setEnabled(False)                              
            self.ui.tab_QKD.setEnabled(False)                               
            self.ui.tab_Fourie.setEnabled(False)                            
            self.ui.tab_Instruments.setEnabled(False)                       

            self.QPU_Qubit_Info.ibm_channel = self.ui.lineEdit_Channel.text()                       
            self.QPU_Qubit_Info.ibm_instance = self.ui.lineEdit_Instance.text()                     
            self.QPU_Qubit_Info.token_name = self.ui.lineEdit_API_Token.text()                      
            self.QPU_Qubit_Info.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()         
            self.QPU_Qubit_Info.qubit_number = self.ui.horizontalSlider_INFO_Num_of_Qubits.value()  

            self.ui.textEdit_Console_Output.clear()                     
            self.ui.textEdit_TAB2.clear()                               
            self.ui.textEdit_QRNG_Output.clear()                        
            self.ui.textEdit_TAB5.clear()                               

            self.QPU_Qubit_Info.finished.connect(self.onFinished_INFO)  
            self.QPU_Qubit_Info.start()                                 

        else:
            print("Выберите КВУ.")

    def onFinished_INFO(self):
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(True)      
        self.ui.pushButton_QPU_Available.setEnabled(True)               
        self.ui.pushButton_QPU_Characteristics.setEnabled(True)         
        if self.ui.comboBox_INFO_QPU_List.currentText() != "": self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(True)    

        self.ui.tab_INIT_IDLE_H.setEnabled(True)                        
        self.ui.tab_QRNG.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             
        self.ui.tab_Instruments.setEnabled(True)                        

        if self.ui.comboBox_INFO_QPU_List.count() != 0:
            self.ui.comboBox_INFO_QPU_List.setEnabled(True)             

            self.ui.comboBox_TAB2_QPU_List.setEnabled(True)        
            self.ui.comboBox_QRNG_QPU_List.setEnabled(True)             

    def combobox_INFO_QPU_Changed(self):

        self.ui.comboBox_INFO_QPU_List.setEnabled(False)                    
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(False)         
        self.ui.pushButton_QPU_Available.setEnabled(False)                  
        self.ui.pushButton_QPU_Characteristics.setEnabled(False)            
        self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(False)       

        self.ui.tab_INIT_IDLE_H.setEnabled(False)           
        self.ui.tab_QRNG.setEnabled(False)                  
        self.ui.tab_QKD.setEnabled(False)                   
        self.ui.tab_Fourie.setEnabled(False)                
        self.ui.tab_Instruments.setEnabled(False)           

        self.QPU_INFO_Change_Value.slider_INFO = self.ui.horizontalSlider_INFO_Num_of_Qubits    

        self.QPU_INFO_Change_Value.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()  
        self.QPU_INFO_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_INFO_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_INFO_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               

        self.ui.textEdit_Console_Output.clear()                                     
        self.ui.textEdit_TAB2.clear()                                               
        self.ui.textEdit_QRNG_Output.clear()                                        
        self.ui.textEdit_TAB5.clear()                                               

        self.QPU_INFO_Change_Value.finished.connect(self.onFinished_INFO_combobox)  
        self.QPU_INFO_Change_Value.start()                                          

    def onFinished_INFO_combobox(self):  
        self.ui.comboBox_INFO_QPU_List.setEnabled(True)                 
        self.ui.pushButton_INFO_Get_Info_on_Qubit.setEnabled(True)      
        self.ui.pushButton_QPU_Available.setEnabled(True)               
        self.ui.pushButton_QPU_Characteristics.setEnabled(True)         
        if self.ui.horizontalSlider_INFO_Num_of_Qubits.maximum() != 0:
            self.ui.horizontalSlider_INFO_Num_of_Qubits.setEnabled(True)    

        self.ui.tab_INIT_IDLE_H.setEnabled(True)                        
        self.ui.tab_QRNG.setEnabled(True)                               
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             
        self.ui.tab_Instruments.setEnabled(True)                        

    def combobox_TAB2_QPU_Changed(self):

        self.ui.horizontalSlider_TAB2_IDLE.setMinimum(0);   self.ui.horizontalSlider_TAB2_IDLE.setMaximum(0)
        self.ui.horizontalSlider_TAB2_INIT.setMinimum(0);   self.ui.horizontalSlider_TAB2_INIT.setMaximum(0)
        self.ui.horizontalSlider_TAB2_H.setMinimum(0);      self.ui.horizontalSlider_TAB2_H.setMaximum(0)
        self.ui.listWidget_TAB2_IDLE.clear();   self.ui.listWidget_TAB2_INIT.clear();   self.ui.listWidget_TAB2_H.clear()

        self.ui.comboBox_TAB2_QPU_List.setEnabled(False)                
        self.ui.frame_TAB2_List_and_Slider.setEnabled(False)            

        self.ui.tab_INFO.setEnabled(False)                              
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            
        self.ui.tab_Instruments.setEnabled(False)                       

        self.QPU_TAB2_Change_Value.list_widget_2_1 = self.ui.listWidget_TAB2_IDLE           
        self.QPU_TAB2_Change_Value.list_widget_2_2 = self.ui.listWidget_TAB2_INIT           
        self.QPU_TAB2_Change_Value.list_widget_2_3 = self.ui.listWidget_TAB2_H              

        self.QPU_TAB2_Change_Value.slider_QRNG_2_1 = self.ui.horizontalSlider_TAB2_IDLE     
        self.QPU_TAB2_Change_Value.slider_QRNG_2_2 = self.ui.horizontalSlider_TAB2_INIT     
        self.QPU_TAB2_Change_Value.slider_QRNG_2_3 = self.ui.horizontalSlider_TAB2_H        

        self.QPU_TAB2_Change_Value.spinBox_max_shots = self.ui.spinBox_INIT_IDLE_max_shots  

        self.QPU_TAB2_Change_Value.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()  
        self.QPU_TAB2_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_TAB2_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_TAB2_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               

        self.ui.textEdit_Console_Output.clear()     
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_QRNG_Output.clear()        
        self.ui.textEdit_TAB5.clear()               

        self.QPU_TAB2_Change_Value.finished.connect(self.onFinished_TAB2_QPU_Changed)       
        self.QPU_TAB2_Change_Value.start()                                                  

    def onFinished_TAB2_QPU_Changed(self):
        if (self.ui.radioButton_TAB2_Slider_1_OK.isChecked()) & (self.ui.horizontalSlider_TAB2_IDLE.maximum() != 0):
            self.ui.horizontalSlider_TAB2_IDLE.setEnabled(True)
        if (self.ui.radioButton_TAB2_Slider_2_OK.isChecked()) & (self.ui.horizontalSlider_TAB2_INIT.maximum() != 0):
            self.ui.horizontalSlider_TAB2_INIT.setEnabled(True)
        if (self.ui.radioButton_TAB2_Slider_3_OK.isChecked()) & (self.ui.horizontalSlider_TAB2_H.maximum() != 0):
            self.ui.horizontalSlider_TAB2_H.setEnabled(True)

        self.ui.tab_INFO.setEnabled(True)               
        self.ui.tab_QRNG.setEnabled(True)               
        self.ui.tab_QKD.setEnabled(True)                
        self.ui.tab_Fourie.setEnabled(True)             
        self.ui.tab_Instruments.setEnabled(True)       

        self.ui.comboBox_TAB2_QPU_List.setEnabled(True)             
        self.ui.frame_TAB2_List_and_Slider.setEnabled(True)         
        self.ui.pushButton_TAB2_Generate_Scheme.setEnabled(True)    

        self.ui.spinBox_INIT_IDLE_max_shots.setValue(self.ui.spinBox_INIT_IDLE_max_shots.maximum()) 

    def rdTAB2_Slider_2_1(self):
        if self.ui.radioButton_TAB2_Slider_1_OK.isChecked():
            self.ui.listWidget_TAB2_IDLE.setEnabled(False)
            if (self.ui.comboBox_TAB2_QPU_List.currentText() != "") & (self.ui.horizontalSlider_TAB2_IDLE.maximum() != 0):
                self.ui.horizontalSlider_TAB2_IDLE.setEnabled(True)
    def rdTAB2_listWidget_2_1(self):
        if self.ui.radioButton_TAB2_ListWidget_1_OK.isChecked():
            self.ui.listWidget_TAB2_IDLE.setEnabled(True)
            self.ui.horizontalSlider_TAB2_IDLE.setEnabled(False)

    def rdTAB2_Slider_2_2(self):
        if self.ui.radioButton_TAB2_Slider_2_OK.isChecked():
            self.ui.listWidget_TAB2_INIT.setEnabled(False)
            if (self.ui.comboBox_TAB2_QPU_List.currentText() != "") & (self.ui.horizontalSlider_TAB2_INIT.maximum() != 0):
                self.ui.horizontalSlider_TAB2_INIT.setEnabled(True)
    def rdTAB2_listWidget_2_2(self):
        if self.ui.radioButton_TAB2_ListWidget_2_OK.isChecked():
            self.ui.listWidget_TAB2_INIT.setEnabled(True)
            self.ui.horizontalSlider_TAB2_INIT.setEnabled(False)

    def rdTAB2_Slider_2_3(self):
        if self.ui.radioButton_TAB2_Slider_3_OK.isChecked():
            self.ui.listWidget_TAB2_H.setEnabled(False)
            if (self.ui.comboBox_TAB2_QPU_List.currentText() != "") & (self.ui.horizontalSlider_TAB2_H.maximum() != 0):
                self.ui.horizontalSlider_TAB2_H.setEnabled(True)
    def rdTAB2_listWidget_2_3(self):
        if self.ui.radioButton_TAB2_ListWidget_3_OK.isChecked():
            self.ui.listWidget_TAB2_H.setEnabled(True)
            self.ui.horizontalSlider_TAB2_H.setEnabled(False)

    def slider_TAB2_Changed_1(self):
        self.Slider_TAB2_Change_Value_1.list_widget_2_x = self.ui.listWidget_TAB2_IDLE                  
        self.Slider_TAB2_Change_Value_1.current_value = self.ui.horizontalSlider_TAB2_IDLE.value()      

        self.Slider_TAB2_Change_Value_1.finished.connect(self.onFinished_slider_TAB2_Changed_1)         
        self.Slider_TAB2_Change_Value_1.start()                                                         
    def onFinished_slider_TAB2_Changed_1(self):
        for i in range(self.ui.horizontalSlider_TAB2_IDLE.value(), self.ui.listWidget_TAB2_IDLE.count()):
            if self.ui.listWidget_TAB2_IDLE.item(i).checkState() == Qt.Checked:
                self.ui.listWidget_TAB2_IDLE.item(i).setCheckState(QtCore.Qt.Unchecked)

    def slider_TAB2_Changed_2(self):
        self.Slider_TAB2_Change_Value_2.list_widget_2_x = self.ui.listWidget_TAB2_INIT                  
        self.Slider_TAB2_Change_Value_2.current_value = self.ui.horizontalSlider_TAB2_INIT.value()      

        self.Slider_TAB2_Change_Value_2.finished.connect(self.onFinished_slider_TAB2_Changed_2)         
        self.Slider_TAB2_Change_Value_2.start()                                                         
    def onFinished_slider_TAB2_Changed_2(self):
        for i in range(self.ui.horizontalSlider_TAB2_INIT.value(), self.ui.listWidget_TAB2_INIT.count()):
            if self.ui.listWidget_TAB2_INIT.item(i).checkState() == Qt.Checked:
                self.ui.listWidget_TAB2_INIT.item(i).setCheckState(QtCore.Qt.Unchecked)

    def slider_TAB2_Changed_3(self):
        self.Slider_TAB2_Change_Value_3.list_widget_2_x = self.ui.listWidget_TAB2_H                     
        self.Slider_TAB2_Change_Value_3.current_value = self.ui.horizontalSlider_TAB2_H.value()         

        self.Slider_TAB2_Change_Value_3.finished.connect(self.onFinished_slider_TAB2_Changed_3)         
        self.Slider_TAB2_Change_Value_3.start()                                                         
    def onFinished_slider_TAB2_Changed_3(self):
        for i in range(self.ui.horizontalSlider_TAB2_H.value(), self.ui.listWidget_TAB2_H.count()):
            if self.ui.listWidget_TAB2_H.item(i).checkState() == Qt.Checked:
                self.ui.listWidget_TAB2_H.item(i).setCheckState(QtCore.Qt.Unchecked)

    def btnClicked_TAB2_Gen_Scheme(self):
        self.ui.comboBox_TAB2_QPU_List.setEnabled(False)                            
        self.ui.frame_TAB2_List_and_Slider.setEnabled(False)                        

        self.ui.tab_INFO.setEnabled(False)                                          
        self.ui.tab_QRNG.setEnabled(False)                                          
        self.ui.tab_QKD.setEnabled(False)                                           
        self.ui.tab_Fourie.setEnabled(False)                                        
        self.ui.tab_Instruments.setEnabled(False)                                   

        self.TAB2_Generate_Scheme.token_name = self.ui.lineEdit_API_Token.text()                
        self.TAB2_Generate_Scheme.ibm_channel = self.ui.lineEdit_Channel.text()                 
        self.TAB2_Generate_Scheme.backend_name = self.ui.comboBox_TAB2_QPU_List.currentText()   
        self.TAB2_Generate_Scheme.shots = self.ui.spinBox_INIT_IDLE_max_shots.value()           
        self.TAB2_Generate_Scheme.alpha = self.ui.doubleSpinBox_INIT_IDLE_Alpha.value()         
        self.TAB2_Generate_Scheme.opt_level = self.ui.spinBox_INIT_IDLE_OptLevel.value()        

        self.TAB2_Generate_Scheme.flag_radio_button_2_1 = self.ui.radioButton_TAB2_Slider_1_OK.isChecked()      
        self.TAB2_Generate_Scheme.flag_radio_button_2_2 = self.ui.radioButton_TAB2_Slider_2_OK.isChecked()      
        self.TAB2_Generate_Scheme.flag_radio_button_2_3 = self.ui.radioButton_TAB2_Slider_3_OK.isChecked()      
        self.TAB2_Generate_Scheme.list_widget_2_1 = self.ui.listWidget_TAB2_IDLE                                
        self.TAB2_Generate_Scheme.list_widget_2_2 = self.ui.listWidget_TAB2_INIT                                
        self.TAB2_Generate_Scheme.list_widget_2_3 = self.ui.listWidget_TAB2_H                                   

        self.TAB2_Generate_Scheme.slider_current_2_1 = self.ui.horizontalSlider_TAB2_IDLE.value()               
        self.TAB2_Generate_Scheme.slider_current_2_2 = self.ui.horizontalSlider_TAB2_INIT.value()               
        self.TAB2_Generate_Scheme.slider_current_2_3 = self.ui.horizontalSlider_TAB2_H.value()                  
        self.TAB2_Generate_Scheme.num_of_qubits_max = self.ui.horizontalSlider_TAB2_IDLE.maximum()              
        self.TAB2_Generate_Scheme.use_barriers = self.ui.checkBox_TAB2_bool_barriers.isChecked()                

        self.TAB2_Generate_Scheme.finished.connect(self.onFinished_TAB2_Gen_Scheme)     
        self.TAB2_Generate_Scheme.start()                                               
    def onFinished_TAB2_Gen_Scheme(self):
        self.ui.comboBox_TAB2_QPU_List.setEnabled(True)                         
        self.ui.frame_TAB2_List_and_Slider.setEnabled(True)                     

        self.ui.tab_INFO.setEnabled(True)                                      
        self.ui.tab_QRNG.setEnabled(True)                                      
        self.ui.tab_QKD.setEnabled(True)                                       
        self.ui.tab_Fourie.setEnabled(True)                                    
        self.ui.tab_Instruments.setEnabled(True)                               

    def btnClicked_TAB2_JobID_Check(self):

        self.ui.lineEdit_TAB2_JobID.setEnabled(False)                       
        self.ui.pushButton_TAB2_JobID_Info.setEnabled(False)                
        self.ui.pushButton_TAB2_JobID_Cancell.setEnabled(False)             
        self.ui.pushButton_TAB2_JobID_Result.setEnabled(False)              

        self.Check_JobID_TAB2.token_name = self.ui.lineEdit_API_Token.text()     
        self.Check_JobID_TAB2.ibm_channel = self.ui.lineEdit_Channel.text()      
        self.Check_JobID_TAB2.jobID = self.ui.lineEdit_TAB2_JobID.text()         

        self.Check_JobID_TAB2.finished.connect(self.onFinished_TAB2_JobID)      
        self.Check_JobID_TAB2.start()                                           

    def btnClicked_TAB2_JobID_Cancel(self):

        self.ui.lineEdit_TAB2_JobID.setEnabled(False)                       
        self.ui.pushButton_TAB2_JobID_Info.setEnabled(False)                
        self.ui.pushButton_TAB2_JobID_Cancell.setEnabled(False)             
        self.ui.pushButton_TAB2_JobID_Result.setEnabled(False)              

        self.Cancel_JobID_TAB2.token_name = self.ui.lineEdit_API_Token.text()    
        self.Cancel_JobID_TAB2.ibm_channel = self.ui.lineEdit_Channel.text()     
        self.Cancel_JobID_TAB2.jobID = self.ui.lineEdit_TAB2_JobID.text()        

        self.Cancel_JobID_TAB2.finished.connect(self.onFinished_TAB2_JobID)     
        self.Cancel_JobID_TAB2.start()                                          

    def btnClicked_TAB2_JobID_Download(self):

        self.ui.lineEdit_TAB2_JobID.setEnabled(False)                       
        self.ui.pushButton_TAB2_JobID_Info.setEnabled(False)                
        self.ui.pushButton_TAB2_JobID_Cancell.setEnabled(False)             
        self.ui.pushButton_TAB2_JobID_Result.setEnabled(False)              

        self.Download_JobID_TAB2.token_name = self.ui.lineEdit_API_Token.text()         
        self.Download_JobID_TAB2.ibm_channel = self.ui.lineEdit_Channel.text()          
        self.Download_JobID_TAB2.jobID = self.ui.lineEdit_TAB2_JobID.text()             
        self.Download_JobID_TAB2.alpha = self.ui.doubleSpinBox_INIT_IDLE_Alpha.value()  

        self.Download_JobID_TAB2.finished.connect(self.onFinished_TAB2_JobID)    
        self.Download_JobID_TAB2.start()                                         

    def onFinished_TAB2_JobID(self):

        self.ui.lineEdit_TAB2_JobID.setEnabled(True)                
        self.ui.pushButton_TAB2_JobID_Info.setEnabled(True)         
        self.ui.pushButton_TAB2_JobID_Cancell.setEnabled(True)      
        self.ui.pushButton_TAB2_JobID_Result.setEnabled(True)       

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

    def rdQRNGSimSlider(self):
        if self.ui.radioButton_QRNG_Sim_Slider_OK.isChecked():
            self.ui.listWidget_QRNG_Sim_Check_Qubits.setEnabled(False)
            if self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.maximum() != 0:
                self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.setEnabled(True)
    def rdQRNGSimListWidget(self):
        if self.ui.radioButton_QRNG_Sim_listWidget_OK.isChecked():
            self.ui.listWidget_QRNG_Sim_Check_Qubits.setEnabled(True)
            self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.setEnabled(False)

    def rdQRNGSlider(self):
        if self.ui.radioButton_QRNG_Slider_OK.isChecked():
            self.ui.listWidget_QRNG_Check_Qubits.setEnabled(False)
            if (self.ui.comboBox_QRNG_QPU_List.currentText() != "") & (self.ui.horizontalSlider_QRNG_Num_of_Qubits.maximum() != 0):
                self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)
    def rdQRNGListWidget(self):
        if self.ui.radioButton_QRNG_listWidget_OK.isChecked():
            self.ui.listWidget_QRNG_Check_Qubits.setEnabled(True)
            self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)

    def combobox_QRNG_QPU_Changed(self):

        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setMinimum(0)
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setMaximum(0)
        self.ui.listWidget_QRNG_Check_Qubits.clear()

        self.ui.comboBox_QRNG_QPU_List.setEnabled(False)                
        self.ui.pushButton_QRNG_Start.setEnabled(False)                 
        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)   
        self.ui.listWidget_QRNG_Check_Qubits.setEnabled(False)          
        self.ui.frame_QRNG_RadioButtons.setEnabled(False)               

        self.ui.tab_INFO.setEnabled(False)                              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            
        self.ui.tab_Instruments.setEnabled(False)                       

        self.QPU_QRNG_Change_Value.slider_QRNG = self.ui.horizontalSlider_QRNG_Num_of_Qubits    
        self.QPU_QRNG_Change_Value.spinBox_max_shots = self.ui.spinBox_QRNG_max_shots           

        self.QPU_QRNG_Change_Value.slider_INFO = self.ui.horizontalSlider_INFO_Num_of_Qubits    
        self.QPU_QRNG_Change_Value.list_widget_3_1 = self.ui.listWidget_QRNG_Check_Qubits       

        self.QPU_QRNG_Change_Value.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()  
        self.QPU_QRNG_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_QRNG_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_QRNG_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               

        self.ui.textEdit_Console_Output.clear()                                         
        self.ui.textEdit_TAB2.clear()                                                   
        self.ui.textEdit_QRNG_Output.clear()                                            
        self.ui.textEdit_TAB5.clear()                                                   

        self.QPU_QRNG_Change_Value.finished.connect(self.onFinished_QRNG_comboBox)      
        self.QPU_QRNG_Change_Value.start()                                              

    def onFinished_QRNG_comboBox(self):  
        if (self.ui.radioButton_QRNG_Slider_OK.isChecked()) & (self.ui.horizontalSlider_QRNG_Num_of_Qubits.maximum() != 0):
            self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)    
        if self.ui.radioButton_QRNG_listWidget_OK.isChecked():
            self.ui.listWidget_QRNG_Check_Qubits.setEnabled(True)           

        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.pushButton_QRNG_Start.setEnabled(True)                  
        self.ui.frame_QRNG_RadioButtons.setEnabled(True)                

        self.ui.tab_INFO.setEnabled(True)                               
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                        
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             
        self.ui.tab_Instruments.setEnabled(True)                       

        self.ui.spinBox_QRNG_max_shots.setValue(self.ui.spinBox_QRNG_max_shots.maximum())   

    def slider_QRNG_Changed(self):
        self.Slider_QRNG_Change_Value.list_widget_3_1 = self.ui.listWidget_QRNG_Check_Qubits                
        self.Slider_QRNG_Change_Value.current_value = self.ui.horizontalSlider_QRNG_Num_of_Qubits.value()   

        self.Slider_QRNG_Change_Value.finished.connect(self.onFinished_slider_QRNG_Changed)     
        self.Slider_QRNG_Change_Value.start()                                                   
    def slider_QRNG_Sim_Changed(self):
        self.Slider_QRNG_Sim_Change_Value.list_widget_3_2 = self.ui.listWidget_QRNG_Sim_Check_Qubits  
        self.Slider_QRNG_Sim_Change_Value.current_value = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.value()  

        self.Slider_QRNG_Sim_Change_Value.finished.connect(
        self.onFinished_slider_QRNG_Sim_Changed)  
        self.Slider_QRNG_Sim_Change_Value.start()  

    def onFinished_slider_QRNG_Changed(self):
        for i in range(self.ui.horizontalSlider_QRNG_Num_of_Qubits.value(), self.ui.listWidget_QRNG_Check_Qubits.count()):
            if self.ui.listWidget_QRNG_Check_Qubits.item(i).checkState() == Qt.Checked:
                self.ui.listWidget_QRNG_Check_Qubits.item(i).setCheckState(QtCore.Qt.Unchecked)
    def onFinished_slider_QRNG_Sim_Changed(self):
        for i in range(self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.value(), self.ui.listWidget_QRNG_Sim_Check_Qubits.count()):
            if self.ui.listWidget_QRNG_Sim_Check_Qubits.item(i).checkState() == Qt.Checked:
                self.ui.listWidget_QRNG_Sim_Check_Qubits.item(i).setCheckState(QtCore.Qt.Unchecked)

    def btnClicked_QRNG_Start(self):

        self.ui.comboBox_QRNG_QPU_List.setEnabled(False)                
        self.ui.pushButton_QRNG_Start.setEnabled(False)                 
        self.ui.frame_QRNG_RadioButtons.setEnabled(False)               

        self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(False)   
        self.ui.listWidget_QRNG_Check_Qubits.setEnabled(False)          
        self.ui.radioButton_QRNG_Slider_OK.setEnabled(False)            
        self.ui.radioButton_QRNG_listWidget_OK.setEnabled(False)        

        self.ui.spinBox_QRNG_max_shots.setEnabled(False)                
        self.ui.doubleSpinBox_QRNG_Alpha.setEnabled(False)              
        self.ui.spinBox_QRNG_OptLevel.setEnabled(False)                 

        self.ui.tab_INFO.setEnabled(False)                              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            
        self.ui.tab_Instruments.setEnabled(False)                       

        self.QRNG_process.token_name = self.ui.lineEdit_API_Token.text()                                
        self.QRNG_process.ibm_channel = self.ui.lineEdit_Channel.text()                                 
        self.QRNG_process.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()                   
        self.QRNG_process.num_of_qubits = self.ui.horizontalSlider_QRNG_Num_of_Qubits.value()           
        self.QRNG_process.num_of_qubits_max = self.ui.horizontalSlider_QRNG_Num_of_Qubits.maximum()     
        self.QRNG_process.alpha = self.ui.doubleSpinBox_QRNG_Alpha.value()                              
        self.QRNG_process.shots = self.ui.spinBox_QRNG_max_shots.value()                                
        self.QRNG_process.opt_level = self.ui.spinBox_QRNG_OptLevel.value()                             
        self.QRNG_process.flag_radio_button = self.ui.radioButton_QRNG_Slider_OK.isChecked()            
        self.QRNG_process.list_widget_3_1 = self.ui.listWidget_QRNG_Check_Qubits                        

        self.ui.textEdit_Console_Output.clear()         
        self.ui.textEdit_TAB2.clear()                   
        self.ui.textEdit_QRNG_Output.clear()            
        self.ui.textEdit_TAB5.clear()                   

        self.QRNG_process.finished.connect(self.onFinished_QRNG)      
        self.QRNG_process.start()                                     

    def onFinished_QRNG(self):  
        self.ui.comboBox_QRNG_QPU_List.setEnabled(True)                 
        self.ui.pushButton_QRNG_Start.setEnabled(True)                  
        self.ui.frame_QRNG_RadioButtons.setEnabled(True)                

        if self.ui.radioButton_QRNG_Slider_OK.isChecked():  self.ui.horizontalSlider_QRNG_Num_of_Qubits.setEnabled(True)    
        elif self.ui.radioButton_QRNG_listWidget_OK.isChecked():    self.ui.listWidget_QRNG_Check_Qubits.setEnabled(True)   
        self.ui.radioButton_QRNG_Slider_OK.setEnabled(True)             
        self.ui.radioButton_QRNG_listWidget_OK.setEnabled(True)         

        self.ui.spinBox_QRNG_max_shots.setEnabled(True)                 
        self.ui.doubleSpinBox_QRNG_Alpha.setEnabled(True)               
        self.ui.spinBox_QRNG_OptLevel.setEnabled(True)                  

        self.ui.tab_INFO.setEnabled(True)                               
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                        
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             
        self.ui.tab_Instruments.setEnabled(True)                        

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_process.full_path_for_NIST))

    def btnClicked_QRNG_SIMULATOR_Start(self):

        self.ui.frame_QRNG_Simulator.setEnabled(False)                              
        self.ui.frame_QRNG_RadioButtons.setEnabled(False)                           

        self.ui.tab_INFO.setEnabled(False)                                          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                                   
        self.ui.tab_QKD.setEnabled(False)                                           
        self.ui.tab_Fourie.setEnabled(False)                                        
        self.ui.tab_Instruments.setEnabled(False)                                   

        self.QRNG_Simulator_process.token_name = self.ui.lineEdit_API_Token.text()                                          
        self.QRNG_Simulator_process.ibm_channel = self.ui.lineEdit_Channel.text()                                           
        self.QRNG_Simulator_process.num_of_qubits = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.value()           
        self.QRNG_Simulator_process.num_of_qubits_max = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.maximum()     
        self.QRNG_Simulator_process.alpha = self.ui.doubleSpinBox_QRNG_Sim_Alpha.value()                                    
        self.QRNG_Simulator_process.shots = self.ui.spinBox_QRNG_Sim_max_shots.value()                                      
        self.QRNG_Simulator_process.opt_level = self.ui.spinBox_QRNG_OptLevel.value()                                       
        self.QRNG_Simulator_process.flag_radio_button = self.ui.radioButton_QRNG_Sim_Slider_OK.isChecked()                  
        self.QRNG_Simulator_process.list_widget_3_2 = self.ui.listWidget_QRNG_Sim_Check_Qubits                              

        self.ui.textEdit_Console_Output.clear()                                             
        self.ui.textEdit_TAB2.clear()                                                       
        self.ui.textEdit_QRNG_Output.clear()                                                
        self.ui.textEdit_TAB5.clear()                                                       

        self.QRNG_Simulator_process.finished.connect(self.onFinished_QRNG_Simulator)        
        self.QRNG_Simulator_process.start()                                                 

    def onFinished_QRNG_Simulator(self):  
        self.ui.frame_QRNG_Simulator.setEnabled(True)                              
        self.ui.frame_QRNG_RadioButtons.setEnabled(True)                           

        self.ui.tab_INFO.setEnabled(True)                               
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                        
        self.ui.tab_QKD.setEnabled(True)                                
        self.ui.tab_Fourie.setEnabled(True)                             
        self.ui.tab_Instruments.setEnabled(True)                        

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_Simulator_process.full_path_for_NIST))

    def btnClicked_QRNG_JobID_Check(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Check_JobID.token_name = self.ui.lineEdit_API_Token.text()     
        self.Check_JobID.ibm_channel = self.ui.lineEdit_Channel.text()      
        self.Check_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()         

        self.Check_JobID.finished.connect(self.onFinished_JobID)        
        self.Check_JobID.start()                                        

    def btnClicked_QRNG_JobID_Cancel(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Cancel_JobID.token_name = self.ui.lineEdit_API_Token.text()    
        self.Cancel_JobID.ibm_channel = self.ui.lineEdit_Channel.text()     
        self.Cancel_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()        

        self.Cancel_JobID.finished.connect(self.onFinished_JobID)       
        self.Cancel_JobID.start()                                       

    def btnClicked_QRNG_JobID_Download(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        

        self.Download_JobID.token_name = self.ui.lineEdit_API_Token.text()      
        self.Download_JobID.ibm_channel = self.ui.lineEdit_Channel.text()       
        self.Download_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()          
        self.Download_JobID.alpha = self.ui.doubleSpinBox_QRNG_Alpha.value()    

        self.Download_JobID.finished.connect(self.onFinished_JobID)         
        self.Download_JobID.start()                                         

    def onFinished_JobID(self):

        self.ui.lineEdit_QRNG_JobID.setEnabled(True)            
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(True)    
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(True)   
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(True) 

    def btnClicked_NIST_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)               

        self.ui.frame_QRNG_RadioButtons.setEnabled(False)           
        self.ui.pushButton_NIST_Start.setEnabled(False)             
        self.ui.pushButton_Path_for_NIST_Dialog.setEnabled(False)   

        self.ui.tab_INFO.setEnabled(False)                          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                   

        self.ui.tab_QKD.setEnabled(False)                           
        self.ui.tab_Fourie.setEnabled(False)                        
        self.ui.tab_Instruments.setEnabled(False)                   

        self.ui.textEdit_Console_Output.clear()                     
        self.ui.textEdit_TAB2.clear()                               
        self.ui.textEdit_QRNG_Output.clear()                        
        self.ui.textEdit_TAB5.clear()                               

        arg1 = self.ui.lineEdit_NIST_Directory_to_Dataset.text()        
        arg2 = self.ui.spinBox_NIST_Key_Length.text()                  
        arg3 = self.ui.spinBox_NIST_Tests_Supplys.text()               
        arg4 = self.ui.spinBox_NIST_Parameters_on_Default.text()       
        arg5 = self.ui.spinBox_NIST_Num_of_Bitstream.text()            
        arg6 = self.ui.spinBox_NIST_Format_of_Data.text()              
        self.NIST_process.args = [arg1, arg2, arg3, arg4, arg5, arg6]   

        self.NIST_process.start()                                       
        self.NIST_process.finished.connect(self.onFinished_NIST)        

    def onFinished_NIST(self):  
            self.ui.frame_QRNG_RadioButtons.setEnabled(True)            
            self.ui.pushButton_NIST_Start.setEnabled(True)              
            self.ui.pushButton_Path_for_NIST_Dialog.setEnabled(True)    

            self.ui.tab_INFO.setEnabled(True)                           
            self.ui.tab_INIT_IDLE_H.setEnabled(True)                    

            self.ui.tab_QKD.setEnabled(True)                            
            self.ui.tab_Fourie.setEnabled(True)                         
            self.ui.tab_Instruments.setEnabled(True)                    

            QApplication.restoreOverrideCursor()                        

    def btnClicked_NIST_Path_to_File(self):

        self.ui.lineEdit_NIST_Directory_to_Dataset.clear()

        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Select", options=QtWidgets.QFileDialog.DontUseNativeDialog)

        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(folder_path))

        flag = False
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_size = os.path.getsize(os.path.join(root, file))
                    self.ui.spinBox_NIST_Key_Length.setValue(file_size)
                    flag = True; break
            if flag: break

    def btnClicked_BITMAP_Path_to_File(self):

        self.ui.lineEdit_TAB5_Bitmap_Directory_Dialog.clear()

        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:", options=QtWidgets.QFileDialog.DontUseNativeDialog)

        self.ui.lineEdit_TAB5_Bitmap_Directory_Dialog.setText(str(folder_path))

    def btnClicked_BITMAP_Start(self):
        self.ui.textEdit_Console_Output.clear()     
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_QRNG_Output.clear()        
        self.ui.textEdit_TAB5.clear()               

        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        

        self.ui.frame_Fcorr_Easy.setEnabled(False)                          
        self.ui.frame_Fcorr_Profi.setEnabled(False)                         
        self.ui.pushButton_TAB5_Path_for_Bitmap_DIALOG.setEnabled(False)    
        self.ui.pushButton_TAB5_Calculate_Bitmap.setEnabled(False)          

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.Bitmap_process.path_to_folder = self.ui.lineEdit_TAB5_Bitmap_Directory_Dialog.text()

        self.Bitmap_process.start()  
        self.Bitmap_process.finished.connect(self.onFinished_Bitmap)  

    def onFinished_Bitmap(self):

        QApplication.restoreOverrideCursor()  

        self.ui.tab_INFO.setEnabled(True)                                  
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                           
        self.ui.tab_QRNG.setEnabled(True)                                  
        self.ui.tab_QKD.setEnabled(True)                                   
        self.ui.tab_Fourie.setEnabled(True)                                

        self.ui.frame_Fcorr_Easy.setEnabled(True)                          
        self.ui.frame_Fcorr_Profi.setEnabled(True)                         
        self.ui.pushButton_TAB5_Path_for_Bitmap_DIALOG.setEnabled(True)    
        self.ui.pushButton_TAB5_Calculate_Bitmap.setEnabled(True)          

    def btnClicked_Fcorr_Seq1_easy(self):

        self.ui.lineEdit_TAB5_path_Seq1_easy.clear()

        dialog = QFileDialog(self)

        folder_path = \
                dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.txt)",
                               options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]

        self.ui.lineEdit_TAB5_path_Seq1_easy.setText(str(folder_path))

    def btnClicked_Fcorr_Seq2_easy(self):

        self.ui.lineEdit_TAB5_path_Seq2_easy.clear()

        dialog = QFileDialog(self)

        folder_path = \
            dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.txt)",
                                   options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]

        self.ui.lineEdit_TAB5_path_Seq2_easy.setText(str(folder_path))

    def btnClicked_Fcorr_calculate_easy(self):

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.ui.tab_INFO.setEnabled(False)                      
        self.ui.tab_INIT_IDLE_H.setEnabled(False)               
        self.ui.tab_QRNG.setEnabled(False)                      
        self.ui.tab_QKD.setEnabled(False)                       
        self.ui.tab_Fourie.setEnabled(False)                    

        self.ui.frame_Bitmp.setEnabled(False)                           
        self.ui.frame_Fcorr_Profi.setEnabled(False)                     
        self.ui.pushButton_TAB5_Seq1_Dialog_easy.setEnabled(False)      
        self.ui.pushButton_TAB5_Seq2_Dialog_easy.setEnabled(False)      
        self.ui.pushButton_TAB5_Fcorrelation_easy.setEnabled(False)     

        self.FCorrEasy_process.USR_FILE_NAME_1 = self.ui.lineEdit_TAB5_path_Seq1_easy.text()  
        self.FCorrEasy_process.USR_FILE_NAME_2 = self.ui.lineEdit_TAB5_path_Seq2_easy.text()  

        self.FCorrEasy_process.start()                                      
        self.FCorrEasy_process.finished.connect(self.onFinished_FCorrEasy)  

    def onFinished_FCorrEasy(self):

        QApplication.restoreOverrideCursor()  

        self.ui.tab_INFO.setEnabled(True)                              
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                       
        self.ui.tab_QRNG.setEnabled(True)                              
        self.ui.tab_QKD.setEnabled(True)                               
        self.ui.tab_Fourie.setEnabled(True)                            

        self.ui.frame_Bitmp.setEnabled(True)                           
        self.ui.frame_Fcorr_Profi.setEnabled(True)                     
        self.ui.pushButton_TAB5_Seq1_Dialog_easy.setEnabled(True)      
        self.ui.pushButton_TAB5_Seq2_Dialog_easy.setEnabled(True)      
        self.ui.pushButton_TAB5_Fcorrelation_easy.setEnabled(True)     

    def btnClicked_Fcorr_Seq1_profi(self):

        self.ui.lineEdit_TAB5_path_Seq1_profi.clear()

        dialog = QFileDialog(self)
        folder_path = \
                dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.txt)",
                               options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]

        self.ui.lineEdit_TAB5_path_Seq1_profi.setText(str(folder_path))

    def btnClicked_Fcorr_Seq2_profi(self):

        self.ui.lineEdit_TAB5_path_Seq2_profi.clear()

        dialog = QFileDialog(self)
        folder_path = \
            dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.txt)",
                                   options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]

        self.ui.lineEdit_TAB5_path_Seq2_profi.setText(str(folder_path))

    def btnClicked_Fcorr_calculate_profi(self):

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.FCorrProfi_process.USR_FILE_NAME_1 = self.ui.lineEdit_TAB5_path_Seq1_profi.text()  
        self.FCorrProfi_process.USR_FILE_NAME_2 = self.ui.lineEdit_TAB5_path_Seq2_profi.text()  

        self.ui.tab_INFO.setEnabled(False)                              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                       
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            

        self.ui.frame_Bitmp.setEnabled(False)                           
        self.ui.frame_Fcorr_Easy.setEnabled(False)                      
        self.ui.pushButton_TAB5_Seq1_Dialog_profi.setEnabled(False)     
        self.ui.pushButton_TAB5_Seq2_Dialog_profi.setEnabled(False)     
        self.ui.pushButton_TAB5_Fcorrelation_profi.setEnabled(False)    

        self.FCorrProfi_process.start()  
        self.FCorrProfi_process.finished.connect(self.onFinished_FCorrProfi)  

    def onFinished_FCorrProfi(self):

        QApplication.restoreOverrideCursor()  

        self.ui.tab_INFO.setEnabled(True)                              
        self.ui.tab_INIT_IDLE_H.setEnabled(True)                       
        self.ui.tab_QRNG.setEnabled(True)                              
        self.ui.tab_QKD.setEnabled(True)                               
        self.ui.tab_Fourie.setEnabled(True)                            

        self.ui.frame_Bitmp.setEnabled(True)                           
        self.ui.frame_Fcorr_Easy.setEnabled(True)                      
        self.ui.pushButton_TAB5_Seq1_Dialog_profi.setEnabled(True)     
        self.ui.pushButton_TAB5_Seq2_Dialog_profi.setEnabled(True)     
        self.ui.pushButton_TAB5_Fcorrelation_profi.setEnabled(True)    

def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
