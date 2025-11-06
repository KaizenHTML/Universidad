def Sum(n):
    
    if n == 0:
        return 0

    else:
     
        LastDigit= n % 10
        
        RestNumber = n // 10
        
        # Sumando último dígito + la suma de los dígitos restantes 
        return LastDigit + Sum(RestNumber)

# Entrada
NumberUser = int(input('Ingrese un número entero: '))

Result = Sum(NumberUser)

print(f"El número es: {NumberUser}")

print(f"La suma de sus dígitos es: {Result}") 

