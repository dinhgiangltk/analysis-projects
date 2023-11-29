from population import Population, Schedule
import random as rnd

NUMB_OF_ELITE_SCHEDULES = 2
TOURNAMENT_SELECTION_SIZE = 3
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.1

class GeneticAlgorithm:
    """
    This class contains the whole process of genetic algorithm for work shift scheduling.
    ### Method
    - `evolve`
    - `crossover_population`
    - `mutate_population`
    - `select_tournament_population`
    - `crossover_schedule`
    - `mutate_schedule`
    """
    
    def evolve(self, pop:Population):
        """
        This function returns a new generation of population.
        ### Parameter
        `pop`: `Population`, `required`
        """
        return self.mutate_population(self.crossover_population(pop))
 
    def crossover_population(self, pop:Population, elitism=NUMB_OF_ELITE_SCHEDULES):
        """
        This function forms a new population after crossover process.
        ### Paremeter
        `pop`: `Population`, `required` \n
        `elitism`: `optional`, default `NUMB_OF_ELITE_SCHEDULES`
            The number of elite individuals that are first selected
        """
        population_size = pop.size
        crossover_pop = Population(size=0)
        initialize_schedules = sorted(pop.get_schedules(), key=lambda x: x.get_fitness(), reverse=True)
        for i in range(elitism):
            crossover_pop.get_schedules().append(initialize_schedules[i])

        for _ in range(elitism, population_size):
            schedule1 = self.select_tournament_population(pop).get_schedules()[0]
            schedule2 = self.select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self.crossover_schedule(schedule1, schedule2))
            
        return crossover_pop
    
    def mutate_population(self, pop:Population, elitism=NUMB_OF_ELITE_SCHEDULES):
        """
        This function forms a new population after mutation process.
        ### Paremeter
        `pop`: `Population`, `required` \n
        `elitism`: `optional`, default `NUMB_OF_ELITE_SCHEDULES`
            The number of elite individuals that are first selected
        """
        population_size = pop.size
        for i in range(elitism, population_size):
            self.mutate_schedule(pop.get_schedules()[i])
        return pop
    
    def select_tournament_population(self, pop:Population, size=TOURNAMENT_SELECTION_SIZE):
        """
        This function randomly selects `TOURNAMENT_SELECTION_SIZE` individuals from population.
        ### Paremeter
        `pop`: `Population`, `required` \n
        `size`: `optional`, default `TOURNAMENT_SELECTION_SIZE`
            The number of individuals selected from population
        """
        tournament_pop = Population(0)
        initialize_schedules = rnd.choices(pop.get_schedules(), k=size)
        
        for i in range(size):
            tournament_pop.get_schedules().append(initialize_schedules[i])

        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
    
    def crossover_schedule(self, schedule1:Schedule, schedule2:Schedule):
        """
        This function processes the crossover between 2 individuals.
        ### Paremeter
        `schedule1`: `Schedule`, `required`
            The first parent individual
        `schedule2`: `Schedule`, `required`
            The second parent individual
        """
        crossoverSchedule = Schedule().initialize()
        for i in range(crossoverSchedule.totalShifts):
            random_number = rnd.random()
            if random_number > CROSSOVER_RATE:
                crossoverSchedule.get_arrangement()[i] = schedule1.get_arrangement()[i]
            else:
                crossoverSchedule.get_arrangement()[i] = schedule2.get_arrangement()[i]
        return crossoverSchedule
    
    def mutate_schedule(self, mutateSchedule:Schedule, mutation_rate=MUTATION_RATE):
        """
        This function processes the mutation of an individual.
        ### Paremeter
        `mutateSchedule`: `Schedule`, `required`
            The mutation individual
        """
        schedule = Schedule().initialize()
        for i in range(schedule.totalShifts):
            if mutation_rate > rnd.random():
                mutateSchedule.get_arrangement()[i] = schedule.get_arrangement()[i]
        return mutateSchedule