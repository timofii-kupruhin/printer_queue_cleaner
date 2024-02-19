import os
import shutil
import win32print
import subprocess as sub

class Worker:
    def clear(self):
        sub.call("clear", shell=True)

    def get_printers(self):
        printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)]
        default_printer = win32print.GetDefaultPrinter()

        return default_printer, printers

    def quit_or_restart(self):
        user_input = input("\nЗАКРЫТЬ ПРОГРАММУ ИЛИ ЗАПУСТИТЬ СНОВА (y - запустить снова, q - выход): ")
        if user_input.lower() in ["y", '',]:
            self.clear()
            return self.run()
        elif user_input.lower() in ["q"]: 
            exit()
        else:
            return self.quit_or_restart()

    def get_user_input(self ):
        self.clear()
        default_printer, printers = self.get_printers()
        printer_name = ""
        print(f'\n{"-" * 10} ВВЕДИТЕ НАЗВАНИЕ ПРИНТЕРА ЛИБО НАЖМИТЕ ENTER {"-" * 10}', end="\n")

        for printer in printers:
            print(f"Название устройства: {printer}")

        print(f"\nПринтер за умолчанием: {default_printer}")
        user_input = input("\nПРИ НАЖАТИИ ENTER БУДЕТ ВЫБРАН СТАНДАРТНЫЙ ПРИНТЕР: ")

        if user_input in printers:
            printer_name = user_input
        elif user_input == "":
            printer_name = default_printer
        else:
            print("\n!!! ПРИНТЕР БЫЛ ВЫБРАН НЕ КОРРЕКТНО !!!\nПРОСМОТРИТЕ СПИСОК ДОСТУПНЫХ УСТРОЙСТВ\n")
            self.quit_or_restart()
        
        self.clear()       
        return printer_name

   
    def clean_printer_queue(self):
        PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}  

        printer_name = self.get_user_input()
        try: 
            printer_handle = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
            win32print.SetPrinter(printer_handle, 0, None, win32print.PRINTER_CONTROL_PURGE)
            win32print.ClosePrinter(printer_handle)
        
        except Exception as e:
            print("!!! ВОЗНИКЛА ОШИБКА !!!")
            print(e)
            print("!!! ВОЗНИКЛА ОШИБКА !!!")
            self.quit_or_restart()

        else:
            print(f"\n {'-'*10} ОЧЕРЕДЬ ДЛЯ ПРИНТЕРА {printer_name} БЫЛА ОЧИЩЕНА {'-'*10}")
            self.quit_or_restart()

    def run (self, ):
        self.clean_printer_queue()


if __name__ == "__main__":
    main = Worker()
    main.run()