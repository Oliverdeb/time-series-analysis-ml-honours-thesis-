from shapelets.shapelet import Shapelet
from shapelets.shapelet_utils import shapelet_utils
import time
from utils.Utils import Utils

def main():
    # shapelet_classifier = Shapelet()

    series = [float(x) for x in open('data/snp2.csv').readlines()]
    # print (series[:100])
    # exit(1)
    # a = [ (1,2), (2,5), (1,1), (1,9)]
    # b = [ (1,3)] #, (1,1), (1,15), (1,8)]
    # b.sort(key = lambda x: x[1])
    # print ('a' , [arr[1] for arr in a])
    # print ('b' , [arr[1] for arr in b])
    # k = Shapelet.merge(4, a, b)
    # print ('a' , [arr[1] for arr in a])
    # print ('b' , [arr[1] for arr in b])

    # print (k)
    t = time.time()
    series_cutoff = 1000

    _min = 12
    _max = 30
    # print ("before",series)
    # series = util.normalize(series[:series_cutoff])
    # import numpy as np
    # series = [np.log(x) for x in series[:series_cutoff]]
    series = series[:series_cutoff]
    # print ("after", series)
    sets = [series]
    k_shapelets = []
    k = 20
    for dataset in sets:
        shapelets = []
        for l in range(_min, _max + 1):            
            candidates_i_l = shapelet_utils.generate_candidates(dataset, l)
            prog = len(candidates_i_l)

            print ("Checking candidates of length %d, %d candidates" % (l, prog))
            for i,w in enumerate(candidates_i_l):
                if i % 11 ==0 :
                    print ("\r%.2f" % (i/prog), end="")
                all_mse = shapelet_utils.find_mse(w, candidates_i_l)
                all_mse.sort()
                w.quality = sum ( all_mse[:6])
                shapelets.append( w )
        print()
        # shapelets = shapelet_utils.remove_all_similar(shapelets, (_min + _max) / 4.0)
        shapelets.sort(key = lambda x: x.quality)
        k_shapelets = shapelet_utils.merge(k_shapelets, shapelets)
    
    print ("%.2fs elapsed\n%d shapelets found" % (time.time() -t, len(k_shapelets)))
    shapelet_utils.graph(series[:series_cutoff], k_shapelets[:k])



if __name__ == '__main__':  
    main()
    exit(1)
    print('\n===== POINTS =====')
    points = Utils.read_file('data/snp2.csv')
    print(len(points))

    points = Utils.moving_average(points)
    print(len(points))
    Utils.print_array(points)

    print('\n===== LINES =====')
    lines = Utils.sliding_window_segmentation(points, 120)
    Utils.print_array(lines)
    print('\n')

    p = []
    for x in points:
        p.append(x.price)

    Utils.graph(p, lines)