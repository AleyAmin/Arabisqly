import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Window,Button
from Connect_Database import *

cursor, conn = connect_to_database(DRIVER, SERVER, DATABASE)

class LoginPage:
    def __init__(self):
        self.id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.content = tk.Frame(main_window)
        self.Job = None
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tk.Label(self.content, text="Id:")
        self.id_label.pack(pady=5)
        self.id_entry = tk.Entry(self.content, textvariable=self.id_var)
        self.id_entry.pack(pady=5)

        self.password_label = tk.Label(self.content, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.content, textvariable=self.password_var, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.content, text="Login", command=self.login)
        self.login_button.pack(pady=5)
        self.login_button.bind('<KeyPress-Return>',lambda event:self.login())
    def login(self):
        id = self.id_var.get()
        password = self.password_entry.get()
        
        try:
            cursor.execute("EXEC Login_func ?, ?", (id, password))
            row = cursor.fetchall()
            if len(row) == 1:
                self.Job = row[0][1]
                self.hide_frame()
                main_window_label.pack_forget()
                if self.Job == 'Manager':
                    manager_page = ManagerPage()
                    manager_page.show_frame()
                elif self.Job == 'Supervisor':
                    supervisor_page = SupervisorPage()
                    supervisor_page.show_frame()

            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                self.id_entry.delete(0,'end')
                self.password_entry.delete(0,'end')

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_frame(self):
        self.content.pack(fill="both", expand=True)

    def hide_frame(self):
        self.content.pack_forget()

class ManagerPage:
    def __init__(self):
        self.no_of_Emps = tk.StringVar()
        self.no_of_Orders = tk.StringVar()
        self.deleteobj = None
        self.managerId = login_page.id_var.get()
        self.content = tk.Frame(main_window)
        self.createWidgets()
    def createWidgets(self):
        self.frame_buttons = tk.Frame(self.content)
        self.frame_buttons.pack(side='bottom',expand=True,fill='both')

        self.frame_employeestable = tk.Frame(self.content)
        self.frame_employeestable.pack(side='bottom',expand=True,fill='both')

        self.frame_noofoorders = tk.Frame(self.content)
        self.frame_noofoorders.pack(side='left',expand=True,fill='both')

        self.frame_noofemps = tk.Frame(self.content)
        self.frame_noofemps.pack(side='left',expand=True,fill='both')

        self.no_of_Emps = self.getNoofEmps()
        self.label_noofemps = tk.Label(self.frame_noofemps,text=f'No Of Employees:\n {self.no_of_Emps}',justify="center",font=("Arial ", 18))
        self.label_noofemps.pack(expand=True,pady=15)

        self.no_of_Orders = self.getNoofOrders()
        self.label_noofoorders = tk.Label(self.frame_noofoorders,text=f'No Of Orders:\n{self.no_of_Orders}',justify="center",font=("Arial ", 18))
        self.label_noofoorders.pack(expand=True,pady=15)

        employees = self.getEmps()
        self.emp_Table = ttk.Treeview(self.frame_employeestable, columns=('Name', 'Id','sex','Job'),show='headings')
        self.emp_Table.heading('Name', text='Name')
        self.emp_Table.heading('Id', text='Id')
        self.emp_Table.heading('sex', text='Sex')
        self.emp_Table.heading('Job', text='Job')

        for emp in employees:
             self.emp_Table.insert(parent='',index=tk.END,values=emp)

        self.emp_Table.bind('<<TreeviewSelect>>', self.item_select)
        self.emp_Table.bind('<Delete>', self.delete_item)

        self.emp_Table.pack(expand=True)

        self.insertEmp = Button(self.frame_buttons,text = "Add Employee" , bootstyle = 'primary')
        self.insertEmp.pack(side='left',expand=True)
        self.editEmp = Button(self.frame_buttons,text = "Edit Employee" , bootstyle = 'warning')
        self.editEmp.pack(side='left',expand=True)
        self.deleteEmp = Button(self.frame_buttons,text = "Delete Employee" , bootstyle = 'danger' , command= self.deleteEmpbyid)
        self.deleteEmp.pack(side='left',expand=True)

    def refresh(self):
        self.emp_Table.pack_forget()
        self.label_noofemps.pack_forget()
        employees = self.getEmps()
        self.no_of_Emps = self.getNoofEmps()
        self.label_noofemps = tk.Label(self.frame_noofemps,text=f'No Of Employees:\n {self.no_of_Emps}',justify="center",font=("Arial ", 18))
        self.label_noofemps.pack(expand=True,pady=15)
        self.emp_Table = ttk.Treeview(self.frame_employeestable, columns=('Name', 'Id','sex','Job'),show='headings')
        self.emp_Table.heading('Name', text='Name')
        self.emp_Table.heading('Id', text='Id')
        self.emp_Table.heading('sex', text='Sex')
        self.emp_Table.heading('Job', text='Job')

        for emp in employees:
             self.emp_Table.insert(parent='',index=tk.END,values=emp)

        self.emp_Table.bind('<<TreeviewSelect>>', self.item_select)
        self.emp_Table.bind('<Delete>', self.delete_item)

        self.emp_Table.pack(expand=True)


    def item_select(self,_):
        self.deleteobj = self.emp_Table.item(self.emp_Table.selection())['values']
        print(self.deleteobj[1])

    def delete_item(self,_):
        self.emp_Table.item(self.emp_Table.selection())
        
    def deleteEmpbyid(self):
        id = self.deleteobj[1]
        print(id)
        cursor.execute("exec RemoveEmployeeById ?", (id,))
        cursor.commit()
        self.refresh()
        
        
    def getNoofEmps(self):
        cursor.execute("exec View_Branch_NoOfEmployee ?", (self.managerId,))
        res = cursor.fetchall()
        return str(res[0][0])
    
    def getNoofOrders(self):
        cursor.execute("exec View_Branch_NoOrders ?", (self.managerId,))
        res = cursor.fetchall()
        return str(res[0][0])
    
    def getEmps(self):
        cursor.execute("exec View_Branch_Employee ?", (self.managerId,))
        emps = cursor.fetchall()
        return emps
    
    def show_frame(self):
        self.content.pack(expand=True,fill='both')
    def hide_frame(self):
        self.content.pack_forget()

class SupervisorPage:
    def __init__(self):
        self.no_of_Emps = tk.StringVar()
        self.no_of_Orders = tk.StringVar()
        self.deleteobj = None
        self.supervisorId = login_page.id_var.get()
        self.content = tk.Frame(main_window)
        self.createWidgets()
    def createWidgets(self):
        self.frame_buttons = tk.Frame(self.content)
        self.frame_buttons.pack(side='bottom',expand=True,fill='both')

        self.frame_employeestable = tk.Frame(self.content)
        self.frame_employeestable.pack(side='bottom',expand=True,fill='both')

        self.frame_noofemps = tk.Frame(self.content)
        self.frame_noofemps.pack(side='top',expand=True,fill='both')

        self.no_of_Emps = self.getNoofEmps()
        self.label_noofemps = tk.Label(self.frame_noofemps,text=f'No Of Employees:\n {self.no_of_Emps}',justify="center",font=("Arial ", 18))
        self.label_noofemps.pack(expand=True,pady=15)

        employees = self.getEmps()
        self.emp_Table = ttk.Treeview(self.frame_employeestable, columns=('Name', 'Id','sex','Job'),show='headings')
        self.emp_Table.heading('Name', text='Name')
        self.emp_Table.heading('Id', text='Id')
        self.emp_Table.heading('sex', text='Sex')
        self.emp_Table.heading('Job', text='Job')

        for emp in employees:
             self.emp_Table.insert(parent='',index=tk.END,values=emp)

        self.emp_Table.pack(expand=True)

        self.insertEmp = Button(self.frame_buttons,text = "Add Employee" , bootstyle = 'primary')
        self.insertEmp.pack(side='left',expand=True)
        self.editEmp = Button(self.frame_buttons,text = "Edit Employee" , bootstyle = 'warning')
        self.editEmp.pack(side='left',expand=True)
        self.deleteEmp = Button(self.frame_buttons,text = "Delete Employee" , bootstyle = 'danger',  command= self.deleteEmpbyid)
        self.deleteEmp.pack(side='left',expand=True)

        self.emp_Table.bind('<<TreeviewSelect>>', self.item_select)
        self.emp_Table.bind('<Delete>', self.delete_item)

        self.emp_Table.pack(expand=True)

    def refresh(self):
        self.emp_Table.pack_forget()
        self.label_noofemps.pack_forget()
        employees = self.getEmps()
        self.no_of_Emps = self.getNoofEmps()
        self.label_noofemps = tk.Label(self.frame_noofemps,text=f'No Of Employees:\n {self.no_of_Emps}',justify="center",font=("Arial ", 18))
        self.label_noofemps.pack(expand=True,pady=15)
        self.emp_Table = ttk.Treeview(self.frame_employeestable, columns=('Name', 'Id','sex','Job'),show='headings')
        self.emp_Table.heading('Name', text='Name')
        self.emp_Table.heading('Id', text='Id')
        self.emp_Table.heading('sex', text='Sex')
        self.emp_Table.heading('Job', text='Job')

        for emp in employees:
             self.emp_Table.insert(parent='',index=tk.END,values=emp)

        self.emp_Table.bind('<<TreeviewSelect>>', self.item_select)
        self.emp_Table.bind('<Delete>', self.delete_item)

        self.emp_Table.pack(expand=True)


    def item_select(self,_):
        self.deleteobj = self.emp_Table.item(self.emp_Table.selection())['values']
        print(self.deleteobj[1])

    def delete_item(self,_):
        self.emp_Table.item(self.emp_Table.selection())
        
    def deleteEmpbyid(self):
        id = self.deleteobj[1]
        print(id)
        cursor.execute("exec RemoveEmployeeById ?", (id,))
        cursor.commit()
        self.refresh()

    def getNoofEmps(self):
        cursor.execute("exec view_NoOfEmployees ?", (self.supervisorId,))
        res = cursor.fetchall()
        return str(res[0][0])
    
    def getEmps(self):
        cursor.execute("exec view_employees ?", (self.supervisorId,))
        emps = cursor.fetchall()
        return emps
    
    def show_frame(self):
        self.content.pack(expand=True,fill='both')
    def hide_frame(self):
        self.content.pack_forget()

def display():
    main_window_button.pack_forget()
    login_page.show_frame()

main_window = Window(themename='darkly')
main_window.geometry("800x600")
main_window.title("Arabisqly")
main_window_label = tk.Label(main_window,text="Welcome to Arabisq",font=("courier new bold", 42))
main_window_label.pack(expand=True,fill="both")
main_window_button = tk.Button(main_window,text="Start",height=2,width=10,command= display)
main_window_button.pack(expand=True)
login_page = LoginPage()

main_window.mainloop()

