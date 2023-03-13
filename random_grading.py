from MoonBoardRNN.GradeNet.grade_net import GradeNet
from MoonBoardRNN.BetaMove.BetaMove import load_feature_dict
from share.moonboard_route import MoonBoardRoute
import pickle
from matplotlib import pyplot as plt
from collections import defaultdict

def do_counts(num_runs, save_path):
    routes = defaultdict(list)
    gnet = GradeNet()
    feature_dict = load_feature_dict()
    for i in range(num_runs):
        if i % 1000 == 0:
            print(f'At iteration {i}')
        route = MoonBoardRoute.make_random_valid()
        grade = gnet.grade_route(route, feature_dict)
        routes[grade].append(route)
    pickle.dump(routes, open(save_path, 'wb'))

def plot_counts(counts_path, save_path):
    counts = pickle.load(open(counts_path, 'rb'))
    x = []
    y = []
    for k in counts:
        x.append(k)
        y.append(len(counts[k]))
    plt.bar(x, y) 
    plt.xlabel('Grade')
    plt.ylabel('Number of Routes')
    plt.savefig(save_path)


    

if __name__ == '__main__':
    do_counts(10_000, 'counts.P')