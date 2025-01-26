from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from src.TAB_0.QPU_Info import set_Num_of_Qubits

class QPUChangedComboBoxTAB2(QThread):

    def __init__(self, parent=None):
        super(QPUChangedComboBoxTAB2, self).__init__(parent)

        self.value = 0

        self.token_name = ""            
        self.ibm_channel = ""           
        self.ibm_instance = ""          
        self.backend_name = ""          

        self.slider_QRNG_2_1 = None       
        self.slider_QRNG_2_2 = None       
        self.slider_QRNG_2_3 = None       

        self.list_widget_2_1 = None       
        self.list_widget_2_2 = None       
        self.list_widget_2_3 = None       

        self.spinBox_max_shots = None     

    def run(self):
        try:
            max_qubit, max_shots = set_Num_of_Qubits(self.token_name, self.ibm_channel, self.backend_name, self.ibm_instance)

            self.list_widget_2_1.clear()
            for i in range(0, max_qubit):
                item_2_1 = QtWidgets.QListWidgetItem(); item_2_1.setText(f'Кубит {i}'); item_2_1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_2_1.setCheckState(QtCore.Qt.Unchecked)  
                self.list_widget_2_1.addItem(item_2_1)
                item_2_2 = QtWidgets.QListWidgetItem(); item_2_2.setText(f'Кубит {i}'); item_2_2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_2_2.setCheckState(QtCore.Qt.Unchecked)  
                self.list_widget_2_2.addItem(item_2_2)
                item_2_3 = QtWidgets.QListWidgetItem(); item_2_3.setText(f'Кубит {i}'); item_2_3.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled); item_2_3.setCheckState(QtCore.Qt.Unchecked)  
                self.list_widget_2_3.addItem(item_2_3)

            self.slider_QRNG_2_1.setMaximum(max_qubit); self.slider_QRNG_2_1.setMinimum(1)  
            self.slider_QRNG_2_2.setMaximum(max_qubit); self.slider_QRNG_2_2.setMinimum(1)  
            self.slider_QRNG_2_3.setMaximum(max_qubit); self.slider_QRNG_2_3.setMinimum(1)  

            self.spinBox_max_shots.clear()                  
            self.spinBox_max_shots.setMaximum(max_shots)    
        except Exception as ex:
            print("Возникла ошибка: \n", ex); print("\n--------------- ОШИБКА --------------"); print("-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

class SliderTAB2Changed(QThread):

    def __init__(self, parent=None):
        super(SliderTAB2Changed, self).__init__(parent)

        self.value = 0

        self.list_widget_2_x = None         
        self.current_value = 0              

    def run(self):
        try:

            for i in range(0, self.current_value):
                if self.list_widget_2_x.item(i).checkState() == Qt.Unchecked:
                    self.list_widget_2_x.item(i).setCheckState(QtCore.Qt.Checked)
        except: print("Что-то пошло не так...")