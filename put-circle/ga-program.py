import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from decimal import Decimal

#変数の定義
N=7         #小さい円の数
r=0.3       #小さい円の半径

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

#n_gene = N*2
n_gene = N
min_ind = numpy.ones(n_gene) * -1.0
max_ind = numpy.ones(n_gene) *  1.0
list_individual=[]
list_eval=[]

#座標を作成
def create_ind_uniform(min_ind, max_ind):
    ind = []        #[x1,y1,x2,y2,x3,y3]
    for min, max in zip(min_ind, max_ind):
        x = random.uniform(min+r, max-r)
        y = random.uniform(min+r, max-r)
        ind.append(x)
        ind.append(y)
    return ind
    
toolbox.register("create_ind", create_ind_uniform, min_ind, max_ind)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_ind)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数
def evalOneMax(individual):
    ovarlapped_area=[]
    
    for i in range(0,len(individual),2):
        if(1<=numpy.sqrt(individual[i]*individual[i]+individual[i+1]*individual[i+1])+r):
            ovarlapped_area.append(100)
        for j in range(i,len(individual),2):
            x1=individual[i]
            y1=individual[i+1]
            if (j+2>=len(individual)):
                break
            else:
                x2=individual[j+2]
                y2=individual[j+3]
            x=numpy.sqrt((x2-x1)**2+(y2-y1)**2)/2
            angle = numpy.arccos(x/r)
            y=r*numpy.sin(angle)
            ovarlapped_area.append(numpy.pi * r*r + angle / 2*numpy.pi-x*y/2)
    return sum([n for n in ovarlapped_area if numpy.isnan(n)!=True]),
    
def cxTwoPointCopy(ind1, ind2):
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()
        
    return ind1, ind2

def mutUniformDbl(individual, min_ind, max_ind, indpb):
    size = len(individual)
    for i, min, max  in zip(range(0,size,2), min_ind, max_ind):
        if random.random() < indpb:
            x=random.uniform(min+r, max-r)
            y=random.uniform(min+r, max-r)
            individual[i]=x
            individual[i+1]=y
            while True:
               x=random.uniform(min, max)
               y=random.uniform(min, max)
               if (1>(numpy.sqrt(x*x+y*y)+r)):
                   individual[i]=x
                   individual[i+1]=y
                   break
    #print(individual)
    #list_individual.append(individual)
    #eval_value=evalOneMax(individual)
    #print(eval_value)
    #list_eval.append(eval_value)
    return individual,
    
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", cxTwoPointCopy)
#toolbox.register("mutate", mutUniformDbl, min_ind=min_ind, max_ind=max_ind, indpb=0.05)
toolbox.register("mutate", mutUniformDbl, min_ind=min_ind, max_ind=max_ind, indpb=0.60)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
       
    pop = toolbox.population(n=300)
    
    hof = tools.HallOfFame(1, similar=numpy.array_equal)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    num_gene=30000
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.4, ngen=num_gene, stats=stats,halloffame=hof)
    #algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=1, stats=stats,halloffame=hof)

    #individual_min=[]       #評価値が一番低い時の座標
    #eval_value_min=10000    #最小の評価値
    #評価値が一番低い座標と評価値を出力する
    #for i in range(num_gene-100,num_gene):
    '''
    for i in range(num_gene):
        eval_value = str(evalOneMax(list_individual[i]))
        eval_value = Decimal(eval_value[1:-2])
        if(eval_value < eval_value_min):
            eval_value_min=eval_value
            individual_min=list_individual[i]
    '''    
    #print(individual_min)
    #print(eval_value_min)

    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof=main()
    print(hof)
    