from utils.parser_utils import parse_yapar_file

result = parse_yapar_file('./examples/yapar/easy.yalp')

print("Terminales:", result['terminales'])
print("Grammar:")
for lhs, prods in result['grammar'].items():
    for prod in prods:
        print(f"{lhs} -> {' '.join(prod)}")