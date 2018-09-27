import random
from abc import ABC, abstractmethod
from copy import copy, deepcopy


class Gene(ABC):
    def __repr__(self):
        return str(self.value)

    @abstractmethod
    def init_value(self):
        pass

    @abstractmethod
    def mutate(self):
        pass

    @classmethod
    @abstractmethod
    def crossover(cls, one, other):
        pass


class FloatGene(Gene):
    GAUSS_SIGMA_MULTIPLIER = 1 / 6
    BLX_ALPHA = 0.1

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
        self.init_value()

    def init_value(self):
        self.value = random.uniform(self.min_value, self.max_value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._clip()

    def _clip(self):
        self._value = min(self.max_value, self._value)
        self._value = max(self.min_value, self._value)

    def mutate(self):
        stdev = (self.max_value - self.min_value) * self.GAUSS_SIGMA_MULTIPLIER
        mutation = random.gauss(0, stdev)
        self.value += mutation

    def _blend_value(self, other):
        """Implements BLX-alpha crossover."""
        interval = abs(self.value - other.value)
        lower = min(self.value, other.value) - self.BLX_ALPHA * interval
        upper = max(self.value, other.value) + self.BLX_ALPHA * interval

        new_value = random.uniform(lower, upper)
        return new_value

    @classmethod
    def crossover(cls, one, other):
        new = copy(one)
        new.value = one._blend_value(other)
        return new


class IntGene(FloatGene):
    @property
    def value(self):
        return super().value
        # return int(self._value)

    @value.setter
    def value(self, new_value):
        _value = int(new_value)
        super(IntGene, self.__class__).value.fset(self, _value)   # No other way to reuse parent property setter
        # self._clip()


class CategoricalGene(Gene):
    def __init__(self, categories):
        self.categories = tuple(categories)
        self.init_value()

    def init_value(self):
        self.mutate()

    def mutate(self):
        self.value = random.choice(self.categories)

    @classmethod
    def crossover(cls, one, other):
        new = copy(one)
        new.value = random.choice([one.value, other.value])
        return new


class BoolGene(CategoricalGene):
    def __init__(self):
        super().__init__([True, False])


class Genome(dict):
    def init_values(self):
        for gene in self:
            self[gene].init_value()

    def mutate(self):
        probability = 1 / len(self)
        for gene in self:
            if (random.random() / probability) < 1:
                self[gene].mutate()

    @classmethod
    def crossover(cls, one, other):
        new = deepcopy(one)
        for gene in one:
            new[gene] = one[gene].crossover(one[gene], other[gene])
        return new

    def random_copy(self):
        new = deepcopy(self)
        new.init_values()
        return new

    def fitness(self, function):
        genes_value = {key: gene.value for key, gene in self.items()}
        return function(**genes_value)

# class Genome(list):
#     def init_values(self):
#         for gene in self:
#             gene.init_value()

#     def mutate(self):
#         probability = 1 / len(self)
#         for gene in self:
#             if (random.random() / probability) < 1:
#                 gene.mutate()

#     @classmethod
#     def crossover(cls, one, other):
#         new = deepcopy(one)
#         # print(one)
#         for i, genes in enumerate(zip(one, other)):
#             new[i] = genes[0].crossover(*genes)
#         return new

#     def random_copy(self):
#         new = deepcopy(self)
#         new.init_values()
#         return new

#     def fitness(self, function):
#         genes_value = [gene.value for gene in self]
#         return function(genes_value)


class Population():
    # Bigger tournament size => increased selection pressure
    TOURNAMENT_SIZE = 5
    MUTATION_RATE = 0.2

    def __init__(self, size, genome, fitness_function=None):
        self.genomes = tuple(genome.random_copy() for _ in range(size))
        self.size = size
        self.fitness_function = fitness_function

    def __repr__(self):
        return "\n".join(repr(genome) for genome in self.genomes)

    def __len__(self):
        return len(self.genomes)

    def tournament(self):
        contestants = random.choices(self.genomes, k=self.TOURNAMENT_SIZE)
        return max(contestants, key=lambda x: x.fitness(self.fitness_function))

    def breed(self):
        parents = (self.tournament(), self.tournament())
        child = Genome.crossover(*parents)
        return child

    def crossover(self):
        children = [self.breed() for _ in range(self.size)]
        self.genomes = tuple(children)

    def mutate(self):
        for genome in self.genomes:
            if random.random() < self.MUTATION_RATE:
                genome.mutate()

    def evolve(self):
        self.crossover()
        self.mutate()

    @property
    def fitness(self):
        return sum(genome.fitness(self.fitness_function) for genome in self.genomes) / self.size

    @property
    def best(self):
        return max(self.genomes, key=lambda x: x.fitness(self.fitness_function))


# def function(x):
#     return 5 * x - 10


# def error(slope, bias):
#     return sum((function(x) - (slope * x + bias))**2 for x in range(-10, 10))


# def fitness(**kwargs):
#     return 1 / error(**kwargs)


# g = Genome(slope=FloatGene(-100, 100), bias=FloatGene(-100, 100))

# p = Population(100, g, fitness)

# for _ in range(20):
#     p.evolve()
#     print(p.fitness)
# print(p.best)

from string import printable, ascii_lowercase


objetive = "mecagoenlaba"


g = Genome([CategoricalGene(ascii_lowercase) for i in range(len(objetive))])


def fitness(guess, ground=objetive):
    score = 0
    for guess_letter, ground_letter in zip(guess, ground):
        if guess_letter == ground_letter:
            score += 1
    return score


p = Population(100, g, fitness)
i = 0
while True:
    p.evolve()
    guess = ''.join(g.value for g in p.best)
    i += 1
    print(f"Gen {i}) {guess}")
    if guess == objetive:
        break
