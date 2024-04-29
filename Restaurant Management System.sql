create database Arabisqly;
use Arabisqly;

CREATE TABLE Employee (
    SSN char(14) PRIMARY KEY,
	Id int Unique IDENTITY,
	Password varchar(99) not null,
    Name VARCHAR(50),
    Sex CHAR(6),
    Salary DECIMAL,
    B_Date DATE,
    Address VARCHAR(100),
    Super_SSN char(14),
    Branch VARCHAR(25),
	Job VARCHAR(10),
    CONSTRAINT fk_SupSSN FOREIGN KEY (Super_SSN) REFERENCES Employee(SSN)
);

CREATE TABLE Dependent (
    Dependent_Name VARCHAR(255),
    Sex CHAR(6),
    B_Date DATE,
    Relationship VARCHAR(50),
    Emp_SSN CHAR(14),
	CONSTRAINT PK_Depandent PRIMARY KEY (Dependent_Name,Emp_SSN),
    CONSTRAINT fk_DependEmpSSN FOREIGN KEY (Emp_SSN) REFERENCES Employee(SSN)
);

CREATE TABLE Branch (
    Branch_Name VARCHAR(25) PRIMARY KEY,
    Location VARCHAR(100) UNIQUE not null,
    MNGR_SSN char(14) not null,
	MNGR_StartDate Date not null,
	CONSTRAINT Fk_MNGRSSN FOREIGN KEY (MNGR_SSN) REFERENCES Employee(SSN)
);

Alter Table Employee add CONSTRAINT Fk_EMPBranch FOREIGN KEY (Branch) REFERENCES Branch (Branch_Name)

CREATE TABLE _Table_ (
	Table_No int not null,
	Status VARCHAR(8) not null,
	NO_of_Seats int not null,
	WaiterSSN char(14) not null,
	Branch VARCHAR(25) not null,
	CONSTRAINT Pk_Table PRIMARY KEY (Table_No,Branch),
	CONSTRAINT Fk_WaiterSSN FOREIGN KEY (WaiterSSN) REFERENCES Employee(SSN),
	CONSTRAINT Fk_TableBranch FOREIGN KEY (Branch) REFERENCES Branch(Branch_Name)
);

CREATE TABLE Customer(
	Name varchar(50),
	CustomerID int PRIMARY KEY
);

CREATE TABLE CustomerPhoneNumber(
	CID int,
	PhoneNumber char(11) unique,
	CONSTRAINT PK_CustPhone PRIMARY KEY (CID,PhoneNumber),
	CONSTRAINT Fk_PhonesCustID FOREIGN KEY (CID) REFERENCES Customer (CustomerID)
);

CREATE TABLE CustomerAddress(
	CID int,
	Address VARCHAR(100) not null,
	CONSTRAINT PK_CustAddress PRIMARY KEY (CID,Address),
	CONSTRAINT Fk_AddressesCustID FOREIGN KEY (CID) REFERENCES Customer (CustomerID)
);

CREATE TABLE Reserves(
	CID int,
	TableNo int,
	Branch VARCHAR(25),
	Reservation_Date date,
	TimeSlot Time,
	CONSTRAINT PK_CustReservation PRIMARY KEY (CID,TableNo,Branch,Reservation_Date,TimeSlot),
	CONSTRAINT Fk_ReservationBranch FOREIGN KEY (Branch) REFERENCES Branch(Branch_Name),
	CONSTRAINT Fk_ReservesCustID FOREIGN KEY (CID) REFERENCES Customer (CustomerID),
	CONSTRAINT Fk_ReservesTable FOREIGN KEY (TableNo,Branch) REFERENCES _Table_ (Table_No,Branch)
);

CREATE TABLE Job(
	Job_Name varchar(10) PRIMARY KEY,
	Min_Salary DECIMAL not null,
	Clearance_Level int not null
);

Alter Table Employee add CONSTRAINT Fk_EMPJob FOREIGN KEY (Job) REFERENCES Job (Job_Name)

CREATE TABLE _Order_(
	OrderID int IDENTITY PRIMARY KEY,
	orderDate Date not null,
	OrderType varchar(10) not null
);

CREATE TABLE Places(
	CID int,
	Order_ID INT,
	BranchName VARCHAR(25),
	CONSTRAINT PK_PlaceOrder PRIMARY KEY (CID,Order_ID,BranchName),
	CONSTRAINT Fk_orderCust FOREIGN KEY (CID) REFERENCES Customer (CustomerID),
	CONSTRAINT Fk_placeorder FOREIGN KEY (Order_ID) REFERENCES _Order_ (OrderID),
	CONSTRAINT Fk_placesBranch FOREIGN KEY (BranchName) REFERENCES Branch (Branch_Name)
);

CREATE TABLE Meal(
	Meal_Name VARCHAR(25) PRIMARY KEY,
	Meal_Type VarChar (10) not null,
	No_of_Ingredients int not null,
	Price Decimal not null,
	ChefSSN char(14) not null,
	CONSTRAINT Fk_MealChef FOREIGN KEY (ChefSSN) REFERENCES Employee (SSN)
);

CREATE TABLE Consists_of(
	Order_ID int,
	Meal_Name VARCHAR(25) not null,
	MealQuantity int not null,
	CONSTRAINT PK_Consists_of PRIMARY KEY (Order_ID,Meal_Name),
	CONSTRAINT Fk_MealConstof FOREIGN KEY (Meal_Name) REFERENCES Meal (Meal_Name),
	CONSTRAINT Fk_OrderConstof FOREIGN KEY (Order_ID) REFERENCES _Order_ (OrderID)
);

INSERT INTO Employee (SSN, Password, Name, Sex, Salary, B_Date, Address, Super_SSN) VALUES
('12345678909876',  'passwordMzn', 'mazen', 'Male', 50000.00, '2003-05-15', 'omar ibn elkhtab, Nasrcity', NULL),
('76548357565384',  'passwordAly', 'Aley', 'Male', 60000.00, '2003-10-20', 'zahraa elmaady st, Elmaady', '12345678909876'),
('09098787654565',  'passwordhsn', 'Hassan', 'Male', 55000.00, '2003-03-25', 'Ahmed hassan elzyad, Nasrcity', '12345678909876'),
('46353645354635',  'passwordsf', 'Seif', 'male', 65000.00, '2003-08-10', 'mostafa elnahhas, NasrCity', '09098787654565'),
('69472835382869', 'passwordfdlya','Ahmed', 'Male', 55000.00, '2003-10-09', 'elmosheer, tagamo', '09098787654565');


INSERT INTO Dependent (Dependent_Name, Sex, B_Date, Relationship, Emp_SSN) VALUES
('menna', 'Female', '2024-03-12', 'Daughter', '12345678909876'),
('ayman', 'Male', '2023-07-25', 'Son', '09098787654565'),
('asmaa', 'Female', '2003-04-30', 'Wife', '76548357565384');

INSERT INTO Branch(Branch_Name, Location, MNGR_SSN, MNGR_StartDate) VALUES
('korba', 'korba', '76548357565384', '2020-03-17'),
('Nasr', 'Nasr city','09098787654565', '2021-02-12');

INSERT INTO _Table_(Table_No, Status, NO_of_Seats, WaiterSSN,Branch) VALUES
(1, 'Free',4,'69472835382869','korba' ),
(2, 'Reserved',8,'69472835382869','korba');

INSERT INTO Customer(Name, CustomerID) VALUES
('Ayman',1),
('mohamed',2);

INSERT INTO CustomerPhoneNumber(CID, PhoneNumber) VALUES
(1,'01022648300'),
(2,'01005102143');

insert into CustomerAddress(CID,Address) values
(1,'abdo basha'),
(2,'salah salem');

insert into Reserves(CID,TableNo,Branch,Reservation_Date,TimeSlot) values
(1,2,'korba','2024-5-5','08:00:00' ),
(2,1,'korba','2024-5-6','10:00:00');

INSERT INTO Job (Job_Name, Min_Salary, Clearance_Level) VALUES
('Manager', 50000.00, 1),
('chef', 10000.00, 3),
('supervisor', 40000.00, 2),
('waiter', 40000.00, 3);

insert into _Order_(orderDate,OrderType) values
('2024-5-5','eat in'),
('2024-5-6','eat in');

insert into Places(CID,Order_ID,BranchName) values
(1,1,'korba'),
(2,2,'korba');

INSERT INTO Meal (Meal_Name, Meal_Type, No_of_Ingredients, Price, ChefSSN) VALUES
('Pizza', 'Main', 8, 40.00, '09098787654565'),
('Pasta', 'Main', 6, 20.00, '09098787654565'),
('Salad', 'Starter', 4, 8.00, '09098787654565');

INSERT INTO Consists_of (Order_ID, Meal_Name, MealQuantity) VALUES
(1, 'Pizza',2),
(2, 'Pasta',5);

UPDATE Employee
SET Branch = 'Nasr'
WHERE Id = 1;

UPDATE Employee
SET Job='Supervisor'
WHERE Id = 1;

UPDATE Employee
SET Branch = 'Nasr', Job='Manager'
WHERE Id = 2;

UPDATE Employee
SET Branch = 'Korba', Job='Manager'
WHERE Id = 3;

UPDATE Employee
SET Branch = 'Nasr', Job='Waiter'
WHERE Id = 4;

UPDATE Employee
SET Branch = 'Korba', Job='Chef'
WHERE Id = 5;


CREATE PROCEDURE Login_func (@Id AS int  ,@Password AS varchar(99))
AS
BEGIN
  SELECT count(*),Job
  from Employee

  where Id=@Id and password=@Password
  group by Job

END;


create procedure View_Branch_Employee (@ManagerId AS int)
AS
BEGIN
	declare @branch varchar(25)
	set @branch = (
	select Branch_Name 
	from Branch b , Employee e 
	where b.MNGR_SSN = e.SSN and e.Id = @ManagerId
	);

	select Name,id,sex,job 
	from Employee
	where branch = @Branch
END;

create procedure ViewAll_Employee_Info (@empId AS int)
AS
BEGIN
	select * 
	from Employee
	where id = @empId
END;


create procedure View_Branch_NoOfEmployee (@ManagerId AS int)
AS
BEGIN
	declare @branch varchar(25)
	set @branch = (
	select Branch_Name 
	from Branch b , Employee e 
	where b.MNGR_SSN = e.SSN and e.Id = @ManagerId
	);

	select count(*)
	from Employee
	where branch = @Branch
END;
exec View_Branch_NoOfEmployee 3


create procedure view_employees (@SuperId AS int)
AS
BEGIN
	DECLARE @S_SSN char(14);

	SET @S_SSN = (
    SELECT 
        SSN
    FROM 
        Employee
	Where 
		id=@SuperId
);
	select Name,id,sex,job 
	from Employee
	where Super_SSN = @S_SSN
END;

exec View_Employees 3


create procedure view_NoOfEmployees (@SuperId AS int)
AS
BEGIN
	DECLARE @S_SSN char(14);

	SET @S_SSN = (
    SELECT 
        SSN
    FROM 
        Employee
	Where 
		id=@SuperId
);
	select count(*)
	from Employee
	where Super_SSN = @S_SSN
END;
exec view_NoOfEmployees 1



create procedure View_Branch_NoOrders (@ManagerId AS int)
AS
BEGIN
	declare @branch varchar(25)
	set @branch = (
	select Branch_Name 
	from Branch b , Employee e 
	where b.MNGR_SSN = e.SSN and e.Id = @ManagerId
	);

	select count(*)
	from _Order_ o, Places p
	where p.BranchName = @Branch and p.Order_ID = o.OrderID
END;

ALTER TABLE Branch
ALTER COLUMN MNGR_SSN CHAR(14) NULL;

ALTER TABLE Branch
DROP CONSTRAINT Fk_MNGRSSN;

ALTER TABLE Branch
ADD CONSTRAINT Fk_MNGRSSN FOREIGN KEY (MNGR_SSN) REFERENCES Employee(SSN)
ON DELETE SET NULL;

ALTER TABLE Meal
DROP CONSTRAINT Fk_MealChef;

ALTER TABLE Meal
ALTER COLUMN ChefSSN CHAR(14) NULL;

ALTER TABLE Meal
ADD CONSTRAINT Fk_MealChef
FOREIGN KEY (ChefSSN)
REFERENCES Employee(SSN)
ON DELETE SET NULL;

CREATE PROCEDURE AddEmployee
    @SSN CHAR(14),
    @Password VARCHAR(99),
    @Name VARCHAR(50),
    @Sex CHAR(6),
    @Salary DECIMAL,
    @B_Date DATE,
    @Address VARCHAR(100),
    @Super_SSN CHAR(14),
    @Branch VARCHAR(25),
    @Job VARCHAR(10)
AS
BEGIN
    INSERT INTO Employee (SSN, Password, Name, Sex, Salary, B_Date, Address, Super_SSN, Branch, Job)
    VALUES (@SSN, @Password, @Name, @Sex, @Salary, @B_Date, @Address, @Super_SSN, @Branch, @Job);
END;


EXEC AddEmployee 
    @SSN = '47575758757575',
    @Password = 'newp',
    @Name = 'abdelrahman',
    @Sex = 'Male',
    @Salary = 60000.00,
    @B_Date = '1999-05-15',
    @Address = 'aabas elaad street, Nasr city',
    @Super_SSN = '12345678909876',
    @Branch ='korba',
    @Job = 'waiter';

CREATE PROCEDURE RemoveEmployeeById
    @Id INT
AS
BEGIN
    DECLARE @EmpSSN CHAR(14);

    -- Get the SSN of the employee to be deleted
    SELECT @EmpSSN = SSN
    FROM Employee
    WHERE Id = @Id;

    -- Update Branch records where the employee is a manager
    UPDATE Branch
    SET MNGR_SSN = NULL
    WHERE MNGR_SSN = @EmpSSN;

    -- Delete dependent records associated with the employee
    DELETE FROM Dependent
    WHERE Emp_SSN = @EmpSSN;

    -- Delete the employee
	UPDATE Meal
SET ChefSSN = NULL  -- or another valid chef's SSN
WHERE ChefSSN = (SELECT SSN FROM Employee WHERE Id = @Id);

    DELETE FROM Employee
    WHERE Id = @Id;

    -- If the deleted employee is a supervisor, set supervisees' Super_SSN to NULL
    IF EXISTS (SELECT 1 FROM Employee WHERE Super_SSN = @EmpSSN)
    BEGIN
        UPDATE Employee
        SET Super_SSN = NULL
        WHERE Super_SSN = @EmpSSN;
    END;
END;

--update

CREATE PROCEDURE update_Employee
	@Id int,
    @SSN CHAR(14),
    @Password VARCHAR(99),
    @Name VARCHAR(50),
    @Sex CHAR(6),
    @Salary DECIMAL,
    @B_Date DATE,
    @Address VARCHAR(100),
    @Super_SSN CHAR(14),
    @Branch VARCHAR(25),
    @Job VARCHAR(10)
AS
BEGIN
  UPDATE Employee
    SET Password = @Password,
        Name = @Name,
        Sex = @Sex,
        Salary = @Salary,
        B_Date = @B_Date,
        Address = @Address,
        Super_SSN = @Super_SSN,
        Branch = @Branch,
        Job = @Job
    WHERE Id = @Id;
END;


EXEC update_Employee 
	@Id=1011,
    @SSN = '69696969696969',
    @Password = 'updatedpass',
    @Name = 'horny',
    @Sex = 'Male',
    @Salary = 690000.00,
    @B_Date = '1899-05-15',
    @Address = 'aabas elaad street, Nasr city',
    @Super_SSN = '12345678909876',
    @Branch ='nasr',
    @Job = 'waiter';


CREATE PROCEDURE ShowReservationsInBranch
    @BranchName VARCHAR(25)
AS
BEGIN
    SELECT 
        R.CID,
        R.TableNo,
        R.Reservation_Date,
        R.TimeSlot,
        C.Name AS CustomerName,
		CPN.PhoneNumber

    FROM 
        Reserves R
    JOIN 
        Customer C ON R.CID = C.CustomerID
	Join
		CustomerPhoneNumber CPN on CPN.CID = C.CustomerID
    JOIN 
        Places P ON R.CID = P.CID  AND R.Branch = P.BranchName

    WHERE 
        R.Branch = @BranchName;
END;


CREATE PROCEDURE ShowOrdersInBranch
    @BranchName VARCHAR(25)
AS
BEGIN
    SELECT 
        O.OrderID,
        O.orderDate,
        O.OrderType,
        P.CID,
        P.BranchName AS OrderBranch,
        dbo.CalculateOrderPrice(O.OrderID) AS TotalPrice
    FROM 
        _Order_ O
    JOIN 
        Places P ON O.OrderID = P.Order_ID
    WHERE 
        P.BranchName = @BranchName;
END;

EXEC ShowOrdersInBranch @BranchName = 'korba';

CREATE FUNCTION CalculateOrderPrice
(
    @OrderID INT
)
RETURNS DECIMAL(10, 2)
AS
BEGIN
    DECLARE @TotalPrice DECIMAL(10, 2);

    SELECT @TotalPrice = SUM(M.Price * CO.MealQuantity)
    FROM _Order_ O
    INNER JOIN Consists_of CO ON O.OrderID = CO.Order_ID
    INNER JOIN Meal M ON CO.Meal_Name = M.Meal_Name
    WHERE O.OrderID = @OrderID;

    RETURN ISNULL(@TotalPrice, 0);
END;

SELECT dbo.CalculateOrderPrice(1) AS TotalPrice;



CREATE PROCEDURE ShowEmployeeDependents @empId int
AS
BEGIN
    SELECT 
        E.SSN AS EmployeeSSN,
        D.Dependent_Name,
        D.Sex AS DependentSex,
        D.B_Date AS DependentBirthDate,
        D.Relationship
    FROM 
        Employee E
    INNER JOIN 
        Dependent D ON E.SSN = D.Emp_SSN
	Where 
		e.id = @empId
END;

EXEC ShowEmployeeDependents 1012


CREATE PROCEDURE ShowMenu
AS
BEGIN
    SELECT Meal_Name AS "Menu Item", Price AS ItemPrice , Meal_Type 
    FROM Meal;
END;

EXEC ShowMenu;