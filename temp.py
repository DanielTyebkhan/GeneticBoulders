import csv

with open('coords.txt', 'w') as coordfile:
    coordfile.write('[')
    with open('/home/daniel/GeneticBoulders/MoonBoardRNN/BetaMove/HoldFeature2016.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            coordfile.write(f"({row['X_coord']}, {row['Y_coord']}),")

    coordfile.write(']')

    