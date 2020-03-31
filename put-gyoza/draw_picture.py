from PIL import Image
def load_image():
    # 餃子画像の読み込み
    img_original=Image.open("gyoza.png")
    gyoza_size=[[]]
    for n in range(360):
        gyoza_size.append([])
        img=img_original.rotate(n)
        width, height = img.size
        img_pixels = []
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
                img_pixels.append(color)
    return gyoza_size

def put_gyoza(individual,gyoza_size):
    penalty=[]
    frame_best=[0]*150*150
    gyoza_height=64
    frame_height=150

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

def main():
    #individual=[  674 ,  230 , 6002 ,  174 ,11551  , 350 ,12349 ,  337 , 6953 ,  189 ,11935  ,  68  ,   8  , 230 , 6232  , 162]   #8
    individual=[12497 ,  302 , 4712 ,   40 ,  179  , 312 ,12916  , 324  , 602  , 325  ,  63  ,   6, 11929  ,  94  ,9151 ,  267  , 236  , 183]   #9 重複なし
    #individual=[12151 ,  333 ,   75 ,  218 ,12929  ,  18 , 8035  ,   6  ,  18  , 131 , 5786  , 187 , 1351  , 314  ,4255 ,  316 , 7834  , 352, 12681 ,   26]   #10 重複あり（７６）

    gyoza_size=load_image()

    img2 = Image.new('RGB', (150, 150))
    frame_best,penalty=put_gyoza(individual,gyoza_size)
    print(frame_best)
    #配列を基に画像に色を付ける
    for y in range(150):
        for x in range(150):
            cell=y*150+x
            if(frame_best[cell]==0):
                color=(255,255,255)
            if(y==0 or y==(150-1) or x==0 or x==(150-1)):
                color=(0,0,0)
            if(frame_best[cell]==1):
                color=(0,217,255)
            if(frame_best[cell]>=2):
                color=(255,0,0)
            img2.putpixel((x,y),color)
    img2.show()
    print('範囲外 : ',len(penalty))
    print('重複ピクセル＋枠外ペナルティ : ',sum([n for n in frame_best if n>=2])+sum(penalty))

if __name__ == "__main__":
    main()