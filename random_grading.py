from collections import Counter
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from MoonBoardRNN.BetaMove.BetaMove import load_feature_dict
from share.moonboard_route import MoonBoardRoute
import json
from matplotlib import pyplot as plt

def do_counts(num_runs, save_path):
    gnet = GradeNet()
    feature_dict = load_feature_dict()
    counter = Counter()
    for i in range(num_runs):
        if i % 1000 == 0:
            print(f'At iteration {i}')
        route = MoonBoardRoute.make_random_valid()
        grade = gnet.grade_route(route, feature_dict)
        counter.update([grade])
    json.dump(counter, open(save_path, 'w'))

def plot_counts(counts_path, save_path):
    counts = json.load(open(counts_path, 'r'))
    x = []
    y = []
    for k in counts:
        x.append(k)
        y.append(counts[k])
    plt.bar(x, y) 
    plt.xlabel('Grade')
    plt.ylabel('Number of Routes')
    plt.savefig(save_path)


    

if __name__ == '__main__':
    plot_counts('counts.json', 'counts.png')