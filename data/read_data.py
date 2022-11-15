import json

with open('ingredients.json', 'r') as f:
    data = json.load(f)


# Collect measurement unit data
uom = set()
for i in data:
    uom.add(i['measurement_unit'])

# Collect data {'measurement_unit': ['name', ...]}
uom_product = {}
for i in data:
    if i['measurement_unit'] in uom_product:
        uom_product[i['measurement_unit']].append(i['name'])
    else:
        uom_product[i['measurement_unit']] = [i['name']]

print(uom)

print(uom_product)
