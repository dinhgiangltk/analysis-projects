import random as rnd
import prettytable

POPULATION_SIZE = 10
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

def random_chunks(iters, n:int, max_drop:int, first_limit:int, last_limit:int):
    S = list(iters)
    chunks = []
    rnd.shuffle(S)
    drop = rnd.randint(0, max_drop)
    S = S[drop:]
    start = rnd.randint(first_limit,len(S)-last_limit-1)
    end = rnd.randint(start+1,len(S)-last_limit)
    chunks.append(S[:start])
    midS = S[start:end]
    for _ in range(n-2):
        mid = rnd.randint(0,len(midS))
        chunks.append(midS[:mid])
        midS = midS[mid:]
    chunks.append(S[end:])
    return chunks

class Data:
    """"""
    EMPLOYEES = df_empT11Level.values.tolist()
    SHIFTS = df_workShiftsMonth.values.tolist()
    SALES = df_salesEmpLv.drop(columns=['employees','customers_dayhour','avg_customers_dayhour','max_of_avg_customers_dayhour']).values.tolist()
    TARGETSHOP = df_targetShop.values.tolist()
    TARGETEMP = df_targetEmp.values.tolist()
    def __init__(self):
        self._employees = []; self._shifts = []; self._sales = []; self._targetShop = []; self._targetEmp = []
        for row in self.EMPLOYEES:
            self._employees.append(Employees(*row))
        for row in self.SHIFTS:
            self._shifts.append(Shifts(*row))
        for row in self.SALES:
            self._sales.append(Sales(*row))
        for row in self.TARGETSHOP:
            self._targetShop.append(TargetShop(*row))
        for row in self.TARGETEMP:
            self._targetEmp.append(TargetEmp(*row))
            
    def get_employees(self): return self._employees
    def get_shifts(self): return self._shifts
    def get_sales(self): return self._sales
    def get_targetShop(self): return self._targetShop
    def get_targetEmp(self): return self._targetEmp
        
class Schedule:
    """"""
    def __init__(self) -> None:
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._numbOfConflicts1 = 0
        self._numbOfConflicts2 = 0
        self._numbOfConflicts3 = 0
        self._numbOfConflicts4 = 0
        self._numbOfConflicts5 = 0
        self._numbOfConflicts6 = 0
        self._numbOfConflicts7 = 0
        self._numbOfConflicts8 = 0
        self._numbOfConflicts9 = 0
        self._numbOfConflicts10 = 0
        self._numbOfConflicts11 = 0
        self._fitness = -1
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self): return self._numbOfConflicts
    def get_numbOfConflicts1(self): return self._numbOfConflicts1
    def get_numbOfConflicts2(self): return self._numbOfConflicts2
    def get_numbOfConflicts3(self): return self._numbOfConflicts3
    def get_numbOfConflicts4(self): return self._numbOfConflicts4
    def get_numbOfConflicts5(self): return self._numbOfConflicts5
    def get_numbOfConflicts6(self): return self._numbOfConflicts6
    def get_numbOfConflicts7(self): return self._numbOfConflicts7
    def get_numbOfConflicts8(self): return self._numbOfConflicts8
    def get_numbOfConflicts9(self): return self._numbOfConflicts9
    def get_numbOfConflicts10(self): return self._numbOfConflicts10
    def get_numbOfConflicts11(self): return self._numbOfConflicts11
    def get_fitness(self):
        if self._isFitnessChanged == True:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        days = df_workShiftsMonth.day.sort_values().drop_duplicates().tolist();shifts = df_workShiftsMonth.drop(columns='day').sort_values('id').drop_duplicates()
        ids=shifts.id.tolist();names=shifts.shiftName.tolist();froms=shifts.shiftFrom.tolist();tos=shifts.shiftTo.tolist()
        for day in days:
            rnd_chunks = random_chunks(self._data.get_employees(),n=9,max_drop=2,first_limit=8,last_limit=5)
            newClass = Class(day, ids, names, froms, tos)
            newClass.set_Employees(rnd_chunks)
            self._classes.append(newClass)
        return self
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        df = pd.DataFrame(columns=['day','id', 'shiftName', 'shiftFrom', 'shiftTo', 'employees'])
        for c in classes:
            new_classes = list(zip(c.get_ids(), c.get_shiftNames(), c.get_shiftFroms(), c.get_shiftTos(), c.get_Employees()))
            temp = pd.DataFrame(new_classes, columns=['id', 'shiftName', 'shiftFrom', 'shiftTo', 'employees'])
            temp['day'] = c.get_day()
            df = pd.concat([df, temp])
        df = df.explode('employees')
        df['EmployeeCode'] = df.employees.apply(lambda x: x.get_EmployeeCode() if x == x else x)
        df['JobTitleName'] = df.employees.apply(lambda x: x.get_JobTitleName() if x == x else x)
        df['Level'] = df.employees.apply(lambda x: x.get_level() if x == x else x)
        df['hour'] = df[['shiftFrom','shiftTo']].apply(tuple,axis=1).apply(lambda x: range(x[0],x[1]+1))
        df = df.explode('hour')
        self._numbOfConflicts += (df.groupby(['day','hour']).agg(levels=('Level', pd.Series.nunique)).levels < 3).sum() ## kiem tra nhan su level 1, level 2, level 3
        self._numbOfConflicts1 += (df.groupby(['day','hour']).agg(levels=('Level', pd.Series.nunique)).levels < 3).sum() ## kiem tra nhan su level 1, level 2, level 3
        df_managers = df[df.JobTitleName.isin(['Trưởng Quản lý Nhà Thuốc','Phó quản lý Nhà Thuốc'])]
        self._numbOfConflicts += (df_managers.groupby('day').agg(hours=('hour', pd.Series.nunique)).hours < 16).sum() ### kiem tra co it nhat 1 quan ly / pho quan ly
        self._numbOfConflicts2 += (df_managers.groupby('day').agg(hours=('hour', pd.Series.nunique)).hours < 16).sum() ### kiem tra co it nhat 1 quan ly / pho quan ly
        max_days = df.day.max()
        self._numbOfConflicts += (df.groupby('EmployeeCode').agg(days=('day', pd.Series.nunique)).days < max_days - 1).sum() ### kiem tra 1 nhan vien nghi toi da 1 ngay trong thang
        self._numbOfConflicts3 += (df.groupby('EmployeeCode').agg(days=('day', pd.Series.nunique)).days < max_days - 1).sum() ### kiem tra 1 nhan vien nghi toi da 1 ngay trong thang
        df = df.merge(df_salesEmpLv, on=['day','hour','Level'], how='left')
        df_shiftEmps = df.groupby(['day','hour','minEmployees'], as_index=False).agg(employees=('EmployeeCode', pd.Series.nunique))
        self._numbOfConflicts += ((df_shiftEmps.employees < df_shiftEmps.minEmployees)&(~df_shiftEmps.minEmployees.isnull())&(~df_shiftEmps.employees.isnull())).sum() # kiem tra 1 khung gio co toi thieu nhan su
        self._numbOfConflicts4 += ((df_shiftEmps.employees < df_shiftEmps.minEmployees)&(~df_shiftEmps.minEmployees.isnull())&(~df_shiftEmps.employees.isnull())).sum()  # kiem tra 1 khung gio co toi thieu nhan su
        df_shiftTargetEmp = df.groupby('EmployeeCode', as_index=False).agg(
            est_total_amount=('avg_total_amount','sum'),
            est_hot_amount=('avg_hot_amount','sum'),
            est_candate_amount=('avg_candate_amount','sum')
            ).merge(df_targetEmp, on='EmployeeCode', how='inner')
        self._numbOfConflicts += (df_shiftTargetEmp.est_total_amount < df_shiftTargetEmp.TargetDoanhSo).sum() ## kiem tra target nhan vien - doanh so
        self._numbOfConflicts5 += (df_shiftTargetEmp.est_total_amount < df_shiftTargetEmp.TargetDoanhSo).sum() ## kiem tra target nhan vien - doanh so
        self._numbOfConflicts += (df_shiftTargetEmp.est_hot_amount < df_shiftTargetEmp.TargetHangHot).sum() ## kiem tra target nhan vien - hang hot
        self._numbOfConflicts6 += (df_shiftTargetEmp.est_hot_amount < df_shiftTargetEmp.TargetHangHot).sum() ## kiem tra target nhan vien - hang hot
        self._numbOfConflicts += (df_shiftTargetEmp.est_candate_amount < df_shiftTargetEmp.TargetCanDate).sum() ## kiem tra target nhan vien - can date
        self._numbOfConflicts7 += (df_shiftTargetEmp.est_candate_amount < df_shiftTargetEmp.TargetCanDate).sum() ## kiem tra target nhan vien - can date
        self._numbOfConflicts += 1 if df.avg_total_amount.sum() < df_targetShop.chitieudtthang[0] else 0 ## kiem tra target shop - doanh so
        self._numbOfConflicts8 += 1 if df.avg_total_amount.sum() < df_targetShop.chitieudtthang[0] else 0 ## kiem tra target shop - doanh so
        self._numbOfConflicts += 1 if df.avg_hot_amount.sum() < df_targetShop.chitieudoanhsohotthang[0] else 0 ## kiem tra target shop - hang hot
        self._numbOfConflicts9 += 1 if df.avg_hot_amount.sum() < df_targetShop.chitieudoanhsohotthang[0] else 0 ## kiem tra target shop - hang hot
        self._numbOfConflicts += 1 if df.avg_candate_amount.sum() < df_targetShop.targetcandate[0] else 0 ## kiem tra target shop - can date
        self._numbOfConflicts10 += 1 if df.avg_candate_amount.sum() < df_targetShop.targetcandate[0] else 0 ## kiem tra target shop - can date
        self._numbOfConflicts += 1 if df.avg_dose_amount.sum() < df_targetShop.targetcatlieu[0] else 0 ## kiem tra target shop - catlieu
        self._numbOfConflicts11 += 1 if df.avg_dose_amount.sum() < df_targetShop.targetcatlieu[0] else 0 ## kiem tra target shop - catlieu
        
        return 1 / (1.0*self._numbOfConflicts + 1)
    def __str__(self):
        classes = self._classes
        finalList = []
        for c in classes:
            day = c.get_day()
            shifts = c.get_ids()
            employees = c.get_Employees()
            zipped = [f'({tup[0]}:{len(tup[1])})' for tup in zip(shifts, employees) if len(tup[1]) > 0]
            finalList.append(str(day)+':['+','.join(zipped)+']')
        return ', '.join(finalList)

class Population:
    """"""
    def __init__(self, size:int):
        self._size = size
        self._data = data
        self._schedules = []
        for _ in range(0, size):
            self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules

class GeneticAlgorithm:
    """"""
    def evolve(self, population:Population): return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop:Population):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population:Population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1:Schedule, schedule2:Schedule):
        crossoverSchedule = Schedule().initialize()
        if rnd.random() > 0.5: crossoverSchedule.get_classes = schedule1.get_classes
        else: crossoverSchedule.get_classes = schedule2.get_classes
        return crossoverSchedule
    def _mutate_schedule(self, mutateSchedule:Schedule):
        schedule = Schedule().initialize()
        if MUTATION_RATE > rnd.random(): mutateSchedule.get_classes = schedule.get_classes
        return mutateSchedule
    def _select_tournament_population(self, pop:Population):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop

class Employees:
    """"""
    def __init__(self, EmployeeCode, EmployeeName, JobTitleName, Level):
        self._EmployeeCode = EmployeeCode
        self._EmployeeName = EmployeeName
        self._JobTitleName = JobTitleName
        self._level = Level
    
    def get_EmployeeCode(self): return self._EmployeeCode
    def get_EmployeeName(self): return self._EmployeeName
    def get_JobTitleName(self): return self._JobTitleName
    def get_level(self): return self._level

class Shifts:
    """"""
    def __init__(self, day, id, shiftName, shiftFrom, shiftTo):
        self._day = day
        self._id = id
        self._shiftName = shiftName
        self._shiftFrom = shiftFrom
        self._shiftTo = shiftTo

    def get_day(self): return self._day
    def get_id(self): return self._id 
    def get_shiftName(self): return self._shiftName
    def get_shiftFrom(self): return self._shiftFrom 
    def get_shiftTo(self): return self._shiftTo

class Sales:
    """"""
    def __init__(self, day, hour, level, avg_total_amount, avg_hot_amount, avg_dose_amount, avg_candate_amount, minEmployees):
        self._day = int(day)
        self._hour = int(hour)
        self._level = int(level)
        self._avg_total_amount = round(avg_total_amount, 2)
        self._avg_hot_amount = round(avg_hot_amount, 2)
        self._avg_dose_amount = round(avg_dose_amount, 2)
        self._avg_candate_amount = round(avg_candate_amount, 2)
        self._minEmployees = int(minEmployees)

    def get_day(self): return self._day
    def get_hour(self): return self._hour
    def get_level(self): return self._level
    def get_avg_total_amount(self): return self._avg_total_amount
    def get_avg_hot_amount(self): return self._avg_hot_amount
    def get_avg_dose_amount(self): return self._avg_dose_amount
    def get_avg_candate_amount(self): return self._avg_candate_amount
    def get_minEmployees(self): return self._minEmployees

class TargetShop:
    """"""
    def __init__(self, shopCode, monthYear, targetDoanhSo, targetHangHot, targetCatLieu, targetCanDate):
        self._shopCode = shopCode
        self._monthYear = monthYear
        self._targetDoanhSo = targetDoanhSo
        self._targetHangHot = targetHangHot
        self._targetCatLieu = targetCatLieu
        self._targetCanDate = targetCanDate
    
    def get_shopCode(self): return self._shopCode
    def get_monthYear(self): return self._monthYear
    def get_targetDoanhSo(self): return self._targetDoanhSo
    def get_targetHangHot(self): return self._targetHangHot
    def get_targetCatLieu(self): return self._targetCatLieu
    def get_targetCanDate(self): return self._targetCanDate

class TargetEmp:
    """"""
    def __init__(self, employeeCode, shopCode, monthYear, targetDoanhSo, targetCanDate, targetHangHot):
        self._employeeCode = employeeCode
        self._shopCode = shopCode
        self._monthYear = monthYear
        self._targetDoanhSo = targetDoanhSo
        self._targetHangHot = targetHangHot
        self._targetCanDate = targetCanDate
    
    def get_employeeCode(self): return self._employeeCode
    def get_shopCode(self): return self._shopCode
    def get_monthYear(self): return self._monthYear
    def get_targetDoanhSo(self): return self._targetDoanhSo
    def get_targetHangHot(self): return self._targetHangHot
    def get_targetCanDate(self): return self._targetCanDate

class Class:
    """"""
    def __init__(self, day:int, ids:list, shiftNames:list, shiftFroms:list, shiftTos:list):
        self._day = day
        self._ids = ids
        self._shiftNames = shiftNames
        self._shiftFroms = shiftFroms
        self._shiftTos = shiftTos
        self._Employees = None
    def get_day(self): return self._day
    def get_ids(self): return self._ids
    def get_shiftNames(self): return self._shiftNames
    def get_shiftFroms(self): return self._shiftFroms
    def get_shiftTos(self): return self._shiftTos
    def get_Employees(self): return self._Employees
    def set_Employees(self, Employees): self._Employees = Employees
    def __str__(self):
        shifts = self.get_shiftNames()
        employees = [[e.get_EmployeeCode() for e in el] for el in self.get_Employees()]
        zipped = [tup[0]+':'+str(tup[1]) for tup in zip(shifts, employees)]
        returnValue = ', '.join(zipped)
        return returnValue

class DisplayMgr:
    def print_available_data(self):
        print('> All Available Data')
        self.print_employees()
        self.print_shifts()
        self.print_sales()
        self.print_targetShop()
        self.print_targetEmp()
    def print_employees(self):
        employees = data.get_employees()
        availableEmpTable = prettytable.PrettyTable(['employeeCode', 'employeeName', 'jobTitleName', 'level'])
        for i in range(len(employees)):
            row = employees.__getitem__(i)
            availableEmpTable.add_row([row.get_EmployeeCode(),row.get_EmployeeName(),row.get_JobTitleName(),row.get_level()])
        print('\n> Employees')
        print(availableEmpTable)
    def print_shifts(self):
        availableShiftTable = prettytable.PrettyTable(['day', 'id','shiftName', 'shiftFrom', 'shiftTo'])
        shifts = data.get_shifts()
        for i in range(10): #len(shifts)
            row = shifts.__getitem__(i)
            availableShiftTable.add_row([row.get_day(),row.get_id(),row.get_shiftName(),row.get_shiftFrom(),row.get_shiftTo()])
        print('\n> Shifts Info')
        print(availableShiftTable)
    def print_sales(self):
        availableHourTable = prettytable.PrettyTable(['day','hour','level','avg_total_amount','avg_hot_amount','avg_dose_amount','avg_candate_amount','minEmployees'])
        sales = data.get_sales()
        for i in range(10): #len(sales)
            row = sales.__getitem__(i)
            availableHourTable.add_row([row.get_day(),row.get_hour(),row.get_level(),row.get_avg_total_amount(),row.get_avg_hot_amount(),row.get_avg_dose_amount(),row.get_avg_candate_amount(),row.get_minEmployees()])
        print('\n> Last Month Sales Sample')
        print(availableHourTable)
    def print_targetShop(self):
        availabelTargetShop = prettytable.PrettyTable(['shop_code','monthYear','targetDoanhSo','targetHangHot','targetCatLieu','targetCanDate'])
        targetShop = data.get_targetShop()
        for i in range(len(targetShop)):
            row = targetShop.__getitem__(i)
            availabelTargetShop.add_row([row.get_shopCode(),row.get_monthYear(),row.get_targetDoanhSo(),row.get_targetHangHot(),row.get_targetCatLieu(),row.get_targetCanDate()])
        print('\n> Target Shop')
        print(availabelTargetShop)
    def print_targetEmp(self):
        availabelTargetEmp = prettytable.PrettyTable(['EmployeeCode','shop_code','monthYear','TargetDoanhSo','TargetCanDate','TargetHangHot'])
        targetEmp = data.get_targetEmp()
        for i in range(len(targetEmp)):
            row = targetEmp.__getitem__(i)
            availabelTargetEmp.add_row([row.get_employeeCode(),row.get_shopCode(),row.get_monthYear(),row.get_targetDoanhSo(),row.get_targetCanDate(),row.get_targetHangHot()])
        print('\n> Target Employees')
        print(availabelTargetEmp)
    def print_generation(self, population:Population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'conflicts details']) #, 'scheduling [day:(shift,employees)]'
        schedules = population.get_schedules()
        for i, row in enumerate(schedules[:1]):
            conflicts = [
                row.get_numbOfConflicts1(),row.get_numbOfConflicts2(),row.get_numbOfConflicts3(),row.get_numbOfConflicts4(),
                row.get_numbOfConflicts5(),row.get_numbOfConflicts6(),row.get_numbOfConflicts7(),
                row.get_numbOfConflicts8(),row.get_numbOfConflicts9(),row.get_numbOfConflicts10(),row.get_numbOfConflicts11()
            ]
            table1.add_row([str(i), round(row.get_fitness(), 3), row.get_numbOfConflicts(), conflicts]) #, row
        print(table1)
    def print_schedule_as_table(self, schedule:Schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['day', 'id','shiftName', 'shiftFrom', 'shiftTo', 'EmployeeCode', 'EmployeeName', 'JobTitleName', 'Level'])
        for _class in classes:
            day = _class.get_day()
            ids = _class.get_ids()
            shiftNames = _class.get_shiftNames()
            shiftFroms = _class.get_shiftFroms()
            shiftTos = _class.get_shiftTos()
            employees = _class.get_Employees()
            for shift in zip(ids,shiftNames,shiftFroms,shiftTos,employees):
                for emp in shift[4]:
                    table.add_row([
                        day,
                        shift[0],
                        shift[1],
                        shift[2],
                        shift[3],
                        emp.get_EmployeeCode(),
                        emp.get_EmployeeName(),
                        emp.get_JobTitleName(),
                        emp.get_level()
                    ])
        print(table)

data = Data()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generationNumber = 0
print('\n> Generation # ' + str(generationNumber))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
geneticAlgorithm = GeneticAlgorithm()
while population.get_schedules()[0].get_fitness() != 1.0:
    generationNumber += 1
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    print("\n> Generation # " + str(generationNumber)) 
    displayMgr.print_generation(population)
else:
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
print('\n\n')