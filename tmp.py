from collections import defaultdict
from csv import DictReader
from user_study.survey_response import SurveyResponse

def read_valid_results(path):
    valid_res = []
    with open(path, 'r') as file:
        reader = DictReader(file)
        next(reader)
        next(reader)
        for item in reader:
            if item['Status'] != 'Survey Preview' and item['Q6'] != '' and item['Screen 1'] == 'Yes' and item['Screen 2'] == '40':
                valid_res.append(item)
    return valid_res

path = '/home/tyebkhad/GeneticBoulders/user_study/Evolving MoonBoard Routes_February 20, 2023_20.45.csv'
valid_res = read_valid_results(path)
all_responses = [SurveyResponse(res) for res in valid_res]

from matplotlib import pyplot as plt
import matplotlib.cm as cm
from scipy.stats import pearsonr, chisquare

responses = all_responses
advanced_responses = [r for r in all_responses if r.max_climbed > 9]
for i in range(3, 13):
    resps = [r for r in all_responses if r.max_climbed > i]
    calibs = [r.perc_calibration_correct() for r in resps]
    gener = [r.perc_generated_correct() for r in resps]
    n = len(resps)
    r, p = pearsonr(calibs, gener)
    print(f'V{i+1} climbers: n={n}, r={r}, p={p}')

calibs = [r.perc_calibration_correct() for r in responses]
gener = [r.perc_generated_correct() for r in responses]

cross = list(zip(calibs, gener))
colors = {i: cross.count(i) / len(cross) for i in cross}
x_data = []
y_data = []
c_data = []
used = set()
for i in range(len(calibs)):
    x = calibs[i]
    y = gener[i]
    if (x, y) not in used:
        x_data.append(x)
        y_data.append(y)
        c_data.append(colors[(x, y)])
        used.add((x, y))


plt.xlabel('Benchmarks Correct (%)')
plt.ylabel('Generated Correct (%)')
sc = plt.scatter(x_data, y_data, c=c_data, label='Any Level', cmap=cm.get_cmap('hot'))
plt.colorbar(sc)
plt.show()