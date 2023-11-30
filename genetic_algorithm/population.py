import pandas as pd
import random as rnd
from data import (
    Data,
    Shift,
    Arrangement,
    Employee,
    NUMB_SHIFTS_PER_EMPLOYEE,
    DATES
)
POPULATION_SIZE = 10
DATA = Data()
SHIFTS = DATA.get_shifts()
EMPLOYEES = DATA.get_employees()

class Schedule:
    """
    This class initializes an individual, calculate the ability of individual adaptation.
    ### Method
    - `initialize`: randomly initialize a individual
    - `get_arrangement`: return a list of `Arrangement` objects that are just initialized
    - `get_conflicts`: return a list of conflicts by each condition
    - `get_numbOfConflicts`: return the total conflicts
    - `get_fitness`: return the fitness of population, where there is no conflict, fitness is equal to 1
    """
    def __init__(self) -> None:
        self.shifts = SHIFTS
        self.employees = EMPLOYEES
        self.arrangement = []
        self.totalShifts = len(SHIFTS)
        self.numbOfConflicts = 0
        self.numbOfConflicts1 = 0
        self.numbOfConflicts2 = 0
        self.numbOfConflicts3 = 0
        self.fitness = -1
        self.isFitnessChanged = True
    def get_arrangement(self):
        self.isFitnessChanged = True
        return self.arrangement
    def get_numbOfConflicts(self): return self.numbOfConflicts
    def get_conflicts(self): return [self.numbOfConflicts1, self.numbOfConflicts2, self.numbOfConflicts3]
    def get_fitness(self):
        if self.isFitnessChanged == True:
            self.fitness = self.calculate_fitness()
            self.isFitnessChanged = False
        return self.fitness

    def initialize(self):
        shifts = self.shifts
        employees = self.employees
        for shift in shifts:
            assert isinstance(shift, Shift)

            minEmps = shift.get_minEmp()
            maxEmps = shift.get_maxEmp()
            newShift = Arrangement(shift)
            selectedEmployees = rnd.choices(employees, k=rnd.randint(minEmps, maxEmps))
            newShift.set_employeeList(selectedEmployees)
            self.arrangement.append(newShift)
        return self
    def calculate_fitness(self):
        arrangement = self.get_arrangement()
        df = pd.DataFrame()
        for a in arrangement:
            # check whether `a` is `Arrangement` object
            assert isinstance(a, Arrangement)

            temp = pd.DataFrame([{
                'shiftName': a.get_Shift().get_shift(),
                'minEmployees': a.get_Shift().get_minEmp(),
                'maxEmployees': a.get_Shift().get_maxEmp(),
                'employeeList': a.get_employeeList()
            }])
            df = pd.concat([df, temp])
        df = df.explode('employeeList')
        df['EmployeeCode'] = df['employeeList'].apply(lambda x: x.get_code() if isinstance(x, Employee) else x)
        df['JobTitleName'] = df['employeeList'].apply(lambda x: x.get_title() if isinstance(x, Employee) else x)

        # check whether all shifts are always observed by managers
        df_managers = df[df['JobTitleName'].isin(['Manager','Leader'])]
        numbOfShiftsWithManager = df_managers['shiftName'].nunique()
        self.numbOfConflicts1 = self.totalShifts - numbOfShiftsWithManager

        # check whether each employee has exactly `NUMB_SHIFTS_PER_EMPLOYEE` shifts in month    
        numbOfEmpsNotExactShifts = (
            df
            .groupby('EmployeeCode', as_index=False)
            .agg(numbShifts=('shiftName','nunique'))
            .query(f"numbShifts < {NUMB_SHIFTS_PER_EMPLOYEE} or numbShifts > {DATES}").shape[0]
        )
        self.numbOfConflicts2 = numbOfEmpsNotExactShifts

        # check whether the number of employees in each shift is in the range
        numbOfShiftsNotEnoughEmps = (
            df
            .groupby(['shiftName','minEmployees','maxEmployees'], as_index=False)
            .agg(Employees=('EmployeeCode','nunique'))
            .query("~Employees.between(minEmployees,maxEmployees)")
            .shape[0]
        )
        self.numbOfConflicts3 = numbOfShiftsNotEnoughEmps
        
        # sum of numbOfConflict components
        self.numbOfConflicts = self.numbOfConflicts1 + self.numbOfConflicts2 + self.numbOfConflicts3

        return 1 / (self.get_numbOfConflicts() + 1)

class Population:
    """
    This class generates a set of individuals in a population.
    ### Parameter
    `size`: `int`, `optional`, default `POPULATION_SIZE`
        The population size, the number of individuals
    ### Method
    - `get_schedules`: return a population of scheduled individuals
    """
    def __init__(self, size=POPULATION_SIZE):
        self.schedules = []
        for _ in range(0, size):
            self.schedules.append(Schedule().initialize())
        self.schedules.sort(key=lambda x: x.get_fitness(), reverse=True)
    def get_schedules(self): return self.schedules