import csv

f = open('recipes.csv')
input_file = list(csv.DictReader(f))
for row in input_file:
    if 'flour' in row.values():
        row['Allergen100'] = 'Gluten'
f.close()

f = open('testing.csv', 'w')
output_file = csv.DictWriter(f, input_file[0].keys())
output_file.writeheader()
output_file.writerows(input_file)
f.close()