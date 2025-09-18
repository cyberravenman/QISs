import os.path
import re
import shutil
from IPython.external.qt_for_kernel import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QListWidgetItem
from src.TAB_0.Predict import PredictValues
from src.TAB_1.Gen_Scheme import GenerateScheme
from src.TAB_2.NIST_STS import NISTLaunch
from src.TAB_3.BB84 import QKDBB84Start
from src.TAB_3.QRNG_Bell import QPUChangedComboBoxTAB4, QRNGBellStart
from src.TAB_5.Bitmap import BitmapLaunch
from src.TAB_5.Fcorrelation import FCorrEasy, FCorrProfi, FCorrMatrix
from src.TAB_5.Merge import MergeFileSequences, MergeFileReportsNIST, MergeCsv, ConcatCsv
from src.TAB_5.p_i import CalcPi
from src.TAB_6.KEY_Alignment import KeyAlignment
from src.TAB_6.Prime_numbers import PrimeGen
from src.TAB_7.Argument import CountArgument, BinomialModeling, LinRegModeling, Predict
from src.TAB_7.Factors import Interrelation, CorrVIF, FactorsSignificance
from src.gui import Ui_MainWindow
from src.TAB_0.QPU_Info import *
from src.TAB_1.IDLE_INIT_H import *
from src.TAB_1.JobID import *
from src.TAB_2.QRNG import *
from src.TAB_2.QRNG_Simulator import *
from src.TAB_2.JobID import *
import sys
from PyQt5.QtWidgets import QMessageBox
class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()
sys.excepthook = log_uncaught_exceptions
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
        self.ui.tabWidget_PARENT.setTabVisible(6, False)
        self.ui.tabWidget_PARENT.setTabVisible(7, False)
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
        self.ui.pushButton_TAB1_Browse_TTX.clicked.connect(self.btnClicked_TAB1_Browse_TTX)
        self.ui.pushButton_TAB1_Browse_Model.clicked.connect(self.btnClicked_TAB1_Browse_Model)
        self.ui.pushButton_TAB1_Predict.clicked.connect(self.btnClicked_TAB1_Predict_Values)
        self.QPU_Predict_Value = PredictValues()
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
        self.ui.comboBox_TAB3_QPU_List.activated[str].connect(self.combobox_TAB3_QPU_Changed)
        self.QPU_TAB3_Change_Value = QPUChangedComboBoxTAB4()
        self.ui.listWidget_TAB3_QRNG_Bell.itemChanged.connect(lambda item : self.listWidget_TAB3_QRNG_Bell_Clicked(self.ui.listWidget_TAB3_QRNG_Bell.indexFromItem(item).row(), item.checkState()))
        self.ui.listWidget_TAB3_QKD_BB84.itemChanged.connect(lambda item: self.listWidget_TAB3_QKD_BB84_Clicked(self.ui.listWidget_TAB3_QKD_BB84.indexFromItem(item).row(), item.checkState()))
        self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.textChanged.connect(self.lineEdit_TAB3_QRNG_Bell_Changed)
        self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.textChanged.connect(self.lineEdit_TAB3_QKD_BB84_Changed)
        self.ui.pushButton_TAB3_QRNG_Bell_Browse.clicked.connect(self.btnClicked_TAB3_Browse_Config)
        self.ui.pushButton_TAB3_QKD_BB84_Browse.clicked.connect(self.btnClicked_TAB3_QKD_BB84_Browse_Config)
        self.ui.pushButton_TAB3_QRNG_Bell_Start.clicked.connect(self.btnClicked_TAB3_QRNG_Bell_Start)
        self.QRNGBell_process = QRNGBellStart()
        self.ui.pushButton_TAB3_QKD_BB84_Start.clicked.connect(self.btnClicked_TAB3_QKD_BB84_Start)
        self.QKDBB84_process = QKDBB84Start()
        self.ui.radioButton_TAB5_FilesSequences_Bad_Seq.clicked.connect(self.rdFileSeqMergeBAD)
        self.ui.radioButton_TAB5_FilesSequences_Good_Seq.clicked.connect(self.rdFileSeqMergeGOOD)
        self.ui.radioButton_TAB5_FilesSequences_All_Seq.clicked.connect(self.rdFileSeqMergeALL)
        self.ui.radioButton_TAB5_FilesSequences_User_Seq.clicked.connect(self.rdFileSeqMergeUSER)
        self.ui.checkBox_TAB5_Left_All.stateChanged.connect(self.chkBox_TAB5_Select_All_LEFT_Headers)
        self.ui.checkBox_TAB5_Right_All.stateChanged.connect(self.chkBox_TAB5_Select_All_RIGHT_Headers)
        self.ui.pushButton_TAB5_Path_for_Bitmap_DIALOG.clicked.connect(self.btnClicked_BITMAP_Path_to_File)
        self.ui.pushButton_TAB5_Calculate_Bitmap.clicked.connect(self.btnClicked_BITMAP_Start)
        self.Bitmap_process = BitmapLaunch()
        self.ui.pushButton_TAB5_CorrMatrix_Dialog.clicked.connect(self.btnClicked_CorrMatrix_Path_to_File)
        self.ui.pushButton_TAB5_CorrMatrix_Calculate.clicked.connect(self.btnClicked_CorrMatrix_Start)
        self.FCorrMatrix_process = FCorrMatrix()
        self.ui.pushButton_TAB5_Seq1_Dialog_easy.clicked.connect(self.btnClicked_Fcorr_Seq1_easy)
        self.ui.pushButton_TAB5_Seq2_Dialog_easy.clicked.connect(self.btnClicked_Fcorr_Seq2_easy)
        self.ui.pushButton_TAB5_Fcorrelation_easy.clicked.connect(self.btnClicked_Fcorr_calculate_easy)
        self.FCorrEasy_process = FCorrEasy()
        self.ui.pushButton_TAB5_Seq1_Dialog_profi.clicked.connect(self.btnClicked_Fcorr_Seq1_profi)
        self.ui.pushButton_TAB5_Seq2_Dialog_profi.clicked.connect(self.btnClicked_Fcorr_Seq2_profi)
        self.ui.pushButton_TAB5_Fcorrelation_profi.clicked.connect(self.btnClicked_Fcorr_calculate_profi)
        self.FCorrProfi_process = FCorrProfi()
        self.ui.pushButton_TAB5_FilesSequences_Dialog.clicked.connect(self.btnClicked_FileSeq_Path_to_Folder)
        self.ui.pushButton_TAB5_FilesSequences_Merge.clicked.connect(self.btnClicked_FileSeq_Start)
        self.Merge_FileSeq_process = MergeFileSequences()
        self.ui.pushButton_TAB5_NISTReports_Dialog.clicked.connect(self.btnClicked_ReportsNIST_Path_to_Folder)
        self.ui.pushButton_TAB5_NISTReports_Merge.clicked.connect(self.btnClicked_ReportsNIST_Start)
        self.Merge_ReportsNIST_process = MergeFileReportsNIST()
        self.ui.pushButton_TAB5_csv_Merge_Dialog_1.clicked.connect(self.btnClicked_csv_1_Path_to_File)
        self.ui.pushButton_TAB5_csv_Merge_Dialog_2.clicked.connect(self.btnClicked_csv_2_Path_to_File)
        self.ui.pushButton_TAB5_csv_Merge_All_csv_Browse.clicked.connect(self.btnClicked_Merge_All_in_Folder)
        self.ui.pushButton_TAB5_csv_Merge_Merge.clicked.connect(self.btnClicked_Merge_csv_Start)
        self.Merge_csv_process = MergeCsv()
        self.ui.pushButton_TAB5_csv_Concat.clicked.connect(self.btnClicked_Concat)
        self.Concat_process = ConcatCsv()
        self.ui.pushButton_TAB5_csv_Sort.clicked.connect(self.btnClicked_Sort_csv_Start)
        self.ui.pushButton_TAB5_Calculate_Pi_Dialog.clicked.connect(self.btnClicked_Calc_P_i_Path_to_Folder)
        self.ui.pushButton_TAB5_Calculate_Pi_Calculate.clicked.connect(self.btnClicked_Calc_P_i_Start)
        self.Calculate_P_i_process = CalcPi()
        self.ui.pushButton_Instruments_2_Prime_Generate.clicked.connect(self.btnClicked_Prime_Numbers_Gen)
        self.Prime_Number_Generate = PrimeGen()
        self.ui.pushButton_Instruments_2_Browse_BAD_qubits.clicked.connect(self.btnClicked_Browse_BAD_qubits)
        self.ui.checkBox_Instruments_2_SHIFT_from_File.stateChanged.connect(self.chkBox_SHIFT_from_File)
        self.ui.pushButton_Instruments_2_Browse_SHIFT_from_File.clicked.connect(self.btnClicked_Browse_SHIFT_from_File)
        self.ui.pushButton_Instruments_2_KEY_Alignment.clicked.connect(self.btnClicked_KEY_Alignment)
        self.Key_Alignment = KeyAlignment()
        self.ui.pushButton_TAB6_Select_csvFile.clicked.connect(self.btnClicked_Logit_Path_to_File)
        self.ui.pushButton_TAB6_Select_Model.clicked.connect(self.btnClicked_Path_to_Model)
        self.ui.pushButton_TAB6_Interrelation.clicked.connect(self.btnClicked_Logit_Interrelation)
        self.Interrelation_process = Interrelation()
        self.ui.pushButton_TAB6_Corr_VIF.clicked.connect(self.btnClicked_Logit_Corr_VIF)
        self.Corr_VIF_process = CorrVIF()
        self.ui.pushButton_TAB6_factors_significance.clicked.connect(self.btnClicked_Factors_Significance)
        self.Factors_Significance_process = FactorsSignificance()
        self.ui.pushButton_TAB6_counts_of_argument.clicked.connect(self.btnClicked_Logit_Count_of_Argument)
        self.Count_of_Argument_process = CountArgument()
        self.ui.pushButton_TAB6_Binomial_Model.clicked.connect(self.btnClicked_Logit_Binomial_Modeling)
        self.Binomial_Modeling_process = BinomialModeling()
        self.ui.pushButton_TAB6_Linear_Modeling_Formula.clicked.connect(self.btnClicked_Linear_Modeling_Gen_Formula)
        self.ui.pushButton_TAB6_Linear_Modeling.clicked.connect(self.btnClicked_Lineal_Regression_Modeling)
        self.LinReg_Modeling_process = LinRegModeling()
        self.ui.pushButton_TAB6_Predict.clicked.connect(self.btnPredict)
        self.Predict_process = Predict()
        self.ui.checkBox_TAB6_Select_all_Factors.stateChanged.connect(self.chkBox_Logit_Select_All_Headers)
    def onUpdateText(self, text):
        self.ui.textEdit_TAB0.insertPlainText(text)
        self.ui.textEdit_TAB0.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB1.insertPlainText(text)
        self.ui.textEdit_TAB1.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB2.insertPlainText(text)
        self.ui.textEdit_TAB2.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB3.insertPlainText(text)
        self.ui.textEdit_TAB3.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB5.insertPlainText(text)
        self.ui.textEdit_TAB5.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB6.insertPlainText(text)
        self.ui.textEdit_TAB6.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_TAB7.insertPlainText(text)
        self.ui.textEdit_TAB7.moveCursor(QtGui.QTextCursor.End)
    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    def rdBASE(self):
        if self.ui.radioButton_BASE.isChecked():
            self.ui.tabWidget_PARENT.setTabVisible(1, False)
            self.ui.tabWidget_PARENT.setTabVisible(2, False)
            self.ui.tabWidget_PARENT.setTabVisible(3, False)
            self.ui.tabWidget_PARENT.setTabVisible(4, False)
            self.ui.tabWidget_PARENT.setTabVisible(5, False)
            self.ui.tabWidget_PARENT.setTabVisible(6, False)
            self.ui.tabWidget_PARENT.setTabVisible(7, False)
    def rdPROFI(self):
        if self.ui.radioButton_PROFESSIONAL.isChecked():
            self.ui.tabWidget_PARENT.setTabVisible(1, True)
            self.ui.tabWidget_PARENT.setTabVisible(2, True)
            self.ui.tabWidget_PARENT.setTabVisible(3, True)
            self.ui.tabWidget_PARENT.setTabVisible(4, True)
            self.ui.tabWidget_PARENT.setTabVisible(5, True)
            self.ui.tabWidget_PARENT.setTabVisible(6, True)
            self.ui.tabWidget_PARENT.setTabVisible(7, True)
    def btnClicked_QPU_Available(self):
        self.ui.comboBox_INFO_QPU_List.clear()
        self.ui.comboBox_QRNG_QPU_List.clear()
        self.ui.comboBox_TAB2_QPU_List.clear()
        self.ui.comboBox_TAB3_QPU_List.clear()
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
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
        self.QPU_info.ibm_channel = self.ui.lineEdit_Channel.text()                         
        self.QPU_info.ibm_instance = self.ui.lineEdit_Instance.text()                       
        self.QPU_info.token_name = self.ui.lineEdit_API_Token.text()                        
        self.QPU_info.combo_box_Dynamic_INFO = self.ui.comboBox_INFO_QPU_List               
        self.QPU_info.combo_box_Dynamic_INIT_IDLE_H = self.ui.comboBox_TAB2_QPU_List        
        self.QPU_info.combo_box_Dynamic_QRNG = self.ui.comboBox_QRNG_QPU_List               
        self.QPU_info.combo_box_Dynamic_QRNG_Bell = self.ui.comboBox_TAB3_QPU_List          
        self.ui.textEdit_TAB0.clear()       
        self.ui.textEdit_TAB1.clear()       
        self.ui.textEdit_TAB2.clear()       
        self.ui.textEdit_TAB3.clear()       
        self.ui.textEdit_TAB5.clear()       
        self.ui.textEdit_TAB6.clear()       
        self.ui.textEdit_TAB7.clear()       
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
            self.ui.tab_Instruments_2.setEnabled(False)                     
            self.ui.tab_Modeling.setEnabled(False)                          
            self.QPU_info_2.ibm_channel = self.ui.lineEdit_Channel.text()               
            self.QPU_info_2.ibm_instance = self.ui.lineEdit_Instance.text()             
            self.QPU_info_2.token_name = self.ui.lineEdit_API_Token.text()              
            self.QPU_info_2.backend_name = self.ui.comboBox_INFO_QPU_List.currentText() 
            self.ui.textEdit_TAB0.clear()               
            self.ui.textEdit_TAB1.clear()               
            self.ui.textEdit_TAB2.clear()               
            self.ui.textEdit_TAB3.clear()               
            self.ui.textEdit_TAB5.clear()               
            self.ui.textEdit_TAB6.clear()               
            self.ui.textEdit_TAB7.clear()               
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
            self.ui.tab_Instruments_2.setEnabled(False)                     
            self.ui.tab_Modeling.setEnabled(False)                          
            self.QPU_Qubit_Info.ibm_channel = self.ui.lineEdit_Channel.text()                       
            self.QPU_Qubit_Info.ibm_instance = self.ui.lineEdit_Instance.text()                     
            self.QPU_Qubit_Info.token_name = self.ui.lineEdit_API_Token.text()                      
            self.QPU_Qubit_Info.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()         
            self.QPU_Qubit_Info.qubit_number = self.ui.horizontalSlider_INFO_Num_of_Qubits.value()  
            self.ui.textEdit_TAB0.clear()           
            self.ui.textEdit_TAB1.clear()           
            self.ui.textEdit_TAB2.clear()           
            self.ui.textEdit_TAB3.clear()           
            self.ui.textEdit_TAB5.clear()           
            self.ui.textEdit_TAB6.clear()           
            self.ui.textEdit_TAB7.clear()           
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
        self.ui.tab_Instruments_2.setEnabled(True)                      
        self.ui.tab_Modeling.setEnabled(True)                           
        if self.ui.comboBox_INFO_QPU_List.count() != 0:
            self.ui.comboBox_INFO_QPU_List.setEnabled(True)             
            self.ui.comboBox_TAB2_QPU_List.setEnabled(True)        
            self.ui.comboBox_QRNG_QPU_List.setEnabled(True)             
    def btnClicked_TAB1_Browse_TTX(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.csv)",
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB1_Callibrate_csv_File_Path.clear()
        self.ui.lineEdit_TAB1_Callibrate_csv_File_Path.setText(str(folder_path))
        df = pd.read_csv(folder_path,
                         sep=',',  
                         header=0,  
                         na_values=['', 'N/A'])  
        pd.set_option('display.max_columns', None)
        print(df.describe())
        pd.reset_option('display.max_columns')
    def btnClicked_TAB1_Browse_Model(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.pickle)",
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB1_Model_Path.clear()
        self.ui.lineEdit_TAB1_Model_Path.setText(str(folder_path))
    def btnClicked_TAB1_Predict_Values(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/QPU_Info/Predicted/" + str(current_date)
        if self.ui.radioButton_TAB1_INIT_Zero_Predict.isChecked():
            self.QPU_Predict_Value.value_predict = "Zero"
            self.QPU_Predict_Value.type_of_argument = True
            self.QPU_Predict_Value.path_to_result = path_to_result + '/INIT_Zero'
        elif self.ui.radioButton_TAB1_QRNG_Zero_Predict.isChecked():
            self.QPU_Predict_Value.value_predict = "Zero"
            self.QPU_Predict_Value.type_of_argument = True
            self.QPU_Predict_Value.path_to_result = path_to_result + '/QRNG_Zero'
        elif self.ui.radioButton_TAB1_QRNG_One_Predict.isChecked():
            self.QPU_Predict_Value.value_predict = "One"
            self.QPU_Predict_Value.type_of_argument = True
            self.QPU_Predict_Value.path_to_result = path_to_result + '/QRNG_One'
        elif self.ui.radioButton_TAB1_QRNG_NIST_Predict.isChecked():
            self.QPU_Predict_Value.value_predict = "p_i"
            self.QPU_Predict_Value.type_of_argument = False
            self.QPU_Predict_Value.path_to_result = path_to_result + '/QRNG_p_i'
        self.QPU_Predict_Value.path_to_csv = self.ui.lineEdit_TAB1_Callibrate_csv_File_Path.text()
        self.QPU_Predict_Value.path_to_model = self.ui.lineEdit_TAB1_Model_Path.text()
        self.QPU_Predict_Value.name_of_result = self.ui.lineEdit_TAB1_Result_Predicted_Path.text()
        self.QPU_Predict_Value.start()  
        self.QPU_Predict_Value.finished.connect(self.onFinished_Predict)  
    def onFinished_Predict(self):
        QApplication.restoreOverrideCursor()  
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
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
        self.ui.tab_Instruments_2.setEnabled(False)         
        self.ui.tab_Modeling.setEnabled(False)              
        self.QPU_INFO_Change_Value.slider_INFO = self.ui.horizontalSlider_INFO_Num_of_Qubits    
        self.QPU_INFO_Change_Value.backend_name = self.ui.comboBox_INFO_QPU_List.currentText()  
        self.QPU_INFO_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_INFO_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_INFO_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
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
        self.ui.tab_Instruments_2.setEnabled(True)                      
        self.ui.tab_Modeling.setEnabled(True)                           
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
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
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
        self.ui.textEdit_TAB0.clear()  
        self.ui.textEdit_TAB1.clear()  
        self.ui.textEdit_TAB2.clear()  
        self.ui.textEdit_TAB3.clear()  
        self.ui.textEdit_TAB5.clear()  
        self.ui.textEdit_TAB6.clear()  
        self.ui.textEdit_TAB7.clear()  
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
        self.ui.tab_Instruments_2.setEnabled(True)      
        self.ui.tab_Modeling.setEnabled(True)           
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
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
        self.ui.comboBox_TAB2_QPU_List.setEnabled(False)                            
        self.ui.frame_TAB2_List_and_Slider.setEnabled(False)                        
        self.ui.tab_INFO.setEnabled(False)                                          
        self.ui.tab_QRNG.setEnabled(False)                                          
        self.ui.tab_QKD.setEnabled(False)                                           
        self.ui.tab_Fourie.setEnabled(False)                                        
        self.ui.tab_Instruments.setEnabled(False)                                   
        self.ui.tab_Instruments_2.setEnabled(False)                                 
        self.ui.tab_Modeling.setEnabled(False)                                      
        self.TAB2_Generate_Scheme.token_name = self.ui.lineEdit_API_Token.text()                
        self.TAB2_Generate_Scheme.ibm_channel = self.ui.lineEdit_Channel.text()                 
        self.TAB2_Generate_Scheme.backend_name = self.ui.comboBox_TAB2_QPU_List.currentText()   
        self.TAB2_Generate_Scheme.shots = self.ui.spinBox_INIT_IDLE_max_shots.value()           
        self.TAB2_Generate_Scheme.alpha = self.ui.doubleSpinBox_INIT_IDLE_Alpha.value()         
        self.TAB2_Generate_Scheme.opt_level = self.ui.spinBox_INIT_IDLE_OptLevel.value()        
        self.TAB2_Generate_Scheme.timezone = self.ui.spinBox_TAB0_TimeZone.value()              
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
        self.ui.tab_Instruments_2.setEnabled(True)                             
        self.ui.tab_Modeling.setEnabled(True)                                  
    def btnClicked_TAB2_JobID_Check(self):
        self.ui.lineEdit_TAB2_JobID.setEnabled(False)                       
        self.ui.pushButton_TAB2_JobID_Info.setEnabled(False)                
        self.ui.pushButton_TAB2_JobID_Cancell.setEnabled(False)             
        self.ui.pushButton_TAB2_JobID_Result.setEnabled(False)              
        self.Check_JobID_TAB2.token_name = self.ui.lineEdit_API_Token.text()     
        self.Check_JobID_TAB2.ibm_channel = self.ui.lineEdit_Channel.text()      
        self.Check_JobID_TAB2.jobID = self.ui.lineEdit_TAB2_JobID.text()         
        self.Check_JobID_TAB2.timezone = self.ui.spinBox_TAB0_TimeZone.value()   
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
        self.Cancel_JobID_TAB2.timezone = self.ui.spinBox_TAB0_TimeZone.value()  
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
        self.Download_JobID_TAB2.timezone = self.ui.spinBox_TAB0_TimeZone.value()       
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
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
        self.QPU_QRNG_Change_Value.slider_QRNG = self.ui.horizontalSlider_QRNG_Num_of_Qubits    
        self.QPU_QRNG_Change_Value.spinBox_max_shots = self.ui.spinBox_QRNG_max_shots           
        self.QPU_QRNG_Change_Value.slider_INFO = self.ui.horizontalSlider_INFO_Num_of_Qubits    
        self.QPU_QRNG_Change_Value.list_widget_3_1 = self.ui.listWidget_QRNG_Check_Qubits       
        self.QPU_QRNG_Change_Value.backend_name = self.ui.comboBox_QRNG_QPU_List.currentText()  
        self.QPU_QRNG_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_QRNG_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_QRNG_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
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
        self.ui.tab_Instruments_2.setEnabled(True)                      
        self.ui.tab_Modeling.setEnabled(True)                           
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
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
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
        self.QRNG_process.timezone = self.ui.spinBox_TAB0_TimeZone.value()                              
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
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
        self.ui.tab_Instruments_2.setEnabled(True)                      
        self.ui.tab_Modeling.setEnabled(True)                           
        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_process.full_path_for_NIST))
    def btnClicked_QRNG_SIMULATOR_Start(self):
        self.ui.frame_QRNG_Simulator.setEnabled(False)                              
        self.ui.frame_QRNG_RadioButtons.setEnabled(False)                           
        self.ui.tab_INFO.setEnabled(False)                                          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)                                   
        self.ui.tab_QKD.setEnabled(False)                                           
        self.ui.tab_Fourie.setEnabled(False)                                        
        self.ui.tab_Instruments.setEnabled(False)                                   
        self.ui.tab_Instruments_2.setEnabled(False)                                 
        self.ui.tab_Modeling.setEnabled(False)                                      
        self.QRNG_Simulator_process.token_name = self.ui.lineEdit_API_Token.text()                                          
        self.QRNG_Simulator_process.ibm_channel = self.ui.lineEdit_Channel.text()                                           
        self.QRNG_Simulator_process.num_of_qubits = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.value()           
        self.QRNG_Simulator_process.num_of_qubits_max = self.ui.horizontalSlider_QRNG_SIMULATOR_Num_of_Qubits.maximum()     
        self.QRNG_Simulator_process.alpha = self.ui.doubleSpinBox_QRNG_Sim_Alpha.value()                                    
        self.QRNG_Simulator_process.shots = self.ui.spinBox_QRNG_Sim_max_shots.value()                                      
        self.QRNG_Simulator_process.opt_level = self.ui.spinBox_QRNG_OptLevel.value()                                       
        self.QRNG_Simulator_process.flag_radio_button = self.ui.radioButton_QRNG_Sim_Slider_OK.isChecked()                  
        self.QRNG_Simulator_process.list_widget_3_2 = self.ui.listWidget_QRNG_Sim_Check_Qubits                              
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
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
        self.ui.tab_Instruments_2.setEnabled(True)                      
        self.ui.tab_Modeling.setEnabled(True)                           
        self.ui.lineEdit_NIST_Directory_to_Dataset.setText(str(self.QRNG_Simulator_process.full_path_for_NIST))
    def btnClicked_QRNG_JobID_Check(self):
        self.ui.lineEdit_QRNG_JobID.setEnabled(False)                   
        self.ui.pushButton_QRNG_JobID_Check.setEnabled(False)           
        self.ui.pushButton_QRNG_JobID_Cancel.setEnabled(False)          
        self.ui.pushButton_QRNG_JobID_Download.setEnabled(False)        
        self.Check_JobID.token_name = self.ui.lineEdit_API_Token.text()     
        self.Check_JobID.ibm_channel = self.ui.lineEdit_Channel.text()      
        self.Check_JobID.jobID = self.ui.lineEdit_QRNG_JobID.text()         
        self.Check_JobID.timezone = self.ui.spinBox_TAB0_TimeZone.value()   
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
        self.Check_JobID.timezone = self.ui.spinBox_TAB0_TimeZone.value()   
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
        self.Check_JobID.timezone = self.ui.spinBox_TAB0_TimeZone.value()       
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
        self.ui.tab_Instruments_2.setEnabled(False)                 
        self.ui.tab_Modeling.setEnabled(False)                      
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
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
            self.ui.tab_Instruments_2.setEnabled(True)                  
            self.ui.tab_Modeling.setEnabled(True)                       
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
    def combobox_TAB3_QPU_Changed(self):
        self.ui.listWidget_TAB3_QRNG_Bell.clear()
        self.ui.listWidget_TAB3_QKD_BB84.clear()
        self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.clear()
        self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.clear()
        self.ui.comboBox_TAB3_QPU_List.setEnabled(False)                
        self.ui.tab_INFO.setEnabled(False)                              
        self.ui.tab_QRNG.setEnabled(False)                              
        self.ui.tab_QKD.setEnabled(False)                               
        self.ui.tab_Fourie.setEnabled(False)                            
        self.ui.tab_Instruments.setEnabled(False)                       
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
        self.QPU_TAB3_Change_Value.list_widget_QRNG_Bell = self.ui.listWidget_TAB3_QRNG_Bell           
        self.QPU_TAB3_Change_Value.list_widget_QKD_BB84 = self.ui.listWidget_TAB3_QKD_BB84             
        self.QPU_TAB3_Change_Value.spinBox_max_shots = self.ui.spinBox_TAB3_max_shots  
        self.QPU_TAB3_Change_Value.backend_name = self.ui.comboBox_TAB3_QPU_List.currentText()  
        self.QPU_TAB3_Change_Value.ibm_channel = self.ui.lineEdit_Channel.text()                
        self.QPU_TAB3_Change_Value.ibm_instance = self.ui.lineEdit_Instance.text()              
        self.QPU_TAB3_Change_Value.token_name = self.ui.lineEdit_API_Token.text()               
        self.ui.textEdit_TAB0.clear()  
        self.ui.textEdit_TAB1.clear()  
        self.ui.textEdit_TAB2.clear()  
        self.ui.textEdit_TAB3.clear()  
        self.ui.textEdit_TAB5.clear()  
        self.ui.textEdit_TAB6.clear()  
        self.ui.textEdit_TAB7.clear()  
        self.QPU_TAB3_Change_Value.start()                                                  
        self.QPU_TAB3_Change_Value.finished.connect(self.onFinished_TAB3_QPU_Changed)  
    def onFinished_TAB3_QPU_Changed(self):
        self.ui.tab_INFO.setEnabled(True)               
        self.ui.tab_QRNG.setEnabled(True)               
        self.ui.tab_QKD.setEnabled(True)                
        self.ui.tab_Fourie.setEnabled(True)             
        self.ui.tab_Instruments.setEnabled(True)        
        self.ui.tab_Instruments_2.setEnabled(True)      
        self.ui.tab_Modeling.setEnabled(True)           
        self.ui.comboBox_TAB3_QPU_List.setEnabled(True)             
        self.ui.spinBox_TAB3_max_shots.setValue(self.ui.spinBox_TAB3_max_shots.maximum()) 
        path_to_config = os.path.expanduser("~") + "/Documents/QISs/QKD/QRNG_BELL/Config/"
        path_to_config_BB84 = os.path.expanduser("~") + "/Documents/QISs/QKD/BB84/Config/"
        if not (os.path.exists(path_to_config)) | (os.path.exists(path_to_config_BB84)):  return
        else:
            if os.path.exists(path_to_config):
                try:
                    for dirpath, dnames, fnames in os.walk(path_to_config):
                        for f in fnames:
                            if f.endswith(".config"):
                                full_path_to_config = os.path.join(dirpath, f)
                                self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.setText(full_path_to_config)
                                try:
                                    if self.ui.listWidget_TAB3_QRNG_Bell.count() == 0:  raise Exception("ListWidget Пуст")
                                    else:
                                        with open(full_path_to_config, "r") as fp:  lines = fp.readlines()
                                        for i in range(0, len(lines)):
                                            had = lines[i].split('=')[1].split(':')[0]
                                            cnot = lines[i].split('=')[1].split(':')[1].strip('\n')
                                            try:
                                                self.ui.listWidget_TAB3_QRNG_Bell.item(int(had)).setCheckState(QtCore.Qt.Checked)
                                                if cnot != "":  self.ui.listWidget_TAB3_QRNG_Bell.item(int(cnot)).setCheckState(QtCore.Qt.Checked)
                                            except Exception as exx:    print(f'Ошибка при выборе checkBox по данным конфигурационного файла:\n{exx}')
                                        print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ КГСЧ ПО БЕЛЛУ--------')
                                        print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {full_path_to_config}--------\n')
                                        for i in range(0, len(lines)):  print(lines[i].strip('\n'))
                                except Exception as ex:
                                    print(f'ListWidget Error: {ex}')
                            break
                except Exception: pass
            if os.path.exists(path_to_config_BB84):
                try:
                    for dirpath, dnames, fnames in os.walk(path_to_config_BB84):
                        for f in fnames:
                            if f.endswith(".config"):
                                full_path_to_config_BB84 = os.path.join(dirpath, f)
                                self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.setText(full_path_to_config_BB84)
                                try:
                                    if self.ui.listWidget_TAB3_QKD_BB84.count() == 0:   raise Exception("ListWidget Пуст")
                                    else:
                                        with open(full_path_to_config_BB84, "r") as fp: lines = fp.readlines()
                                        for i in range(0, len(lines)):
                                            had_Alc_1 = re.split("=|:", lines[i])[1]
                                            had_Alc_2 = re.split(":|;", lines[i])[1]
                                            had_Bob_1 = re.split(";|!", lines[i])[1]
                                            had_Eve_1 = re.split("!|\+", lines[i])[1]
                                            qub_Alc = re.split("\+|/", lines[i])[1]
                                            qub_Bob = re.split("/|\*", lines[i])[1]
                                            qub_Eve = lines[i].split('*')[1].strip('\n')
                                            try:
                                                if had_Alc_1 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Alc_1)).setCheckState(QtCore.Qt.Checked)
                                                if had_Alc_2 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Alc_2)).setCheckState(QtCore.Qt.Checked)
                                                if had_Bob_1 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Bob_1)).setCheckState(QtCore.Qt.Checked)
                                                if had_Eve_1 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Eve_1)).setCheckState(QtCore.Qt.Checked)
                                                if qub_Alc != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Checked)
                                                if qub_Bob != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Checked)
                                                if qub_Eve != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Checked)
                                            except Exception as exx:    print(f'Ошибка при выборе checkBox по данным конфигурационного файла:\n{exx}')
                                        print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ ККС ВРК BB84--------')
                                        print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {full_path_to_config_BB84}--------\n')
                                        for i in range(0, len(lines)):  print(lines[i].strip('\n'))
                                        print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
                                except Exception as ex:
                                    print(f'ListWidget Error: {ex}')
                            break
                except Exception:   pass
    def listWidget_TAB3_QRNG_Bell_Clicked(self, chkbx_index, checked_flag):
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/QKD/QRNG_BELL/Config/" + str(current_date)
        if checked_flag == 2:
            file_name = self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.text()
            if file_name == "":
                file_name = 'Bell.config'
                if not os.path.exists(path_to_result):  create_dir(path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                if not os.path.exists(dst_path):    os.mknod(dst_path)
                self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.setText(str(dst_path))
            else:
                if not os.path.exists(path_to_result):  create_dir(path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                if not os.path.exists(dst_path):    os.mknod(dst_path)
            try:
                with open(dst_path, "r") as fp:
                    lines = fp.readlines(); len_of_config_file = len(lines)
                    for i in range(0, len_of_config_file):
                        had_in_file = lines[i].split('=')[1].split(':')[0]
                        cnot_in_file = lines[i].split('=')[1].split(':')[1].strip('\n')
                        if (str(chkbx_index) == had_in_file) | (str(chkbx_index) == cnot_in_file):  return
                    with open(dst_path, "w") as fp:
                        if len_of_config_file == 0: str_res = "BellPair=" + str(chkbx_index) + ':';  fp.write(str_res); lines.append(str_res)
                        else:
                            index_for_rewrite = 0
                            for i in range(0, len_of_config_file):
                                qubit_cnot = lines[i].split('=')[1].split(':')[1].strip('\n')
                                if qubit_cnot == "":    index_for_rewrite = i;  break
                            qubit_cnot = lines[index_for_rewrite].split('=')[1].split(':')[1].strip('\n')
                            if qubit_cnot == "":
                                lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '\n'
                                for line in lines:  fp.write(line)
                            else:
                                str_res = "BellPair=" + str(chkbx_index) + ':'; lines.append(str_res)
                                for line in lines:  fp.write(line)
                    if self.ui.listWidget_TAB3_QRNG_Bell.item(int(chkbx_index)).checkState() == Qt.Unchecked:
                            self.ui.listWidget_TAB3_QRNG_Bell.item(int(chkbx_index)).setCheckState(QtCore.Qt.Checked)
                    self.ui.textEdit_TAB3.clear()
                    print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ КГСЧ ПО БЕЛЛУ--------\n')
                    print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                    for i in range(0, len(lines)):
                        print(lines[i].strip('\n'))
                    print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
            except Exception:   return
        elif checked_flag == 0:
            file_name = self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.text()
            dst_path = os.path.join(path_to_result, file_name)
            if not os.path.exists(path_to_result):  return
            if not os.path.exists(dst_path):    return
            try:
                with open(dst_path, "r") as fp:
                    lines = fp.readlines()
                    lines_console = lines.copy()
                    with open(dst_path, "w") as fp:
                        for index, line in enumerate(lines):
                            qubit_hadamard = line.split('=')[1].split(':')[0]
                            try:    qubit_cnot = line.split('=')[1].split(':')[1].strip('\n')
                            except Exception:   qubit_cnot = ""
                            if qubit_cnot == str(chkbx_index):  fp.write((lines[index].split(':')[0]) + ':\n'); lines_console[index] = lines_console[index].split(':')[0] + ':'
                            elif (qubit_hadamard == str(chkbx_index)) & (qubit_cnot != ""): self.ui.listWidget_TAB3_QRNG_Bell.item(int(qubit_cnot)).setCheckState(QtCore.Qt.Unchecked); lines_console.pop(index)
                            elif (qubit_hadamard == str(chkbx_index)):  pass;   lines_console.pop(index)
                            else:   fp.write(lines[index])
                    self.ui.textEdit_TAB3.clear()
                    print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ КГСЧ ПО БЕЛЛУ--------\n')
                    print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                    for i in range(0, len(lines_console)):
                        print(lines_console[i].strip('\n'))
                    print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
            except Exception:   return
        else:   self.ui.textEdit_TAB3.clear();  print("\nОшибка при определении статуса checkBox\n");   return
    def lineEdit_TAB3_QRNG_Bell_Changed(self):
        try:
            for i in range(self.ui.listWidget_TAB3_QRNG_Bell.count()):
                if self.ui.listWidget_TAB3_QRNG_Bell.item(i).checkState() == Qt.Checked:
                    self.ui.listWidget_TAB3_QRNG_Bell.item(i).setCheckState(QtCore.Qt.Unchecked)
        except Exception as ex:
            print(f'ListWidget Error: {ex}')
    def btnClicked_TAB3_Browse_Config(self):
        self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.clear()
        dialog = QFileDialog(self)
        folder_path = \
            dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.config)",
                                   options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.setText(str(folder_path))
        try:
            current_date = date.today()
            path_to_result = os.path.expanduser("~") + "/Documents/QISs/QKD/QRNG_BELL/Config/" + str(current_date)
            if not os.path.exists(path_to_result):  create_dir(path_to_result)
            input_config = self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.text()
            file_name = os.path.basename(input_config)
            if os.path.dirname(os.path.abspath(input_config)) != path_to_result:
                shutil.copy(input_config, path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.setText(str(dst_path))
            else:   dst_path = input_config
            if self.ui.listWidget_TAB3_QRNG_Bell.count() == 0:  print("ListWidget Пуст");   return
            else:
                with open(dst_path, "r") as fp: lines = fp.readlines()
                for i in range(0, len(lines)):
                    had = lines[i].split('=')[1].split(':')[0]
                    cnot = lines[i].split('=')[1].split(':')[1].strip('\n')
                    try:
                        self.ui.listWidget_TAB3_QRNG_Bell.item(int(had)).setCheckState(QtCore.Qt.Checked)
                        if cnot != "":  self.ui.listWidget_TAB3_QRNG_Bell.item(int(cnot)).setCheckState(QtCore.Qt.Checked)
                    except Exception as exx:    print(f'Ошибка при выборе checkBox по данным конфигурационного файла:\n{exx}')
                self.ui.textEdit_TAB3.clear()
                print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ КГСЧ ПО БЕЛЛУ--------\n')
                print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                for i in range(0, len(lines)):
                    print(lines[i].strip('\n'))
                print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
        except Exception as ex: print(f'Возникло исключение: {ex}')
    def btnClicked_TAB3_QRNG_Bell_Start(self):
        self.ui.tab_INFO.setEnabled(False)           
        self.ui.tab_QRNG.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)         
        self.ui.tab_Instruments.setEnabled(False)    
        self.ui.tab_Instruments_2.setEnabled(False)  
        self.ui.tab_Modeling.setEnabled(False)       
        self.ui.frame_TAB3_QRNG_Bell.setEnabled(False)   
        self.ui.frame_TAB3_QKD_BB84.setEnabled(False)         
        self.QRNGBell_process.token_name = self.ui.lineEdit_API_Token.text()                        
        self.QRNGBell_process.ibm_channel = self.ui.lineEdit_Channel.text()                         
        self.QRNGBell_process.backend_name = self.ui.comboBox_TAB3_QPU_List.currentText()           
        self.QRNGBell_process.shots = self.ui.spinBox_TAB3_max_shots.value()                        
        self.QRNGBell_process.alpha = self.ui.doubleSpinBox_TAB3_Alpha.value()                      
        self.QRNGBell_process.opt_level = self.ui.spinBox_TAB3_OptLevel.value()                     
        self.QRNGBell_process.timezone = self.ui.spinBox_TAB0_TimeZone.value()                      
        self.QRNGBell_process.use_barriers = self.ui.checkBox_TAB3_Barriers.isChecked()             
        self.QRNGBell_process.num_of_qubits_max = self.ui.listWidget_TAB3_QRNG_Bell.count()         
        self.QRNGBell_process.file_config = self.ui.lineEdit_TAB3_QRNG_Bell_Name_of_Config.text()   
        self.QRNGBell_process.finished.connect(self.onFinished_TAB3_QRNG_Bell)  
        self.QRNGBell_process.start()  
    def onFinished_TAB3_QRNG_Bell(self):
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
        self.ui.frame_TAB3_QRNG_Bell.setEnabled(True)   
        self.ui.frame_TAB3_QKD_BB84.setEnabled(True)         
    def listWidget_TAB3_QKD_BB84_Clicked(self, chkbx_index, checked_flag):
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/QKD/BB84/Config/" + str(current_date)
        if checked_flag == 2:
            file_name = self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.text()
            if file_name == "":
                file_name = 'BB84.config'
                if not os.path.exists(path_to_result):  create_dir(path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                if not os.path.exists(dst_path):    os.mknod(dst_path)
                self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.setText(str(dst_path))
            else:
                if not os.path.exists(path_to_result):  create_dir(path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                if not os.path.exists(dst_path):    os.mknod(dst_path)
            try:
                with open(dst_path, "r") as fp:
                    lines = fp.readlines(); len_of_config_file = len(lines)
                    for i in range(0, len_of_config_file):
                        had_Alc_1 = ""; had_Alc_2 = ""; had_Bob_1 = ""; had_Eve_1 = ""; qub_Alc = "";   qub_Bob = "";   qub_Eve = ""
                        try:
                            had_Alc_1 = re.split("=|:", lines[i])[1]
                            if lines[i].endswith('\n'):
                                for j in range(0, len(lines[i].strip('\n')) - 1)[::-1]:
                                    symb = str(lines[i][j])
                                    if symb.isdigit():  pass
                                    else:
                                        if str(lines[i].strip('\n')[-1]).isdigit(): last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                        else:   last_number_in_str = int((lines[i])[j + 1:-2].strip('\n')); break
                            else:
                                for j in range(0, len(lines[i]) - 1)[::-1]:
                                    symb = str(lines[i][j])
                                    if symb.isdigit():  pass
                                    else:   last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                            if had_Alc_1 != str(last_number_in_str):
                                had_Alc_2 = re.split(":|;", lines[i])[1]
                                if had_Alc_2 != str(last_number_in_str):
                                    had_Bob_1 = re.split(";|!", lines[i])[1]
                                    if had_Bob_1 != str(last_number_in_str):
                                        had_Eve_1 = re.split("!|\+", lines[i])[1]
                                        if had_Eve_1 != str(last_number_in_str):
                                            qub_Alc = re.split("\+|/", lines[i])[1]
                                            if qub_Alc != str(last_number_in_str):
                                                qub_Bob = re.split("/|\*", lines[i])[1]
                                                if qub_Bob != str(last_number_in_str):
                                                    qub_Eve = lines[i].split('*')[1].strip('\n')
                        except Exception as ex: print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
                        if (str(chkbx_index) == had_Alc_1) | (str(chkbx_index) == had_Alc_2) | (str(chkbx_index) == had_Bob_1) | (
                                str(chkbx_index) == had_Eve_1) | (str(chkbx_index) == qub_Alc) | (
                                str(chkbx_index) == qub_Bob) | (str(chkbx_index) == qub_Eve):   return
                    with open(dst_path, "w") as fp:
                        if len_of_config_file == 0: str_res = "BB84=" + str(chkbx_index) + ':';  fp.write(str_res); lines.append(str_res)
                        else:
                            index_for_rewrite = 0
                            for i in range(0, len_of_config_file):
                                had_Alc_1 = ""; had_Alc_2 = ""; had_Bob_1 = ""; had_Eve_1 = ""; qub_Alc = "";   qub_Bob = "";   qub_Eve = ""
                                try:
                                    had_Alc_1 = re.split("=|:", lines[i])[1]
                                    if lines[i].endswith('\n'):
                                        for j in range(0, len(lines[i].strip('\n')) - 1)[::-1]:
                                            symb = str(lines[i][j])
                                            if symb.isdigit():  pass
                                            else:
                                                if str(lines[i].strip('\n')[-1]).isdigit(): last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                                else:   last_number_in_str = int((lines[i])[j + 1:-2].strip('\n')); break
                                    else:
                                        for j in range(0, len(lines[i]) - 1)[::-1]:
                                            symb = str(lines[i][j])
                                            if symb.isdigit():  pass
                                            else:   last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                    if had_Alc_1 != str(last_number_in_str):
                                        had_Alc_2 = re.split(":|;", lines[i])[1]
                                        if had_Alc_2 != str(last_number_in_str):
                                            had_Bob_1 = re.split(";|!", lines[i])[1]
                                            if had_Bob_1 != str(last_number_in_str):
                                                had_Eve_1 = re.split("!|\+", lines[i])[1]
                                                if had_Eve_1 != str(last_number_in_str):
                                                    qub_Alc = re.split("\+|/", lines[i])[1]
                                                    if qub_Alc != str(last_number_in_str):
                                                        qub_Bob = re.split("/|\*", lines[i])[1]
                                                        if qub_Bob != str(last_number_in_str):
                                                            qub_Eve = lines[i].split('*')[1].strip('\n')
                                except Exception as ex:
                                    print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
                                if (had_Alc_1 == "") | (had_Alc_2 == "") | (
                                        had_Bob_1 == "") | (had_Eve_1 == "") | (
                                        qub_Alc == "") \
                                        | (qub_Bob == "") | (qub_Eve == ""):    index_for_rewrite = i;  break
                            flag_position = "had_Alc_2"
                            try:
                                had_Alc_1 = re.split("=|:", lines[index_for_rewrite])[1]
                                if lines[i].endswith('\n'):
                                    for j in range(0, len(lines[i].strip('\n')) - 1)[::-1]:
                                        symb = str(lines[i][j])
                                        if symb.isdigit():  pass
                                        else:
                                            if str(lines[i].strip('\n')[-1]).isdigit(): last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                            else:   last_number_in_str = int((lines[i])[j + 1:-2].strip('\n')); break
                                else:
                                    for j in range(0, len(lines[i]) - 1)[::-1]:
                                        symb = str(lines[i][j])
                                        if symb.isdigit():  pass
                                        else:   last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                if had_Alc_1 != str(last_number_in_str):
                                    had_Alc_2 = re.split(":|;", lines[index_for_rewrite])[1];   flag_position = "had_Bob_1"
                                    if had_Alc_2 != str(last_number_in_str):
                                        had_Bob_1 = re.split(";|!", lines[index_for_rewrite])[1];   flag_position = "had_Eve_1"
                                        if had_Bob_1 != str(last_number_in_str):
                                            had_Eve_1 = re.split("!|\+", lines[index_for_rewrite])[1];  flag_position = "qub_Alc"
                                            if had_Eve_1 != str(last_number_in_str):
                                                qub_Alc = re.split("\+|/", lines[index_for_rewrite])[1];    flag_position = "qub_Bob"
                                                if qub_Alc != str(last_number_in_str):
                                                    qub_Bob = re.split("/|\*", lines[index_for_rewrite])[1];    flag_position = "qub_Eve"
                                                    if qub_Bob != str(last_number_in_str):
                                                        qub_Eve = lines[index_for_rewrite].split('*')[1].strip('\n');   flag_position = "had_Alc_1"
                            except Exception as ex:
                                print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
                            if flag_position == "had_Alc_1":
                                str_res = "BB84=" + str(chkbx_index) + ':'; lines.append(str_res)
                                for line in lines:  fp.write(line)
                            elif flag_position == "had_Alc_2":
                                if index_for_rewrite == len_of_config_file - 1: lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + ';'
                                else:   lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + ';\n'
                                for line in lines:  fp.write(line)
                            elif flag_position == "had_Bob_1":
                                if index_for_rewrite == len_of_config_file - 1: lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '!'
                                else:   lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '!\n'
                                for line in lines:  fp.write(line)
                            elif flag_position == "had_Eve_1":
                                if index_for_rewrite == len_of_config_file - 1: lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '+'
                                else:   lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '+\n'
                                for line in lines:  fp.write(line)
                            elif flag_position == "qub_Alc":
                                if index_for_rewrite == len_of_config_file - 1: lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '/'
                                else:   lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '/\n'
                                for line in lines:  fp.write(line)
                            elif flag_position == "qub_Bob":
                                if index_for_rewrite == len_of_config_file - 1: lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '*'
                                else:   lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '*\n'
                                for line in lines:  fp.write(line)
                            elif flag_position == "qub_Eve":
                                lines[index_for_rewrite] = lines[index_for_rewrite].strip('\n') + str(chkbx_index) + '\n'
                                for line in lines:  fp.write(line)
                    if self.ui.listWidget_TAB3_QKD_BB84.item(int(chkbx_index)).checkState() == Qt.Unchecked:
                        self.ui.listWidget_TAB3_QKD_BB84.item(int(chkbx_index)).setCheckState(QtCore.Qt.Checked)
                    self.ui.textEdit_TAB3.clear()
                    print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ ККС ВРК BB84--------\n')
                    print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                    for i in range(0, len(lines)):  print(lines[i].strip('\n'))
                    print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
            except Exception:
                return
        elif checked_flag == 0:
            file_name = self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.text()
            dst_path = os.path.join(path_to_result, file_name)
            if not os.path.exists(path_to_result):  return
            if not os.path.exists(dst_path):    return
            try:
                with open(dst_path, "r") as fp:
                    lines = fp.readlines()
                    lines_console = lines.copy()
                    with open(dst_path, "w") as fp:
                        for index, line in enumerate(lines):
                            had_Alc_1 = ""; had_Alc_2 = ""; had_Bob_1 = ""; had_Eve_1 = ""; qub_Alc = "";   qub_Bob = "";   qub_Eve = ""
                            try:
                                had_Alc_1 = re.split("=|:", line)[1]
                                if line.endswith('\n'):
                                    for j in range(0, len(line.strip('\n')) - 1)[::-1]:
                                        symb = str(line[j])
                                        if symb.isdigit():  pass
                                        else:
                                            if str(line.strip('\n')[-1]).isdigit(): last_number_in_str = int((line)[j + 1:-1].strip('\n')); break
                                            else:   last_number_in_str = int((line)[j + 1:-2].strip('\n')); break
                                else:
                                    for j in range(0, len(line) - 1)[::-1]:
                                        symb = str(line[j])
                                        if symb.isdigit():  pass
                                        else:   last_number_in_str = int((line)[j + 1:-1].strip('\n')); break
                                if had_Alc_1 != str(last_number_in_str):
                                    had_Alc_2 = re.split(":|;", line)[1]
                                    if had_Alc_2 != str(last_number_in_str):
                                        had_Bob_1 = re.split(";|!", line)[1]
                                        if had_Bob_1 != str(last_number_in_str):
                                            had_Eve_1 = re.split("!|\+", line)[1]
                                            if had_Eve_1 != str(last_number_in_str):
                                                qub_Alc = re.split("\+|/", line)[1]
                                                if qub_Alc != str(last_number_in_str):
                                                    qub_Bob = re.split("/|\*", line)[1]
                                                    if qub_Bob != str(last_number_in_str):
                                                        qub_Eve = line.split('*')[1].strip('\n')
                            except Exception as ex:
                                print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
                            if qub_Eve == str(chkbx_index):
                                if index == len(lines) - 1: fp.write((lines[index].split('*')[0]) + '*')
                                else:   fp.write((lines[index].split('*')[0]) + '*\n')
                                lines_console[index] = lines_console[index].split('*')[0] + '*'
                            elif (qub_Bob == str(chkbx_index)):
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                if index == len(lines) - 1: fp.write((lines[index].split('/')[0]) + '/')
                                else:   fp.write((lines[index].split('/')[0]) + '/\n')
                                lines_console[index] = lines_console[index].split('/')[0] + '/'
                            elif (qub_Alc == str(chkbx_index)):
                                if qub_Bob != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                if index == len(lines) - 1: fp.write((lines[index].split('+')[0]) + '+')
                                else:   fp.write((lines[index].split('+')[0]) + '+\n')
                                lines_console[index] = lines_console[index].split('+')[0] + '+'
                            elif (had_Eve_1 == str(chkbx_index)):
                                if qub_Alc != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Bob != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                if index == len(lines) - 1: fp.write((lines[index].split('!')[0]) + '!')
                                else:   fp.write((lines[index].split('!')[0]) + '!\n')
                                lines_console[index] = lines_console[index].split('!')[0] + '!'
                            elif (had_Bob_1 == str(chkbx_index)):
                                if had_Eve_1 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Eve_1)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Alc != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Bob != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                if index == len(lines) - 1: fp.write((lines[index].split(';')[0]) + ';')
                                else:   fp.write((lines[index].split(';')[0]) + ';\n')
                                lines_console[index] = lines_console[index].split(';')[0] + ';'
                            elif (had_Alc_2 == str(chkbx_index)):
                                if had_Bob_1 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Bob_1)).setCheckState(QtCore.Qt.Unchecked)
                                if had_Eve_1 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Eve_1)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Alc != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Bob != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                if index == len(lines) - 1: fp.write((lines[index].split(':')[0]) + ':')
                                else:   fp.write((lines[index].split(':')[0]) + ':\n')
                                lines_console[index] = lines_console[index].split(':')[0] + ':'
                            elif (had_Alc_1 == str(chkbx_index)):
                                if had_Alc_2 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Alc_2)).setCheckState(QtCore.Qt.Unchecked)
                                if had_Bob_1 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Bob_1)).setCheckState(QtCore.Qt.Unchecked)
                                if had_Eve_1 != "": self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Eve_1)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Alc != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Bob != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Unchecked)
                                if qub_Eve != "":   self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Unchecked)
                                lines_console.pop(index)
                            else:
                                fp.write(lines[index])
                    self.ui.textEdit_TAB3.clear()
                    print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ ККС ВРК ВВ84--------\n')
                    print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                    for i in range(0, len(lines_console)):  print(lines_console[i].strip('\n'))
                    print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
            except Exception:   return
        else:   self.ui.textEdit_TAB3.clear();  print("\nОшибка при определении статуса checkBox\n");   return
    def lineEdit_TAB3_QKD_BB84_Changed(self):
        try:
            for i in range(self.ui.listWidget_TAB3_QKD_BB84.count()):
                if self.ui.listWidget_TAB3_QKD_BB84.item(i).checkState() == Qt.Checked:
                    self.ui.listWidget_TAB3_QKD_BB84.item(i).setCheckState(QtCore.Qt.Unchecked)
        except Exception as ex:
            print(f'ListWidget Error: {ex}')
    def btnClicked_TAB3_QKD_BB84_Browse_Config(self):
        self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.clear()
        dialog = QFileDialog(self)
        folder_path = \
            dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.config)",
                                   options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.setText(str(folder_path))
        try:
            current_date = date.today()
            path_to_result = os.path.expanduser("~") + "/Documents/QISs/QKD/BB84/Config/" + str(current_date)
            if not os.path.exists(path_to_result):  create_dir(path_to_result)
            input_config = self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.text()
            file_name = os.path.basename(input_config)
            if os.path.dirname(os.path.abspath(input_config)) != path_to_result:
                shutil.copy(input_config, path_to_result)
                dst_path = os.path.join(path_to_result, file_name)
                self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.setText(str(dst_path))
            else:   dst_path = input_config
            if self.ui.listWidget_TAB3_QKD_BB84.count() == 0:   print("ListWidget Пуст");   return
            else:
                with open(dst_path, "r") as fp: lines = fp.readlines()
                for i in range(0, len(lines)):
                    had_Alc_1 = ""; had_Alc_2 = ""; had_Bob_1 = ""; had_Eve_1 = ""; qub_Alc = "";   qub_Bob = "";   qub_Eve = ""
                    try:
                        had_Alc_1 = re.split("=|:", lines[i])[1]
                        if lines[i].endswith('\n'):
                            for j in range(0, len(lines[i].strip('\n')) - 1)[::-1]:
                                symb = str(lines[i][j])
                                if symb.isdigit():  pass
                                else:
                                    if str(lines[i].strip('\n')[-1]).isdigit(): last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                                    else:   last_number_in_str = int((lines[i])[j + 1:-2].strip('\n')); break
                        else:
                            for j in range(0, len(lines[i]) - 1)[::-1]:
                                symb = str(lines[i][j])
                                if symb.isdigit():  pass
                                else:   last_number_in_str = int((lines[i])[j + 1:-1].strip('\n')); break
                        if had_Alc_1 != str(last_number_in_str):
                            had_Alc_2 = re.split(":|;", lines[i])[1]
                            if had_Alc_2 != str(last_number_in_str):
                                had_Bob_1 = re.split(";|!", lines[i])[1]
                                if had_Bob_1 != str(last_number_in_str):
                                    had_Eve_1 = re.split("!|\+", lines[i])[1]
                                    if had_Eve_1 != str(last_number_in_str):
                                        qub_Alc = re.split("\+|/", lines[i])[1]
                                        if qub_Alc != str(last_number_in_str):
                                            qub_Bob = re.split("/|\*", lines[i])[1]
                                            if qub_Bob != str(last_number_in_str):
                                                qub_Eve = lines[i].split('*')[1].strip('\n')
                    except Exception as ex:
                        print(f"Не удалось корректно считать данные из {i} строки конфигурационного файла", ex)
                    try:
                        self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Alc_1)).setCheckState(QtCore.Qt.Checked)
                        if had_Alc_2 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Alc_2)).setCheckState(QtCore.Qt.Checked)
                        if had_Bob_1 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Bob_1)).setCheckState(QtCore.Qt.Checked)
                        if had_Eve_1 != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(had_Eve_1)).setCheckState(QtCore.Qt.Checked)
                        if qub_Alc != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Alc)).setCheckState(QtCore.Qt.Checked)
                        if qub_Bob != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Bob)).setCheckState(QtCore.Qt.Checked)
                        if qub_Eve != "":  self.ui.listWidget_TAB3_QKD_BB84.item(int(qub_Eve)).setCheckState(QtCore.Qt.Checked)
                    except Exception as exx:    print(f'Ошибка при выборе checkBox по данным конфигурационного файла:\n{exx}')
                self.ui.textEdit_TAB3.clear()
                print('\n--------КОРРЕКТИРОВКА КУБИТ ДЛЯ РЕАЛИЗАЦИИ ККС ВРК ВВ84--------\n')
                print(f'--------КОНФИГУРАЦИОННЫЙ ФАЙЛ: {dst_path}--------\n')
                for i in range(0, len(lines)):  print(lines[i].strip('\n'))
                print('\n--------ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО--------\n')
        except Exception as ex: print(f'Возникло исключение: {ex}')
    def btnClicked_TAB3_QKD_BB84_Start(self):
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        self.ui.frame_TAB3_QRNG_Bell.setEnabled(False)  
        self.ui.frame_TAB3_QKD_BB84.setEnabled(False)   
        self.QKDBB84_process.token_name = self.ui.lineEdit_API_Token.text()                
        self.QKDBB84_process.ibm_channel = self.ui.lineEdit_Channel.text()                 
        self.QKDBB84_process.backend_name = self.ui.comboBox_TAB3_QPU_List.currentText()   
        self.QKDBB84_process.shots = self.ui.spinBox_TAB3_max_shots.value()                
        self.QKDBB84_process.alpha = self.ui.doubleSpinBox_TAB3_Alpha.value()              
        self.QKDBB84_process.opt_level = self.ui.spinBox_TAB3_OptLevel.value()             
        self.QKDBB84_process.timezone = self.ui.spinBox_TAB0_TimeZone.value()              
        self.QKDBB84_process.use_barriers = self.ui.checkBox_TAB3_Barriers.isChecked()     
        self.QKDBB84_process.num_of_qubits_max = self.ui.listWidget_TAB3_QKD_BB84.count()  
        self.QKDBB84_process.flag_eve = self.ui.checkBox_TAB3_QKD_BB84_Flag_Eve.isChecked()
        self.QKDBB84_process.file_config = self.ui.lineEdit_TAB3_QKD_BB84_Name_of_Config.text()  
        self.QKDBB84_process.finished.connect(self.onFinished_TAB3_QKD_BB84)  
        self.QKDBB84_process.start()  
    def onFinished_TAB3_QKD_BB84(self):
        self.ui.tab_INFO.setEnabled(True)               
        self.ui.tab_QRNG.setEnabled(True)               
        self.ui.tab_Fourie.setEnabled(True)             
        self.ui.tab_Instruments.setEnabled(True)        
        self.ui.tab_Instruments_2.setEnabled(True)      
        self.ui.tab_Modeling.setEnabled(True)           
        self.ui.frame_TAB3_QRNG_Bell.setEnabled(True)   
        self.ui.frame_TAB3_QKD_BB84.setEnabled(True)    
    def rdFileSeqMergeBAD(self):
        self.ui.spinBox_TAB5_FilesSequences_User_Qubit.setEnabled(False)
    def rdFileSeqMergeGOOD(self):
        self.ui.spinBox_TAB5_FilesSequences_User_Qubit.setEnabled(False)
    def rdFileSeqMergeALL(self):
        self.ui.spinBox_TAB5_FilesSequences_User_Qubit.setEnabled(False)
    def rdFileSeqMergeUSER(self):
        self.ui.spinBox_TAB5_FilesSequences_User_Qubit.setEnabled(True)
    def chkBox_TAB5_Select_All_LEFT_Headers(self):
        if self.ui.checkBox_TAB5_Left_All.isChecked():
            try:
                for index in range(self.ui.listWidget_TAB5_csv_Header_1.count()):
                    if self.ui.listWidget_TAB5_csv_Header_1.item(index).checkState() == Qt.Unchecked:
                        self.ui.listWidget_TAB5_csv_Header_1.item(index).setCheckState(QtCore.Qt.Checked)
            except: print("Не сработало...")
        else:
            try:
                for index in range(self.ui.listWidget_TAB5_csv_Header_1.count()):
                    if self.ui.listWidget_TAB5_csv_Header_1.item(index).checkState() == Qt.Checked:
                        self.ui.listWidget_TAB5_csv_Header_1.item(index).setCheckState(QtCore.Qt.Unchecked)
            except: print("Не сработало...")
    def chkBox_TAB5_Select_All_RIGHT_Headers(self):
        if self.ui.checkBox_TAB5_Right_All.isChecked():
            try:
                for index in range(self.ui.listWidget_TAB5_csv_Header_2.count()):
                    if self.ui.listWidget_TAB5_csv_Header_2.item(index).checkState() == Qt.Unchecked:
                        self.ui.listWidget_TAB5_csv_Header_2.item(index).setCheckState(QtCore.Qt.Checked)
            except: print("Не сработало...")
        else:
            try:
                for index in range(self.ui.listWidget_TAB5_csv_Header_2.count()):
                    if self.ui.listWidget_TAB5_csv_Header_2.item(index).checkState() == Qt.Checked:
                        self.ui.listWidget_TAB5_csv_Header_2.item(index).setCheckState(QtCore.Qt.Unchecked)
            except: print("Не сработало...")
    def btnClicked_BITMAP_Path_to_File(self):
        self.ui.lineEdit_TAB5_Bitmap_Directory_Dialog.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_TAB5_Bitmap_Directory_Dialog.setText(str(folder_path))
    def btnClicked_BITMAP_Start(self):
        self.ui.textEdit_TAB0.clear()               
        self.ui.textEdit_TAB1.clear()               
        self.ui.textEdit_TAB2.clear()               
        self.ui.textEdit_TAB3.clear()               
        self.ui.textEdit_TAB5.clear()               
        self.ui.textEdit_TAB6.clear()               
        self.ui.textEdit_TAB7.clear()               
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
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
        self.ui.tab_Instruments.setEnabled(True)                           
        self.ui.tab_Instruments_2.setEnabled(True)                         
        self.ui.tab_Modeling.setEnabled(True)                              
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
        self.ui.tab_Instruments.setEnabled(False)               
        self.ui.tab_Instruments_2.setEnabled(False)             
        self.ui.tab_Modeling.setEnabled(False)                  
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
        self.ui.tab_Instruments.setEnabled(True)                       
        self.ui.tab_Instruments_2.setEnabled(True)                     
        self.ui.tab_Modeling.setEnabled(True)                          
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
        self.ui.tab_Instruments.setEnabled(False)                       
        self.ui.tab_Instruments_2.setEnabled(False)                     
        self.ui.tab_Modeling.setEnabled(False)                          
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
        self.ui.tab_Instruments.setEnabled(True)                       
        self.ui.tab_Instruments_2.setEnabled(True)                     
        self.ui.tab_Modeling.setEnabled(True)                          
        self.ui.frame_Bitmp.setEnabled(True)                           
        self.ui.frame_Fcorr_Easy.setEnabled(True)                      
        self.ui.pushButton_TAB5_Seq1_Dialog_profi.setEnabled(True)     
        self.ui.pushButton_TAB5_Seq2_Dialog_profi.setEnabled(True)     
        self.ui.pushButton_TAB5_Fcorrelation_profi.setEnabled(True)    
    def btnClicked_CorrMatrix_Path_to_File(self):
        self.ui.lineEdit_TAB5_CorMatrix_Directory_Dialog.clear()
        dialog = QFileDialog(self)
        folder_path = \
            dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.csv)",
                                   options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB5_CorMatrix_Directory_Dialog.setText(str(folder_path))
    def btnClicked_CorrMatrix_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_pictures = os.path.expanduser("~") + "/Documents/QISs/Instruments/Corr/Fcorr_Matrix/" + str(current_date)
        self.FCorrMatrix_process.csv_for_matrix = self.ui.lineEdit_TAB5_CorMatrix_Directory_Dialog.text()
        self.FCorrMatrix_process.path_for_output_txt = path_to_pictures
        self.FCorrMatrix_process.path_for_output_image = path_to_pictures
        self.FCorrMatrix_process.method = self.ui.lineEdit_TAB5_CorMatrix_Method.text()
        self.FCorrMatrix_process.start()  
        self.FCorrMatrix_process.finished.connect(self.onFinished_CorrMatrix)  
    def onFinished_CorrMatrix(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_FileSeq_Path_to_Folder(self):
        self.ui.lineEdit_TAB5_FilesSequences_Directory_Dialog.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:",
                                                  options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_TAB5_FilesSequences_Directory_Dialog.setText(str(folder_path))
    def btnClicked_FileSeq_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments/Merge/Sequences/" + str(current_date) + '/experiment'
        self.Merge_FileSeq_process.path_for_sequences = self.ui.lineEdit_TAB5_FilesSequences_Directory_Dialog.text()
        self.Merge_FileSeq_process.path_for_distination = path_to_result
        self.Merge_FileSeq_process.save_in_common_folder = self.ui.checkBox_TAB5_FilesSequences_Common.isChecked()
        if self.ui.radioButton_TAB5_FilesSequences_User_Seq.isChecked():
            self.Merge_FileSeq_process.Seq_USER = self.ui.spinBox_TAB5_FilesSequences_User_Qubit.value()
        else:
            self.Merge_FileSeq_process.Seq_USER = -1
            self.Merge_FileSeq_process.Seq_BAD = self.ui.radioButton_TAB5_FilesSequences_Bad_Seq.isChecked()
            self.Merge_FileSeq_process.Seq_GOOD = self.ui.radioButton_TAB5_FilesSequences_Good_Seq.isChecked()
            self.Merge_FileSeq_process.Seq_ALL = self.ui.radioButton_TAB5_FilesSequences_All_Seq.isChecked()
        self.Merge_FileSeq_process.start()  
        self.Merge_FileSeq_process.finished.connect(self.onFinished_Merge_FileSeq)  
    def onFinished_Merge_FileSeq(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_ReportsNIST_Path_to_Folder(self):
        self.ui.lineEdit_TAB5_NISTReports_Directory_Dialog.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:",options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_TAB5_NISTReports_Directory_Dialog.setText(str(folder_path))
    def btnClicked_ReportsNIST_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments/Merge/Reports_NIST/" + str(current_date) + '/experiment'
        self.Merge_ReportsNIST_process.path_to_reports = self.ui.lineEdit_TAB5_NISTReports_Directory_Dialog.text()
        self.Merge_ReportsNIST_process.path_for_distination = path_to_result
        self.Merge_ReportsNIST_process.report_name = self.ui.lineEdit_TAB5_NISTReports_Name_of_Report.text()
        self.Merge_ReportsNIST_process.save_in_common_folder = self.ui.checkBox_TAB5_NISTReports_Common.isChecked()
        self.Merge_ReportsNIST_process.start()  
        self.Merge_ReportsNIST_process.finished.connect(self.onFinished_Merge_ReportsNIST)  
    def onFinished_Merge_ReportsNIST(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_csv_1_Path_to_File(self):
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_1.clear()
        self.ui.lineEdit_TAB5_Folder_to_csvs.clear()
        if self.ui.checkBox_TAB5_Left_All.isChecked():
            self.ui.checkBox_TAB5_Left_All.setCheckState(False)
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.csv)",
                                       options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_1.setText(str(folder_path))
        self.ui.listWidget_TAB5_csv_Header_1.clear()
        df = pd.read_csv(folder_path,
                         sep=',',  
                         header=0,  
                         na_values=['', 'N/A'])  
        csv_columns = list(df.columns)
        for i in range(0, len(csv_columns)):
            item_csv = QtWidgets.QListWidgetItem();   item_csv.setText(csv_columns[i])
            item_csv.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv.setCheckState(QtCore.Qt.Unchecked);  self.ui.listWidget_TAB5_csv_Header_1.addItem(item_csv)
    def btnClicked_csv_2_Path_to_File(self):
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_2.clear()
        self.ui.lineEdit_TAB5_Folder_to_csvs.clear()
        if self.ui.checkBox_TAB5_Right_All.isChecked():
            self.ui.checkBox_TAB5_Right_All.setCheckState(False)
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.csv)",
                                       options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_2.setText(str(folder_path))
        self.ui.listWidget_TAB5_csv_Header_2.clear()
        df = pd.read_csv(folder_path,
                         sep=',',  
                         header=0,  
                         na_values=['', 'N/A'])  
        csv_columns = list(df.columns)
        for i in range(0, len(csv_columns)):
            item_csv = QtWidgets.QListWidgetItem(); item_csv.setText(csv_columns[i])
            item_csv.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv.setCheckState(QtCore.Qt.Unchecked);    self.ui.listWidget_TAB5_csv_Header_2.addItem(item_csv)
    def btnClicked_Merge_csv_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments/Merge/csv/" + str(current_date)
        self.Merge_csv_process.csv_path_1 = self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_1.text()
        self.Merge_csv_process.csv_path_2 = self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_2.text()
        self.Merge_csv_process.csv_output_path = path_to_result
        self.Merge_csv_process.csv_output_name = self.ui.lineEdit_TAB5_csv_Merge_Output_File_Name.text()
        self.Merge_csv_process.parameter_how = self.ui.lineEdit_TAB5_csv_Merge_param_how.text()
        self.Merge_csv_process.parameter_on = self.ui.lineEdit_TAB5_csv_Merge_param_on.text()
        self.Merge_csv_process.parameter_index = self.ui.lineEdit_TAB5_csv_Merge_param_index.text()
        self.Merge_csv_process.list_widget_csv_1 = self.ui.listWidget_TAB5_csv_Header_1
        self.Merge_csv_process.list_widget_csv_2 = self.ui.listWidget_TAB5_csv_Header_2
        self.Merge_csv_process.start()  
        self.Merge_csv_process.finished.connect(self.onFinished_Merge_csv)  
    def btnClicked_Merge_All_in_Folder(self):
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_1.clear()
        self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_2.clear()
        self.ui.listWidget_TAB5_csv_Header_1.clear()
        self.ui.listWidget_TAB5_csv_Header_2.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:",
                                                  options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_TAB5_Folder_to_csvs.setText(str(folder_path))
    def btnClicked_Concat(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments/Concat_csv/" + str(current_date)
        self.Concat_process.input_folder = self.ui.lineEdit_TAB5_Folder_to_csvs.text()
        self.Concat_process.output_folder = path_to_result
        self.Concat_process.output_name = self.ui.lineEdit_TAB5_csv_Merge_Output_File_Name.text()
        self.Concat_process.start()  
        self.Concat_process.finished.connect(self.onFinished_Merge_csv)  
    def onFinished_Merge_csv(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_Sort_csv_Start(self):
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments/Sort/" + str(current_date)
        create_dir(path_to_result)
        file_path_1 = self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_1.text()
        file_path_2 = self.ui.lineEdit_TAB5_Files_Dialog_csv_merge_2.text()
        sort_by_value = self.ui.lineEdit_TAB5_csv_Merge_param_on.text()
        file_result_1 = path_to_result + '/' + "sorted_" + os.path.basename(file_path_1)
        file_result_2 = path_to_result + '/' + "sorted_" + os.path.basename(file_path_2)
        if file_path_1 != "":
            data_csv_1 = pd.read_csv(file_path_1, sep=',')
            try:
                d_sort_1 = data_csv_1.sort_values([sort_by_value],
                                                  axis=0,  
                                                  ascending=[True])  
                d_sort_1.to_csv(file_result_1, index=False)
                print("\nСортировка файла с левого окна [ЗАВЕРШЕНА]")
            except Exception as ex:
                print("\nСортировка файла с левого окна [не выполнена]\nПроверьте исходные данные..\n", ex)
        if file_path_2 != "":
            data_csv_2 = pd.read_csv(file_path_2, sep=',')
            try:
                d_sort_2 = data_csv_2.sort_values([sort_by_value],
                                                  axis=0,  
                                                  ascending=[True])  
                d_sort_2.to_csv(file_result_2, index=False)
                print("\nСортировка файла с правого окна [ЗАВЕРШЕНА]")
            except Exception as ex:
                print("\nСортировка файла с правого окна [не выполнена]\nПроверьте исходные данные..\n", ex)
    def btnClicked_Calc_P_i_Path_to_Folder(self):
        self.ui.lineEdit_TAB5_Calculate_Pi_Directory_Dialog.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:",
                                                  options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_TAB5_Calculate_Pi_Directory_Dialog.setText(str(folder_path))
    def btnClicked_Calc_P_i_Start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        self.Calculate_P_i_process.path_to_reports = self.ui.lineEdit_TAB5_Calculate_Pi_Directory_Dialog.text()
        self.Calculate_P_i_process.path_to_csv_distination = self.ui.lineEdit_TAB5_Calculate_Pi_Directory_Dialog.text()
        self.Calculate_P_i_process.name_of_file_csv = self.ui.lineEdit_TAB5_Calculate_Pi_Output_File_Name.text()
        self.Calculate_P_i_process.start()  
        self.Calculate_P_i_process.finished.connect(self.onFinished_Calc_P_i)  
    def onFinished_Calc_P_i(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_Prime_Numbers_Gen(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments_2/PrimeNumbers/" + str(current_date)
        if not os.path.exists(path_to_result):
            create_dir(path_to_result)
        self.Prime_Number_Generate.start_value = self.ui.spinBox_Instruments_2_Prime_start.value()
        self.Prime_Number_Generate.stop_value = self.ui.spinBox_Instruments_2_Prime_stop.value()
        self.Prime_Number_Generate.path_to_result = path_to_result
        self.Prime_Number_Generate.file_name = self.ui.lineEdit_Instruments_2_Prime_filename.text()
        self.Prime_Number_Generate.start()  
        self.Prime_Number_Generate.finished.connect(self.onFinished_Prime_Numbers_Gen)  
    def onFinished_Prime_Numbers_Gen(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_Browse_BAD_qubits(self):
        self.ui.lineEdit_Instruments_2_Path_to_BAD_qubits.clear()
        dialog = QFileDialog(); dialog.setFileMode(dialog.Directory)
        folder_path = dialog.getExistingDirectory(self, "Выберите ПАПКУ:",
                                                  options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.ui.lineEdit_Instruments_2_Path_to_BAD_qubits.setText(str(folder_path))
    def chkBox_SHIFT_from_File(self):
        if self.ui.checkBox_Instruments_2_SHIFT_from_File.isChecked():
            self.ui.lineEdit_Instruments_2_SHIFT_from_File.setEnabled(True)
            self.ui.pushButton_Instruments_2_Browse_SHIFT_from_File.setEnabled(True)
        else:
            self.ui.lineEdit_Instruments_2_SHIFT_from_File.setEnabled(False)
            self.ui.pushButton_Instruments_2_Browse_SHIFT_from_File.setEnabled(False)
            self.ui.lineEdit_Instruments_2_SHIFT_from_File.clear()
    def btnClicked_Browse_SHIFT_from_File(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.[tT][xX][tT])",
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_Instruments_2_SHIFT_from_File.clear()
        self.ui.lineEdit_Instruments_2_SHIFT_from_File.setText(str(folder_path))
    def btnClicked_KEY_Alignment(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Instruments_2/Alignment/" + str(current_date)
        if not os.path.exists(path_to_result):
            create_dir(path_to_result)
        self.Key_Alignment.path_to_qubits = self.ui.lineEdit_Instruments_2_Path_to_BAD_qubits.text()
        self.Key_Alignment.dir_output = path_to_result
        self.Key_Alignment.RNG_from_file = self.ui.checkBox_Instruments_2_SHIFT_from_File.isChecked()
        self.Key_Alignment.file_with_RNG_numbers = self.ui.lineEdit_Instruments_2_SHIFT_from_File.text()
        self.Key_Alignment.start()  
        self.Key_Alignment.finished.connect(self.onFinished_Prime_Numbers_Gen)  
    def onFinished_KEY_Alignment(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_Logit_Path_to_File(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.csv)",
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB6_Path_to_csvFile.clear()
        self.ui.lineEdit_TAB6_Path_to_csvFile.setText(str(folder_path))
        self.ui.listWidget_TAB6_csvHeaders.clear()
        self.ui.listWidget_TAB6_csvHeaders_Argument.clear()
        df = pd.read_csv(folder_path,
                         sep=',',  
                         header=0,  
                         na_values=['', 'N/A'])  
        csv_columns = list(df.columns)
        for i in range(0, len(csv_columns)):
            item_csv_1 = QtWidgets.QListWidgetItem(); item_csv_1.setText(csv_columns[i])
            item_csv_1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv_1.setCheckState(QtCore.Qt.Unchecked);  self.ui.listWidget_TAB6_csvHeaders.addItem(item_csv_1)
            item_csv_2 = QtWidgets.QListWidgetItem();   item_csv_2.setText(csv_columns[i])
            item_csv_2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv_2.setCheckState(QtCore.Qt.Unchecked);  self.ui.listWidget_TAB6_csvHeaders_Argument.addItem(item_csv_2)
        pd.set_option('display.max_columns', None)
        print(df.describe())
        pd.reset_option('display.max_columns')
    def btnClicked_Path_to_Model(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getOpenFileName(self, "Выберите ФАЙЛ:", "/home", "Text Files (*.pickle)",
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        self.ui.lineEdit_TAB6_Path_to_model.clear()
        self.ui.lineEdit_TAB6_Path_to_model.setText(str(folder_path))
    def chkBox_Logit_Select_All_Headers(self):
        if self.ui.checkBox_TAB6_Select_all_Factors.isChecked():
            try:
                for index in range(self.ui.listWidget_TAB6_csvHeaders.count()):
                    if self.ui.listWidget_TAB6_csvHeaders.item(index).checkState() == Qt.Unchecked:
                        self.ui.listWidget_TAB6_csvHeaders.item(index).setCheckState(QtCore.Qt.Checked)
            except: print("Не сработало...")
        else:
            try:
                for index in range(self.ui.listWidget_TAB6_csvHeaders.count()):
                    if self.ui.listWidget_TAB6_csvHeaders.item(index).checkState() == Qt.Checked:
                        self.ui.listWidget_TAB6_csvHeaders.item(index).setCheckState(QtCore.Qt.Unchecked)
            except: print("Не сработало...")
    def btnClicked_Logit_Interrelation(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/Interrelation/" + str(current_date)
        self.Interrelation_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        self.Interrelation_process.path_for_result = path_to_result
        self.Interrelation_process.name_of_file = self.ui.lineEdit_TAB6_Interrelation_name_output.text()
        self.Interrelation_process.list_widget_csv = self.ui.listWidget_TAB6_csvHeaders
        self.Interrelation_process.start()  
        self.Interrelation_process.finished.connect(self.onFinished_Factors)  
    def btnClicked_Logit_Corr_VIF(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/"
        self.Corr_VIF_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        self.Corr_VIF_process.path_for_result = path_to_result
        self.Corr_VIF_process.name_of_file_corr = self.ui.lineEdit_TAB6_Corrcoef_name_output.text()
        self.Corr_VIF_process.name_of_file_vif = self.ui.lineEdit_TAB6_VIF_name_output.text()
        self.Corr_VIF_process.duplicate = self.ui.checkBox_TAB6_factors_to_input_csv.isChecked()
        self.Corr_VIF_process.list_widget_csv = self.ui.listWidget_TAB6_csvHeaders
        self.Corr_VIF_process.start()  
        self.Corr_VIF_process.finished.connect(self.onFinished_Factors)  
    def btnClicked_Factors_Significance(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)  
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        self.Factors_Significance_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()       
        self.Factors_Significance_process.list_widget_csv_arg = self.ui.listWidget_TAB6_csvHeaders_Argument 
        self.Factors_Significance_process.list_widget_csv_fac = self.ui.listWidget_TAB6_csvHeaders          
        cnt_spin_Box = self.ui.spinBox_TAB6_factors_significance.value()        
        cnt_factors = 0                                                         
        for index in range(self.ui.listWidget_TAB6_csvHeaders.count()):
            if self.ui.listWidget_TAB6_csvHeaders.item(index).checkState() == Qt.Checked:
                cnt_factors += 1
        if cnt_factors == 0:
            print("\nВыберите факторы!\n")
            self.onFinished_Factors()
        elif cnt_spin_Box > cnt_factors:
            print("\nКоличество выбранных факторов должно быть меньше ожидаемых!\n(Проверь spinBox)\n")
            self.onFinished_Factors()
        elif (cnt_spin_Box != 0) & (cnt_spin_Box <= cnt_factors):
            self.Factors_Significance_process.features_to_select = cnt_spin_Box
            self.Factors_Significance_process.start()  
            self.Factors_Significance_process.finished.connect(self.onFinished_Argument)  
        else:
            print("\nЧто-то делаешь не так...\n")
            self.onFinished_Factors()
    def onFinished_Factors(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
    def btnClicked_Logit_Count_of_Argument(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/cntArgument/" + str(current_date)
        self.Count_of_Argument_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        self.Count_of_Argument_process.path_for_result = path_to_result
        self.Count_of_Argument_process.name_of_file = self.ui.lineEdit_TAB6_cnt_Argument_name_output.text()
        self.Count_of_Argument_process.list_widget_csv = self.ui.listWidget_TAB6_csvHeaders_Argument
        self.Count_of_Argument_process.start()  
        self.Count_of_Argument_process.finished.connect(self.onFinished_Argument)  
    def btnClicked_Logit_Binomial_Modeling(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)              
        self.ui.tab_INIT_IDLE_H.setEnabled(False)       
        self.ui.tab_QRNG.setEnabled(False)              
        self.ui.tab_QKD.setEnabled(False)               
        self.ui.tab_Fourie.setEnabled(False)            
        self.ui.tab_Instruments.setEnabled(False)       
        self.ui.tab_Instruments_2.setEnabled(False)     
        self.ui.tab_Modeling.setEnabled(False)          
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/_MODELS_/LogitModel/" + str(current_date)
        self.Binomial_Modeling_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        self.Binomial_Modeling_process.path_for_result = path_to_result
        self.Binomial_Modeling_process.name_of_file = self.ui.lineEdit_TAB6_BinModel_name_output.text()
        self.Binomial_Modeling_process.MLE_or_IRLS = self.ui.radioButton_TAB6_IRLS.isChecked()
        self.Binomial_Modeling_process.list_widget_csv_arg = self.ui.listWidget_TAB6_csvHeaders_Argument
        self.Binomial_Modeling_process.list_widget_csv_fac = self.ui.listWidget_TAB6_csvHeaders
        self.Binomial_Modeling_process.start()  
        self.Binomial_Modeling_process.finished.connect(self.onFinished_Argument)  
    def btnClicked_Linear_Modeling_Gen_Formula(self):
        path_to_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        Intercept = self.ui.checkBox_TAB6_LinModel_Intercept.isChecked()
        try:
            argument = []
            for index in range(self.ui.listWidget_TAB6_csvHeaders_Argument.count()):
                if self.ui.listWidget_TAB6_csvHeaders_Argument.item(index).checkState() == Qt.Checked:
                    argument.append(self.ui.listWidget_TAB6_csvHeaders_Argument.item(index).text())  
            if len(argument) == 1:
                factors = []
                for index in range(self.ui.listWidget_TAB6_csvHeaders.count()):
                    if self.ui.listWidget_TAB6_csvHeaders.item(index).checkState() == Qt.Checked:
                        factors.append(self.ui.listWidget_TAB6_csvHeaders.item(index).text())  
                if len(factors) != 0:
                    df = pd.read_csv(path_to_csv, sep=',')
                    df.columns = df.columns.str.replace(' ', '_')
                    df.columns = df.columns.str.replace('(', '')
                    df.columns = df.columns.str.replace(')', '')
                    df.columns = df.columns.str.replace(chr(8730), '')
                    formula = argument[0] + ' ~ '
                    formula_for_user = argument[0] + ' = '
                    for i in range(0, len(factors)):
                        factors[i] = factors[i].replace(' ', '_')
                        factors[i] = factors[i].replace('(', '')
                        factors[i] = factors[i].replace(')', '')
                        factors[i] = factors[i].replace(chr(8730), '')
                        formula += factors[i] + ' + '
                        formula_for_user += 'a' + str(i + 1) + '*' + factors[i] + ' + '
                    formula = formula[:-3]  
                    formula_for_user += 'Intercept'
                    if not Intercept:
                        formula += ' - 1'
                        formula_for_user = formula_for_user.replace(' + Intercept', '')
                    print(f'\nИтоговая формула для моделирования: {formula_for_user}\n\n')
                    self.ui.lineEdit_TAB6_LinModel_Formula.setText(formula)
                else:
                    print("Выберите не менее одного фактора.")
            else:
                print("Выберите 1 аргумент.")
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
    def btnClicked_Lineal_Regression_Modeling(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)          
        self.ui.tab_INIT_IDLE_H.setEnabled(False)   
        self.ui.tab_QRNG.setEnabled(False)          
        self.ui.tab_QKD.setEnabled(False)           
        self.ui.tab_Fourie.setEnabled(False)        
        self.ui.tab_Instruments.setEnabled(False)   
        self.ui.tab_Instruments_2.setEnabled(False) 
        self.ui.tab_Modeling.setEnabled(False)      
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/_MODELS_/LinRegModel/" + str(current_date)
        self.LinReg_Modeling_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()
        self.LinReg_Modeling_process.path_for_result = path_to_result
        self.LinReg_Modeling_process.name_of_file = self.ui.lineEdit_TAB6_LinModel_name_output.text()
        self.LinReg_Modeling_process.Intercept = self.ui.checkBox_TAB6_LinModel_Intercept.isChecked()
        self.LinReg_Modeling_process.formula = self.ui.lineEdit_TAB6_LinModel_Formula.text()
        self.LinReg_Modeling_process.list_widget_csv_arg = self.ui.listWidget_TAB6_csvHeaders_Argument
        self.LinReg_Modeling_process.list_widget_csv_fac = self.ui.listWidget_TAB6_csvHeaders
        self.LinReg_Modeling_process.type_of_argument = self.ui.radioButton_Argument_INT.isChecked()    
        self.LinReg_Modeling_process.start()  
        self.LinReg_Modeling_process.finished.connect(self.onFinished_Argument)  
    def btnPredict(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ui.tab_INFO.setEnabled(False)                  
        self.ui.tab_INIT_IDLE_H.setEnabled(False)           
        self.ui.tab_QRNG.setEnabled(False)                  
        self.ui.tab_QKD.setEnabled(False)                   
        self.ui.tab_Fourie.setEnabled(False)                
        self.ui.tab_Instruments.setEnabled(False)           
        self.ui.tab_Instruments_2.setEnabled(False)         
        self.ui.tab_Modeling.setEnabled(False)              
        current_date = date.today()
        path_to_result = os.path.expanduser("~") + "/Documents/QISs/Modeling/Predicted/" + str(current_date)
        self.Predict_process.path_for_result = path_to_result                               
        self.Predict_process.path_for_model = self.ui.lineEdit_TAB6_Path_to_model.text()    
        self.Predict_process.path_for_csv = self.ui.lineEdit_TAB6_Path_to_csvFile.text()    
        self.Predict_process.name_of_file = self.ui.lineEdit_TAB6_Predict_name_output.text()    
        self.Predict_process.list_widget_csv_arg = self.ui.listWidget_TAB6_csvHeaders_Argument  
        self.Predict_process.list_widget_csv_fac = self.ui.listWidget_TAB6_csvHeaders           
        self.Predict_process.type_of_argument = self.ui.radioButton_Argument_INT.isChecked()  
        self.Predict_process.start()        
        self.Predict_process.finished.connect(self.onFinished_Argument)     
    def onFinished_Argument(self):
        QApplication.restoreOverrideCursor()        
        self.ui.tab_INFO.setEnabled(True)           
        self.ui.tab_INIT_IDLE_H.setEnabled(True)    
        self.ui.tab_QRNG.setEnabled(True)           
        self.ui.tab_QKD.setEnabled(True)            
        self.ui.tab_Fourie.setEnabled(True)         
        self.ui.tab_Instruments.setEnabled(True)    
        self.ui.tab_Instruments_2.setEnabled(True)  
        self.ui.tab_Modeling.setEnabled(True)       
def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()