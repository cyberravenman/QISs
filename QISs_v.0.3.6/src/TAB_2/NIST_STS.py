from PyQt5.QtCore import QThread
import subprocess

class NISTLaunch(QThread):

    def __init__(self, parent=None):
        super(NISTLaunch, self).__init__(parent)

        self.value = 0

        self.args = []                                  
        self.bash_command = "./NIST/auto_test_v.3.1.sh" 

    def run(self):
        print("-----ПРОВЕРКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ ТЕСТАМИ NIST STS-----\n")

        try:
            calculate_NIST_STS(self.bash_command, self.args)
        except Exception as ex:
            print("Возникло непредвиденное исключение. Перепроверьте исходные данные.\n", ex)
        print("\n-----ВЫПОЛНЕНИЕ ЗАДАЧИ ЗАВЕРШЕНО-----\n")

def calculate_NIST_STS(bash_command, bash_arguments):
    result = subprocess.run([bash_command] + bash_arguments, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)