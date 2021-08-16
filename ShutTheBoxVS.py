import ShutTheBox
import json

file = open('stbAI.json')
pi = json.load(file)
file.close()

print("Der Zufall bietet an:")
print(ShutTheBox.simulation([1], 100000, 1, 1))
print("")
print("---------------------")
print("")
print("Elisa bietet an:")
print(ShutTheBox.simulation([1], 100000, 2, 1))
print("")
print("---------------------")
print("")
print("Die AI bietet an:")
print(ShutTheBox.simulation([1], 100000, 3, 1))
print("")
print("---------------------")
print("")
print("Florian bietet an:")
print(ShutTheBox.simulation([1], 100000, 4, 1))