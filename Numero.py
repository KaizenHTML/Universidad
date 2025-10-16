def Sum_digits_recursive(N):
    
    # La recursión termina cuando el número es 0
    if N == 0:
        return 0
    
    # Caso Recursivo
    else:
     
        Last_digit= N % 10
        
        Rest_number = N // 10
        
        # La suma es el último dígito + la suma de los dígitos restantes 
        return Last_digit + Sum_digits_recursive(Rest_number)

Number_user = int(input('Ingrese un número entero: '))
Result = Sum_digits_recursive(Number_user)

print(f"El número es: {Number_user}")
print(f"La suma de sus dígitos es: {Result}") 

