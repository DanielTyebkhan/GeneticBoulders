# import csv
    

# read_path = '/home/daniel/Downloads/Moonboard types - Sheet2.csv'
# save_path = 'holdtypes.csv'
# remap = []
# with open(read_path, 'r') as file:
#     reader = csv.reader(file)
#     next(reader)
#     for row in reader:
#         y = int(row[0])
#         for x, val in enumerate(row[1:]):
#             if val != '':
#                 remap.append(
#                     {
#                         'x': int(x),
#                         'y': int(y),
#                         'val': int(val)
#                     }
#                 )

# with open(save_path, 'w') as file:
#     writer = csv.DictWriter(file, ['x', 'y', 'val'])
#     writer.writeheader()
#     writer.writerows(remap)
from share.moonboard_util import HOLD_TYPES
print(HOLD_TYPES)
