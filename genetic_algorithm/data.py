from datetime import date
import pandas as pd
from calendar import monthrange

# define the month of year
YEAR = 2023
MONTH = 9
LAST_DAY = monthrange(YEAR, MONTH)[1]
DAYS = list(range(1, LAST_DAY+1))
DATES = len(DAYS)
START_DATE = date(YEAR, MONTH, 1)
END_DATE = date(YEAR, MONTH, LAST_DAY)

# list of employees
EMPLOYEES = []
for i in range(0,10):
    sub = []
    if i == 0:
        sub = ["E0", "Manager"]
    elif i in (1,2):
        sub = [f"E{i}", "Leader"]
    else:
        sub = [f"E{i}", "Staff"]
    EMPLOYEES.append(sub)

# list of shifts
SHIFTS = []
HALF_OF_EMPLOYEES = len(EMPLOYEES) // 2
for DATE in pd.date_range(START_DATE, END_DATE):
    day = DATE.day
    day_name = DATE.day_name()
    for session in ["MOR","EVE"]:
        if session == "MOR":
            minEmp = HALF_OF_EMPLOYEES - 2
        else:
            # the evening is expected to attract more customers than the morning
            # therefore, it is expected to need more employees in the evening
            minEmp = HALF_OF_EMPLOYEES - 1
        
        if day_name in ('Saturday','Sunday'):
            # the customers get more free time on the weekend
            # they tend to go shopping more than on the weekdays
            # that is why the store needs more employees
            minEmp = minEmp + 1

        # each shift has at least 2 employees, even no customer visit
        minEmp = max(minEmp, 2)
        # the store also care about the cost, should limit the number of employees
        maxEmp = minEmp + 2

        SHIFTS.append([
            str(day).zfill(2) + '-' + session,
            minEmp,
            maxEmp
        ])

# define number of shifts each employee must join
NUMB_SHIFTS_PER_EMPLOYEE = 23

class Employee:
    """
    This class holds the information of an employee.
    ### Parameter
    `EmployeeCode`: `str`, `required`
        The ID of employees
    `JobTitleName`: `str`, `required`
        The job title name of employees, can be `Manager`, `Leader`, `Staff`
    
    ### Method
    - `get_code`: return the employee code
    - `get_title`: return the employee job title name
    """
    def __init__(self, EmployeeCode:str, JobTitleName:str):
        self.code = EmployeeCode
        self.title = JobTitleName
    
    def get_code(self): return self.code
    def get_title(self): return self.title

class Shift:
    """
    This class holds the information of a work shift.
    ### Parameter
    `shiftName`: `str`, `required`
        The name of work shifts, each day has two shifts (morning & evening)
    `minEmployees`: `str`, `required`
        The minimum number of employees required in each shift
    `maxEmployees`: `str`, `required`
        The maximum number of employees required in each shift
    ### Method
    - `get_shift`: return the shift name
    - `get_minEmp`: return the minimum number of employees in each shift
    - `get_maxEmp`: return the maximum number of employees in each shift
    """
    def __init__(self, shiftName:str, minEmployees:int, maxEmployees:int):
        self.shift = shiftName
        self.minEmp = minEmployees
        self.maxEmp = maxEmployees

    def get_shift(self): return self.shift
    def get_minEmp(self): return self.minEmp
    def get_maxEmp(self): return self.maxEmp

class Arrangement:
    """
    This class assigns a list of initialized employees to a work shift.
    ### Parameter
    `shift`: `Shifts`, `required`
        `Shifts` object, contains the information of a work shift
    ### Method
    - `get_Shifts`: return a set of work shift information
    - `get_employeeList`: return a list of employees assigned to the work shift
    - `set_employeeList`: assign a list of employees to the work shift
    """
    def __init__(self, shift:Shift):
        self.shift = shift
        self.employeeList = []
    def get_Shift(self): return self.shift
    def get_employeeList(self): return self.employeeList
    def set_employeeList(self, employeeList:list) -> None: self.employeeList = employeeList

class Data:
    """
    This class consolidates data needed for scheduling the work shift.
    ### Parameter
    `employees`: `list`, `optional`
        A list of employee information, contains `employeeCode` and `JobTitleName`
    `shifts`: `list`, `optional`
        A list of shift information, contains `shiftName`, `minEmployees` and `maxEmployees`
    ### Method
    - `get_employees`: return a list of `Employees` object
    - `get_shifts`: return a list of `Shifts` object
    """
    def __init__(self, employees=EMPLOYEES, shifts=SHIFTS):
        self.employees = []
        self.shifts = []
        for row in employees:
            self.employees.append(Employee(*row))
        for row in shifts:
            self.shifts.append(Shift(*row))
            
    def get_employees(self): return self.employees
    def get_shifts(self): return self.shifts