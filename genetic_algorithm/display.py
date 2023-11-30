import pandas as pd
from prettytable import PrettyTable
from data import Data, Employee, Shift, Arrangement
from population import Population, Schedule

DATA = Data()
SHIFTS = DATA.get_shifts()
EMPLOYEES = DATA.get_employees()

class DisplayMgr:
    """
    This class prints readable outputs.
    ### Method
    - `print_available_data`: print all available data
    - `print_employees`: print all employees
    - `print_shifts`: print all shifts
    - `print_generation`: print all individuals in a population
    - `print_schedule_as_table`: print and return an individual
    """
    def __init__(self) -> None:
        pass

    def print_available_data(self):
        print('> All Available Data')
        self.print_employees()
        self.print_shifts()
    
    def print_employees(self, limit:int=None):
        availableEmpTable = PrettyTable(['employeeCode', 'jobTitleName'])
        for employee in EMPLOYEES:
            assert isinstance(employee, Employee)
            availableEmpTable.add_row([employee.get_code(), employee.get_title()])
        print('\n> Employees')
        if limit == None:
            print(availableEmpTable)
        else:
            print(availableEmpTable[:limit])

    def print_shifts(self, limit:int=None):
        availableShiftTable = PrettyTable(['shiftName', 'minEmployees', 'maxEmployees'])
        for shift in SHIFTS:
            assert isinstance(shift, Shift)
            availableShiftTable.add_row([shift.get_shift(), shift.get_minEmp(), shift.get_maxEmp()])
        print('\n> Shifts Info')
        if limit == None:
            print(availableShiftTable)
        else:
            print(availableShiftTable[:limit])
    
    def print_generation(self, population:Population):
        table1 = PrettyTable(['schedule #', 'fitness', '# of conflicts', 'conflicts details'])
        schedules = population.get_schedules()
        for i, schedule in enumerate(schedules):
            assert isinstance(schedule, Schedule)
            conflicts = schedule.get_conflicts()
            table1.add_row([str(i), round(schedule.get_fitness(), 3), schedule.get_numbOfConflicts(), conflicts])
        print(table1)
    
    def print_schedule_as_table(self, schedule:Schedule, limit:int=None):
        arrangement = schedule.get_arrangement()
        columns = ['shiftName', 'EmployeeCode', 'JobTitleName']
        table = PrettyTable(columns)
        schedules = []
        for a in arrangement:
            assert isinstance(a, Arrangement)
            shiftName = a.get_Shift().get_shift()
            employees = a.get_employeeList()
            for e in employees:
                assert isinstance(e, Employee)
                row_data = [
                    shiftName,
                    e.get_code(),
                    e.get_title()
                ]
                table.add_row(row_data)
                schedules.append(dict(zip(columns, row_data)))
        if limit == None:
            print(table)
        else:
            print(table[:limit])

        return pd.DataFrame(schedules)