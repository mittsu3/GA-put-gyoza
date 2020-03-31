import random
import numpy
from PIL import Image

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from decimal import Decimal

#変数の定義
N=10         # 餃子の数

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
frame_height,frame_width=150,150
frame=[0]*frame_height*frame_width
gyoza_height,gyoza_width=64,64
n_gene = N
min_ind = [0]*n_gene
max_ind = [150*150]*n_gene
list_individual=[]
list_eval=[]

#基準点＆角度を作成
def create_ind_uniform(min_ind, max_ind):
    ind = []        #[point1,angle1,point2,angle2,point3,angle3,...]
    min_angle,max_angle=0,360
    for min, max in zip(min_ind, max_ind):
        x = random.randint(0, 150*150)
        angle=random.randint(min_angle,max_angle)
        ind.append(x)
        ind.append(angle)
    return ind
    
toolbox.register("create_ind", create_ind_uniform, min_ind, max_ind)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_ind)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def load_image():
    # 餃子画像の読み込み
    img_original=Image.open("gyoza.png")
    gyoza_size=[[]]
    for n in range(360):
        gyoza_size.append([])
        img=img_original.rotate(n)
        width, height = img.size
        for y in range(height):
            for x in range(width):
                color=img.getpixel((x,y))
                if(color[0]==0 and color[1]==0 and color[2]==0):
                    color=(255,255,255)
                    gyoza_size[n].append(0)
                elif(color[0]>=230 and color[1]>=230 and color[2]>=230):
                    gyoza_size[n].append(0)
                else:
                    gyoza_size[n].append(1)
    return gyoza_size

def put_gyoza(individual):
    penalty=[]
    frame_best=[0]*150*150
    for j in range(0,len(individual),2):
        try:
            row=-1
            point=individual[j]
            angle=individual[j+1]
            if(point%150>(150-64)):
                penalty.append(1000)
            for i in range(64*64):
                if(i%gyoza_height==0):
                    row+=1
                if(row==0):
                    cell_num=point-1+i
                else:
                    cell_num=row*frame_height-64*row+point-1+i
                frame_best[cell_num]+=gyoza_size[angle][i]
        except:
            penalty.append(1000)
    return frame_best,penalty

#評価関数
def evalOneMax(individual):
    frame,penalty=put_gyoza(individual)
    return sum([n for n in frame if n>=2])+sum(penalty),

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
            point=random.randint(0, 150*150)        #len(フレーム)
            angle=random.randint(0, 360)
            individual[i]=point
            individual[i+1]=angle
    return individual,
    
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", cxTwoPointCopy)
toolbox.register("mutate", mutUniformDbl, min_ind=min_ind, max_ind=max_ind, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(gyoza_size):
    random.seed(64)
       
    pop = toolbox.population(n=300)
    
    hof = tools.HallOfFame(1, similar=numpy.array_equal)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    num_gene=3
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.4, ngen=num_gene, stats=stats,halloffame=hof)
    
    return pop, stats, hof

if __name__ == "__main__":
    gyoza_size=load_image()
    pop, stats, hof=main(gyoza_size)
    list_a=hof[0]

    img2 = Image.new('RGB', (150, 150))     #フレームサイズ
    frame_best=put_gyoza(list_a)
    individual=list_a
    
    frame_best,penalty=put_gyoza(individual)
    
    #配列を基に画像に色を付ける
    for y in range(150):
        for x in range(150):
            cell=y*150+x
            if(frame_best[cell]==0):
                color=(255,255,255)
            elif(frame_best[cell]==1):
                color=(0,217,255)
            elif(frame_best[cell]>=2):
                color=(255,0,0)
            else:
                color=(0,0,0)
            img2.putpixel((x,y),color)
    img2.show()    
    print(individual)
    print('範囲外 : ',len(penalty))     #はみ出ている餃子の個数
    print('重複 : ',sum([n for n in frame_best if n>=2])+sum(penalty))      #重複している数値の合計
