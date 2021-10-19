import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, math

class Place:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def distToPlace(self, place):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = math.radians(self.x)
        lon1 = math.radians(self.y)
        lat2 = math.radians(place.x)
        lon2 = math.radians(place.y)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        dist = R * c

        return dist

class Route:
    def __init__(self, arrayPlaces) -> None:
        self.places = arrayPlaces

    def CalcDistance(self):
        totalDist = 0
        
        for i in range(0, len(self.places)-1):
            sPlace = self.places[i]
            tPlace = self.places[i + 1]
            totalDist += sPlace.distToPlace(tPlace)
        
        return totalDist
    
class GeneticAlgorithm:
    def __init__(self, generation) -> None:
        self.firstGeneration = generation
        self.avaliation = None
    
    def RankPop(self, pop):
        results = {}
        for index, ind in enumerate(pop):
            results[index] = 1 / float(Route(ind).CalcDistance())
        return sorted(results.items(), key = operator.itemgetter(1), reverse = True)


    def OrderParentsIndex(self, rankedPop, eliteSize):
        selectionResults = []
        df = pd.DataFrame(np.array(rankedPop), columns=["Index","Value"])
        df['cum_sum'] = df.Value.cumsum()
        df['cum_perc'] = 100*df.cum_sum/df.Value.sum()

        for i in range(0, eliteSize):
            selectionResults.append(rankedPop[i][0])
        for i in range(0, len(rankedPop) - eliteSize):
            pick = 100*random.random()
            for i in range(0, len(rankedPop)):
                if pick <= df.iat[i,3]:
                    selectionResults.append(rankedPop[i][0])
                    break

        return selectionResults

    def OrderParents(self, pop, selectionResults):
        parents = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            parents.append(pop[index])
        return parents


    def Permutate(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []
        
        childP1.append(parent1[0])    
        childP1.extend(parent1[1:int(len(parent1)/2)])    
        childP2 = [item for item in parent2 if item not in childP1]
        childP2.append(parent1[0])    
        child = childP1 + childP2 
        return child


    def GenerateChildren(self, parents, eliteSize):
        children = []
        length = len(parents) - eliteSize
        pool = random.sample(parents, len(parents))

        for i in range(0,eliteSize):
            children.append(parents[i])
        
        for i in range(0, length):
            child = self.Permutate(pool[i], pool[len(parents)-i-1])
            children.append(child)
            # print(child)
        return children


    def Mutate(self, being, mutationRate):
        for gene1 in range(1,len(being)-1):
            if(random.random() < mutationRate):
                gene2 = random.randint(1, len(being)-2)
                temp = being[gene2]
                being[gene2] = being[gene1] 
                being[gene1] = temp
        return being


    def MutatePopulation(self, population, mutationRate):
        mutatedPop = []
        
        for ind in range(0, len(population)):
            mutatedBeing = self.Mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedBeing)
        return mutatedPop


    def nextGeneration(self, curGen, eliteSize, mutationRate):
        popRanked = self.RankPop(curGen)
        self.selectionResults = self.OrderParentsIndex(popRanked, eliteSize)
        listParents = self.OrderParents(curGen, self.selectionResults)
        listChildren = self.GenerateChildren(listParents, eliteSize)
        nextGeneration = self.MutatePopulation(listChildren, mutationRate)
        return nextGeneration

    def Start(self, pop, popSize, eliteSize, mutationRate, generations):
        pop = CreateFirstGeneration(popSize, pop)
        print("Initial distance: " + str(1 / self.RankPop(pop)[0][1]))
        
        for i in range(0, generations):
            pop = self.nextGeneration(pop, eliteSize, mutationRate)
        
        print("Final distance: " + str(1 / self.RankPop(pop)[0][1]))
        bestRouteIndex = self.RankPop(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        return bestRoute

def createRoute(placeList):
    route = []
    route.append(placeList[0])
    route.extend(random.sample(placeList[1:], len(placeList)-1))
    route.append(placeList[0]) 

    return route

def CreateFirstGeneration(popSize, placeList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(placeList))
    return population


if __name__ == "__main__":
    medicalInstitutions = {}

    medicalInstitutions = {
        "Cemepar": (-25.44456697, -49.24101723),
        "Parque Barigui": (-25.42358719, -49.30617610),
        "US Vila Diana": (-25.36778846, -49.26880802),
        "US Bom Pastor": (-25.41346182, -49.30138085),
        "US Santa Quitéria I": (-25.46163685, -49.31665832),
        "US Fanny-Lindoia": (-25.47855365, -49.27271154),
        "Hospital Monastier": (-25.49731089, -49.22737201),
        "US Cajuru": (-25.45202173, -49.21754306),
        "US Sao Miguel": (-25.48016583, -49.33679080),
        "US Sao Joao Del Rey": (-25.53744581, -49.27329490),
        "US Moradias Santa Rita": (-25.56611241, -49.33346267)
    }


    cityList = []
    for mi in medicalInstitutions:
        cityList.append(Place(mi, x=medicalInstitutions[mi][0], y=medicalInstitutions[mi][1]))

    firstRoute = createRoute(cityList)

    bestRoute = GeneticAlgorithm(firstRoute).Start(pop=firstRoute, popSize=100, eliteSize=20, mutationRate=0.05, generations=500)
    print([b.name for b in bestRoute])

    bestRoute = GeneticAlgorithm(firstRoute).Start(pop=firstRoute, popSize=100, eliteSize=20, mutationRate=0.05, generations=500)
    print([b.name for b in bestRoute])

    bestRoute = GeneticAlgorithm(firstRoute).Start(pop=firstRoute, popSize=100, eliteSize=20, mutationRate=0.05, generations=500)
    print([b.name for b in bestRoute])




