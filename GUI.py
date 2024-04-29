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

        self.login_button = tk.Button(self.content, text="Login",height=2,width=10, command=self.login)
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
                    employee_page = EmployeePage()
                    employee_page.show_frame()

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
        self.var1 = tk.StringVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()
        self.var7 = tk.StringVar()
        self.var8 = tk.StringVar()
        self.var9 = tk.StringVar()
        self.var10 = tk.StringVar()
        self.var11 = tk.StringVar()
        self.deleteobj = None
        self.updEmp = None
        self.managerId = login_page.id_var.get()
        self.content = tk.Frame(main_window)
        self.createWidgets()
        
    def createWidgets(self):
        self.form_frame = tk.Frame(self.content)

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

        self.emp_Table.pack(fill='both',expand=True)

        self.insertEmp = Button(self.frame_buttons,text = "Add Employee" , bootstyle = 'primary', command = lambda : self.formpage("Add"))
        self.insertEmp.pack(side='left',expand=True)
        self.editEmp = Button(self.frame_buttons,text = "Edit Employee" , bootstyle = 'warning', command=self.getEmpbyid)
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

    def hide_formpage(self):
        self.form_frame.pack_forget()

    def formpage(self,page):
        self.frame_buttons.pack_forget()
        self.frame_employeestable.pack_forget()
        self.frame_noofoorders.pack_forget()
        self.frame_noofemps.pack_forget()
        self.form_frame.pack()

        self.frame1 = tk.Frame(self.form_frame)
        self.frame1.pack(side='top',expand=True,fill='both')

        self.frame2 = tk.Frame(self.form_frame)
        self.frame2.pack(side='top',expand=True,fill='both')

        self.frame3 = tk.Frame(self.form_frame)
        self.frame3.pack(side='top',expand=True,fill='both')

        self.frame4 = tk.Frame(self.form_frame)
        self.frame4.pack(side='top',expand=True,fill='both')

        self.frame5 = tk.Frame(self.form_frame)
        self.frame5.pack(side='top',expand=True,fill='both')

        self.frame6 = tk.Frame(self.form_frame)
        self.frame6.pack(side='top',expand=True,fill='both')

        self.frame7 = tk.Frame(self.form_frame)
        self.frame7.pack(side='top',expand=True,fill='both')

        self.frame8 = tk.Frame(self.form_frame)
        self.frame8.pack(side='top',expand=True,fill='both')

        self.frame9 = tk.Frame(self.form_frame)
        self.frame9.pack(side='top',expand=True,fill='both')
        
        self.frame10 = tk.Frame(self.form_frame)
        self.frame10.pack(side='top',expand=True,fill='both')

        self.frame11 = tk.Frame(self.form_frame)
        self.frame11.pack(side='top',expand=True,fill='both')

        self.frame12 = tk.Frame(self.form_frame)
        self.frame12.pack(side='top',expand=True,fill='both')

        self.label1 = tk.Label(self.frame1, text="SSN:")
        self.label1.pack(side='left',pady=5)
        self.entry1 = tk.Entry(self.frame1, textvariable=self.var1)
        self.entry1.pack(pady=5)

        self.label2 = tk.Label(self.frame2, text="Id:")
        self.label2.pack(side='left',pady=5)
        self.entry2 = tk.Entry(self.frame2, textvariable=self.var2,state='disabled')
        self.entry2.pack(pady=5)

        self.label3 = tk.Label(self.frame3, text="Password:")
        self.label3.pack(side='left',pady=5)
        self.entry3 = tk.Entry(self.frame3, textvariable=self.var3)
        self.entry3.pack(pady=5)

        self.label4 = tk.Label(self.frame4, text="Name:")
        self.label4.pack(side='left',pady=5)
        self.entry4 = tk.Entry(self.frame4, textvariable=self.var4)
        self.entry4.pack(pady=5)
        
        self.label5 = tk.Label(self.frame5, text="Sex:")
        self.label5.pack(side='left',pady=5)
        self.entry5 = tk.Entry(self.frame5, textvariable=self.var5)
        self.entry5.pack(pady=5)

        self.label6 = tk.Label(self.frame6, text="Salary:")
        self.label6.pack(side='left',pady=5)
        self.entry6 = tk.Entry(self.frame6, textvariable=self.var6)
        self.entry6.pack(pady=5)

        self.label7 = tk.Label(self.frame7, text="Birth Date:")
        self.label7.pack(side='left',pady=5)
        self.entry7 = tk.Entry(self.frame7, textvariable=self.var7)
        self.entry7.pack(pady=5)

        self.label8 = tk.Label(self.frame8, text="Address:")
        self.label8.pack(side='left',pady=5)
        self.entry8 = tk.Entry(self.frame8, textvariable=self.var8)
        self.entry8.pack(pady=5)

        self.label9 = tk.Label(self.frame9, text="SuperSSN:")
        self.label9.pack(side='left',pady=5)
        self.entry9 = tk.Entry(self.frame9, textvariable=self.var9)
        self.entry9.pack(pady=5)

        self.label10 = tk.Label(self.frame10, text="Branch:")
        self.label10.pack(side='left',pady=5)
        self.entry10 = tk.Entry(self.frame10, textvariable=self.var10)
        self.entry10.pack(pady=5)

        self.label11 = tk.Label(self.frame11, text="Job:")
        self.label11.pack(side='left',pady=5)
        self.entry11 = tk.Entry(self.frame11, textvariable=self.var11)
        self.entry11.pack(pady=5)

        if page == "update":
            self.save_button = tk.Button(self.frame12, text="Save", command=self.updateEmployee)
            self.save_button.pack(pady=10)
        elif page == "Add":
            self.save_button = tk.Button(self.frame12, text="Save", command=self.addEmployee)
            self.save_button.pack(pady=10)
   
    def updateEmployee(self):
        SSN = self.var1.get()
        emp_id = self.var2.get()
        password = self.var3.get()
        name = self.var4.get()
        sex = self.var5.get()
        salary = self.var6.get()
        birth_date = self.var7.get()
        address = self.var8.get()
        super_ssn = self.var9.get()
        branch = self.var10.get()
        job = self.var11.get()
        cursor.execute("exec update_Employee ?,?,?,?,?,?,?,?,?,?,?",(emp_id,SSN,password,name,sex,salary,birth_date,address,super_ssn,branch,job))
        cursor.commit()
        self.hide_formpage()
        self.createWidgets()
        
    def addEmployee(self):
        SSN = self.var1.get()
        password = self.var3.get()
        name = self.var4.get()
        sex = self.var5.get()
        salary = self.var6.get()
        birth_date = self.var7.get()
        address = self.var8.get()
        super_ssn = self.var9.get()
        branch = self.var10.get()
        job = self.var11.get()
        cursor.execute("exec AddEmployee ?,?,?,?,?,?,?,?,?,?",(SSN,password,name,sex,salary,birth_date,address,super_ssn,branch,job))
        cursor.commit()
        self.hide_formpage()
        self.createWidgets()

    def getEmpbyid(self):
        id = self.deleteobj[1]
        cursor.execute('exec ViewAll_Employee_Info ?',(id,))
        self.updEmp = cursor.fetchall()
        self.formpage("update")
        self.var1.set(self.updEmp[0][0])
        self.var2.set(self.updEmp[0][1])
        self.var3.set(self.updEmp[0][2])
        self.var4.set(self.updEmp[0][3])
        self.var5.set(self.updEmp[0][4])
        self.var6.set(self.updEmp[0][5])
        self.var7.set(self.updEmp[0][6])
        self.var8.set(self.updEmp[0][7])
        self.var9.set(self.updEmp[0][8])
        self.var10.set(self.updEmp[0][9])
        self.var11.set(self.updEmp[0][10])

    def item_select(self,_):
        self.deleteobj = self.emp_Table.item(self.emp_Table.selection())['values']
        print(self.deleteobj[1])

    def delete_item(self,_):
        self.emp_Table.item(self.emp_Table.selection())
        
    def deleteEmpbyid(self):
        id = self.deleteobj[1]
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
        self.var1 = tk.StringVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()
        self.var7 = tk.StringVar()
        self.var8 = tk.StringVar()
        self.var9 = tk.StringVar()
        self.var10 = tk.StringVar()
        self.var11 = tk.StringVar()
        self.deleteobj = None
        self.supervisorId = login_page.id_var.get()
        self.content = tk.Frame(main_window)
        self.createWidgets()

    def createWidgets(self):
        self.form_frame = tk.Frame(self.content)
        self.frame_Deps = tk.Frame(self.content)

        self.frame_buttons = tk.Frame(self.content)
        self.frame_buttons.pack(side='bottom',expand=True,fill='both')

        self.frame_employeestable = tk.Frame(self.content)
        self.frame_employeestable.pack(side='bottom',expand=True,fill='both')

        self.frame_noofemps = tk.Frame(self.content)
        self.frame_noofemps.pack(side='top',expand=True,fill='both')

        self.showDependents_Button = Button(self.frame_noofemps, text="Show Employee Dependents",bootstyle = "success",command= self.showDependents)
        self.showDependents_Button.pack(side = 'left',expand=True,pady=15)

        self.no_of_Emps = self.getNoofEmps()
        self.label_noofemps = tk.Label(self.frame_noofemps,text=f'No Of Employees:\n {self.no_of_Emps}',justify="center",font=("Arial ", 18))
        self.label_noofemps.pack(side = 'left',expand=True,pady=15)

        employees = self.getEmps()
        self.emp_Table = ttk.Treeview(self.frame_employeestable, columns=('Name', 'Id','sex','Job'),show='headings')
        self.emp_Table.heading('Name', text='Name')
        self.emp_Table.heading('Id', text='Id')
        self.emp_Table.heading('sex', text='Sex')
        self.emp_Table.heading('Job', text='Job')

        for emp in employees:
             self.emp_Table.insert(parent='',index=tk.END,values=emp)

        self.emp_Table.pack(expand=True,fill='both')

        self.insertEmp = Button(self.frame_buttons,text = "Add Employee" , bootstyle = 'primary', command = lambda : self.formpage("Add"))
        self.insertEmp.pack(side='left',expand=True)
        self.editEmp = Button(self.frame_buttons,text = "Edit Employee" , bootstyle = 'warning', command=self.getEmpbyid)
        self.editEmp.pack(side='left',expand=True)
        self.deleteEmp = Button(self.frame_buttons,text = "Delete Employee" , bootstyle = 'danger' , command= self.deleteEmpbyid)
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

    def hide_formpage(self):
        self.form_frame.pack_forget()

    def showDependents(self):
        self.frame_buttons.pack_forget()
        self.frame_employeestable.pack_forget()
        self.frame_noofemps.pack_forget()
        self.frame_Deps.pack()

        id = self.deleteobj[1]
        cursor.execute('exec ShowEmployeeDependents ?',(id,))
        Dependents = cursor.fetchall()
        if len(Dependents) > 0 :
            self.depend_Table = ttk.Treeview(self.frame_Deps, columns=('SSN', 'Name','Sex','BDate','Relation'),show='headings')
            self.depend_Table.heading('SSN', text='Employee SSN')
            self.depend_Table.heading('Name', text='Name')
            self.depend_Table.heading('Sex', text='Sex')
            self.depend_Table.heading('BDate', text='Birth Date')
            self.depend_Table.heading('Relation', text='Relationship')

            for dep in Dependents:
                self.depend_Table.insert(parent='',index=tk.END,values=dep)

            self.depend_Table.pack(expand=True,fill='both')
        else:
            self.depend_Label = ttk.Label(self.frame_Deps, text="This Employee\n has NO Dependents" ,font=('Arial',36), justify='center')
            self.depend_Label.pack(expand=True,fill='both')

        self.back_button = tk.Button(self.frame_Deps, text= "Back",height=2,width=10, command= self.Hide_Dependants)
        self.back_button.pack(side='bottom',expand=True)

    def Hide_Dependants(self):
        self.frame_Deps.pack_forget()
        self.createWidgets()

    def formpage(self,page):
        self.frame_buttons.pack_forget()
        self.frame_employeestable.pack_forget()
        self.frame_noofemps.pack_forget()
        self.form_frame.pack()

        self.frame1 = tk.Frame(self.form_frame)
        self.frame1.pack(side='top',expand=True,fill='both')

        self.frame2 = tk.Frame(self.form_frame)
        self.frame2.pack(side='top',expand=True,fill='both')

        self.frame3 = tk.Frame(self.form_frame)
        self.frame3.pack(side='top',expand=True,fill='both')

        self.frame4 = tk.Frame(self.form_frame)
        self.frame4.pack(side='top',expand=True,fill='both')

        self.frame5 = tk.Frame(self.form_frame)
        self.frame5.pack(side='top',expand=True,fill='both')

        self.frame6 = tk.Frame(self.form_frame)
        self.frame6.pack(side='top',expand=True,fill='both')

        self.frame7 = tk.Frame(self.form_frame)
        self.frame7.pack(side='top',expand=True,fill='both')

        self.frame8 = tk.Frame(self.form_frame)
        self.frame8.pack(side='top',expand=True,fill='both')

        self.frame9 = tk.Frame(self.form_frame)
        self.frame9.pack(side='top',expand=True,fill='both')
        
        self.frame10 = tk.Frame(self.form_frame)
        self.frame10.pack(side='top',expand=True,fill='both')

        self.frame11 = tk.Frame(self.form_frame)
        self.frame11.pack(side='top',expand=True,fill='both')

        self.frame12 = tk.Frame(self.form_frame)
        self.frame12.pack(side='top',expand=True,fill='both')

        self.label1 = tk.Label(self.frame1, text="SSN:")
        self.label1.pack(side='left',pady=5)
        self.entry1 = tk.Entry(self.frame1, textvariable=self.var1)
        self.entry1.pack(pady=5)

        self.label2 = tk.Label(self.frame2, text="Id:")
        self.label2.pack(side='left',pady=5)
        self.entry2 = tk.Entry(self.frame2, textvariable=self.var2,state='disabled')
        self.entry2.pack(pady=5)

        self.label3 = tk.Label(self.frame3, text="Password:")
        self.label3.pack(side='left',pady=5)
        self.entry3 = tk.Entry(self.frame3, textvariable=self.var3)
        self.entry3.pack(pady=5)

        self.label4 = tk.Label(self.frame4, text="Name:")
        self.label4.pack(side='left',pady=5)
        self.entry4 = tk.Entry(self.frame4, textvariable=self.var4)
        self.entry4.pack(pady=5)
        
        self.label5 = tk.Label(self.frame5, text="Sex:")
        self.label5.pack(side='left',pady=5)
        self.entry5 = tk.Entry(self.frame5, textvariable=self.var5)
        self.entry5.pack(pady=5)

        self.label6 = tk.Label(self.frame6, text="Salary:")
        self.label6.pack(side='left',pady=5)
        self.entry6 = tk.Entry(self.frame6, textvariable=self.var6)
        self.entry6.pack(pady=5)

        self.label7 = tk.Label(self.frame7, text="Birth Date:")
        self.label7.pack(side='left',pady=5)
        self.entry7 = tk.Entry(self.frame7, textvariable=self.var7)
        self.entry7.pack(pady=5)

        self.label8 = tk.Label(self.frame8, text="Address:")
        self.label8.pack(side='left',pady=5)
        self.entry8 = tk.Entry(self.frame8, textvariable=self.var8)
        self.entry8.pack(pady=5)

        self.label9 = tk.Label(self.frame9, text="SuperSSN:")
        self.label9.pack(side='left',pady=5)
        self.entry9 = tk.Entry(self.frame9, textvariable=self.var9)
        self.entry9.pack(pady=5)

        self.label10 = tk.Label(self.frame10, text="Branch:")
        self.label10.pack(side='left',pady=5)
        self.entry10 = tk.Entry(self.frame10, textvariable=self.var10)
        self.entry10.pack(pady=5)

        self.label11 = tk.Label(self.frame11, text="Job:")
        self.label11.pack(side='left',pady=5)
        self.entry11 = tk.Entry(self.frame11, textvariable=self.var11)
        self.entry11.pack(pady=5)

        if page == "update":
            self.save_button = tk.Button(self.frame12, text="Save", command=self.updateEmployee)
            self.save_button.pack(pady=10)
        elif page == "Add":
            self.save_button = tk.Button(self.frame12, text="Save", command=self.addEmployee)
            self.save_button.pack(pady=10)
   
    def updateEmployee(self):
        SSN = self.var1.get()
        emp_id = self.var2.get()
        password = self.var3.get()
        name = self.var4.get()
        sex = self.var5.get()
        salary = self.var6.get()
        birth_date = self.var7.get()
        address = self.var8.get()
        super_ssn = self.var9.get()
        branch = self.var10.get()
        job = self.var11.get()
        cursor.execute("exec update_Employee ?,?,?,?,?,?,?,?,?,?,?",(emp_id,SSN,password,name,sex,salary,birth_date,address,super_ssn,branch,job))
        cursor.commit()
        self.hide_formpage()
        self.createWidgets()
        
    def addEmployee(self):
        SSN = self.var1.get()
        password = self.var3.get()
        name = self.var4.get()
        sex = self.var5.get()
        salary = self.var6.get()
        birth_date = self.var7.get()
        address = self.var8.get()
        super_ssn = self.var9.get()
        branch = self.var10.get()
        job = self.var11.get()
        cursor.execute("exec AddEmployee ?,?,?,?,?,?,?,?,?,?",(SSN,password,name,sex,salary,birth_date,address,super_ssn,branch,job))
        cursor.commit()
        self.hide_formpage()
        self.createWidgets()

    def getEmpbyid(self):
        id = self.deleteobj[1]
        cursor.execute('exec ViewAll_Employee_Info ?',(id,))
        self.updEmp = cursor.fetchall()
        self.formpage("update")
        self.var1.set(self.updEmp[0][0])
        self.var2.set(self.updEmp[0][1])
        self.var3.set(self.updEmp[0][2])
        self.var4.set(self.updEmp[0][3])
        self.var5.set(self.updEmp[0][4])
        self.var6.set(self.updEmp[0][5])
        self.var7.set(self.updEmp[0][6])
        self.var8.set(self.updEmp[0][7])
        self.var9.set(self.updEmp[0][8])
        self.var10.set(self.updEmp[0][9])
        self.var11.set(self.updEmp[0][10])

    def item_select(self,_):
        self.deleteobj = self.emp_Table.item(self.emp_Table.selection())['values']

    def delete_item(self,_):
        self.emp_Table.item(self.emp_Table.selection())
        
    def deleteEmpbyid(self):
        id = self.deleteobj[1]
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

class EmployeePage:
    def __init__(self):
        self.content = tk.Frame(main_window)
        self.Id = login_page.id_var.get()
        self.branch = tk.StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.Employee_main_label = tk.Label(main_window,text="What would you\n like to see?",font=("Arial", 32))
        self.Employee_main_label.pack(expand=True,fill="both")

        self.show_main_buttons = tk.Frame(main_window)
        self.show_main_buttons.pack(side='bottom',expand=True,fill='both')

        self.orders_button = tk.Button(self.show_main_buttons,text="Orders",height=3,width=12,command=self.show_orders)
        self.orders_button.pack(side='left',expand=True)
        self.Reservations_button = tk.Button(self.show_main_buttons,text="Reservations",height=3,width=12 , command=self.show_reservations)
        self.Reservations_button.pack(side='right',expand=True)

    def getEmpbranch(self):
        cursor.execute('exec ViewAll_Employee_Info ?',(self.Id,))
        empbranch = cursor.fetchall()
        print (empbranch)
        return (empbranch[0][9])

    def show_orders(self):
        self.Employee_main_label.pack_forget()
        self.show_main_buttons.pack_forget()

        branch = self.getEmpbranch()
        cursor.execute('ShowOrdersInBranch ?',(branch,))
        Orders = cursor.fetchall()

        self.Orders_frame = tk.Frame(main_window)
        self.Orders_frame.pack(side='bottom',expand=True,fill='both')
        if len(Orders) > 0 :
            main_window.geometry("1200x600")
            self.Orders_table = ttk.Treeview(self.Orders_frame, columns=('OrderID', 'Date','Type','CID','Branch','Price'),show='headings')
            self.Orders_table.heading('OrderID', text='ID')
            self.Orders_table.heading('Date', text='Date')
            self.Orders_table.heading('Type', text='Type')
            self.Orders_table.heading('CID', text='Customer ID')
            self.Orders_table.heading('Branch', text='Branch')
            self.Orders_table.heading('Price', text='Price')

            for o in Orders:
                self.Orders_table.insert(parent='',index=tk.END,values=o)

            self.Orders_table.pack(expand=True,fill='both')
        else:
            self.order_Label = ttk.Label(self.Orders_frame, text="This Branch\n has NO Orders" ,font=('Arial',36), justify='center')
            self.order_Label.pack(expand=True,fill='both')

        self.back_button = tk.Button(self.Orders_frame, text= "Back",height=2,width=10, command=self.hide_orders)
        self.back_button.pack(side='bottom',expand=True)

    def hide_orders(self):
        self.Orders_frame.pack_forget()
        main_window.geometry("1000x600")
        self.createWidgets()
    
    def show_reservations(self):
        self.Employee_main_label.pack_forget()
        self.show_main_buttons.pack_forget()

        branch = self.getEmpbranch()
        cursor.execute('ShowReservationsInBranch ?',(branch,))
        Reservations = cursor.fetchall()

        self.reservations_frame = tk.Frame(main_window)
        self.reservations_frame.pack(side='bottom',expand=True,fill='both')
        if len(Reservations) > 0 :
            main_window.geometry("1200x600")
            self.Reservations_table = ttk.Treeview(self.reservations_frame, columns=('CID', 'TableNo','Reservation_Date','TimeSlot','Name','PhoneNumber'),show='headings')
            self.Reservations_table.heading('CID', text='Customer ID')
            self.Reservations_table.heading('TableNo', text='TableNo')
            self.Reservations_table.heading('Reservation_Date', text='Reservation_Date')
            self.Reservations_table.heading('TimeSlot', text='TimeSlot')
            self.Reservations_table.heading('Name', text='Name')
            self.Reservations_table.heading('PhoneNumber', text='Phone Number')

            for r in Reservations:
                self.Reservations_table.insert(parent='',index=tk.END,values=r)

            self.Reservations_table.pack(expand=True,fill='both')
        else:
            self.reservation_Label = ttk.Label(self.reservations_frame, text="This Branch\n has NO Reservations" ,font=('Arial',36), justify='center')
            self.reservation_Label.pack(expand=True,fill='both')

        self.back_button = tk.Button(self.reservations_frame, text= "Back",height=2,width=10, command=self.hide_reservations)
        self.back_button.pack(side='bottom',expand=True)

    def hide_reservations(self):
        self.reservations_frame.pack_forget()
        main_window.geometry("1000x600")
        self.createWidgets()

    def show_frame(self):
        self.content.pack(expand=True,fill="both")
    
def display():
    main_buttons.pack_forget()
    login_page.show_frame()

def hide_menu():
    main_menu.pack_forget()
    main_buttons.pack(side='bottom',expand=True,fill='both')
    main_window_label.pack(expand=True,fill="both")

def show_menu():
    main_buttons.pack_forget()
    main_window_label.pack_forget()
    main_menu.pack(expand=True,fill='both')    
    cursor.execute('exec ShowMenu')
    Meals = cursor.fetchall()
    Menu = ttk.Treeview(main_menu, columns=('Meal', 'Price','Type'),show='headings')
    Menu.heading('Meal', text='Meal Name')
    Menu.heading('Price', text='Price')
    Menu.heading('Type', text='Meal Type')

    for meal in Meals:
        Menu.insert(parent='',index=tk.END,values=meal)

    Menu.pack(expand=True,fill='both')

    menu_back_button = tk.Button(main_menu, text= "Back",height=2,width=10, command= hide_menu)
    menu_back_button.pack(expand=True)

main_window = Window(themename='darkly')
main_window.geometry("1000x600")
main_window.title("Arabisqly")
main_window_label = tk.Label(main_window,text="Welcome to Arabisq",font=("courier new bold", 42))
main_window_label.pack(expand=True,fill="both")
main_buttons = tk.Frame(main_window)
main_buttons.pack(side='bottom',expand=True,fill='both')
main_window_button = tk.Button(main_buttons,text="Start",height=2,width=10,command= display)
main_window_button.pack(side='left',expand=True)
main_window_button_menu = tk.Button(main_buttons,text="Menu",height=2,width=10,command= show_menu)
main_window_button_menu.pack(side='right',expand=True)
main_menu = tk.Frame(main_window)
login_page = LoginPage()

main_window.mainloop()

