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

class Schedule:
    """
    This class initializes an individual, calculate the ability of individual adaptation.
    ### Parameter
    `data`: `Data`, `optional`
        The `Data` object contains a set of employees and shifts
    ### Method
    - `initialize`: randomly initialize a individual
    - `get_arrangement`: return a list of `Arrangement` objects that are just initialized
    - `get_conflicts`: return a list of conflicts by each condition
    - `get_numbOfConflicts`: return the total conflicts
    - `get_fitness`: return the fitness of population, where there is no conflict, fitness is equal to 1
    """
    def __init__(self, data=Data()) -> None:
        self.data = data
        self.arrangement = []
        self.totalShifts = len(self.data.get_shifts())
        self.numbOfConflicts = 0
        self.conflicts = []
        self.fitness = -1
        self.isFitnessChanged = True
    def get_arrangement(self):
        self.isFitnessChanged = True
        return self.arrangement
    def get_numbOfConflicts(self): return self.numbOfConflicts
    def get_conflicts(self): return self.conflicts
    def get_fitness(self):
        if self.isFitnessChanged == True:
            self.fitness = self.calculate_fitness()
            self.isFitnessChanged = False
        return self.fitness

    def initialize(self):
        shifts = self.data.get_shifts()
        employees = self.data.get_employees()
        for shift in shifts:
            assert isinstance(shift, Shift)

            minEmps = shift.get_minEmp()
            maxEmps = shift.get_maxEmp()
            newShift = Arrangement(shift)
            selectedEmployees = rnd.choices(employees, k=rnd.randint(minEmps, maxEmps))
            # for employee in employees:
            #     isSelected = rnd.getrandbits(1)
            #     if isSelected == 1:
            #         selectedEmployees.append(employee)
            
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
        self.conflicts.append(self.totalShifts - numbOfShiftsWithManager)

        # check whether the number of employees is greater than or equal to the threshold (minimum of employees number)
        # numbOfShiftsLackOfEmps = (
        #     df
        #     .groupby(['shiftName','minEmployees','maxEmployees'], as_index=False)
        #     .agg(numbEmployees=('EmployeeCode','nunique'))
        #     .query("numbEmployees < minEmployees or numbEmployees > maxEmployees").shape[0]
        # )
        # self.conflicts.append(numbOfShiftsLackOfEmps)

        # check whether each employee has exactly `NUMB_SHIFTS_PER_EMPLOYEE` shifts in month    
        numbOfEmpsNotExactShifts = (
            df
            .groupby('EmployeeCode', as_index=False)
            .agg(numbShifts=('shiftName','nunique'))
            .query(f"numbShifts < {NUMB_SHIFTS_PER_EMPLOYEE} or numbShifts > {DATES}").shape[0]
        )
        self.conflicts.append(numbOfEmpsNotExactShifts)
        
        # sum of numbOfConflict components
        self.numbOfConflicts = sum(self.conflicts)

        return 1 / (self.get_numbOfConflicts() + 1)

class Population:
    """
    This class generates a set of individuals in a population.
    ### Parameter
    `data`: `Data`, `optional`
        The `Data` object contains a set of employees and shifts
    `size`: `int`, `optional`, default `POPULATION_SIZE`
        The population size, the number of individuals
    ### Method
    - `get_schedules`: return a population of scheduled individuals
    """
    def __init__(self, data=Data(), size=POPULATION_SIZE):
        self.size = size
        self.schedules = []
        for _ in range(0, size):
            self.schedules.append(Schedule(data).initialize())
    def get_schedules(self): return self.schedules