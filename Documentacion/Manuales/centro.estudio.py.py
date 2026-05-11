palabra = input("Dime una palabra: ")
contador = 0
i = 0

while i < len(palabra):
    if palabra[i] == "a":
        contador = contador + 1
i = i + 1

print ("la letra a aparece", contador, "veces" )


