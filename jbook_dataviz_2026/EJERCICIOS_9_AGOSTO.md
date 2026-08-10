
# Ejercicio 1

```python
import numpy as np

n = 10

def factorial(n):
    resultado = 1

    for i in range(1, n + 1):
        resultado = resultado * i

    return resultado

factorial(n)
```

**Resultado:**

```text
3628800
```

```python
V1 = np.random.randint(1, 11, n)
V2 = np.random.randint(1, 11, n)

print(V1)
print(V2)
```

**Ejemplo de resultado obtenido:**

```text
[1 1 4 2 4 5 9 10 3 9]
[3 6 4 6 7 4 2 1 5 9]
```

```python
V3 = []

for i in range(n):
    if V1[i] < V2[i]:
        V3.append(0)
    else:
        V3.append(1)

V3 = np.array(V3)

print(V3)
```

**Resultado:**

```text
[0 0 1 0 0 1 1 1 0 1]
```

```python
V1_col = V1.reshape(n, 1)
V2_col = V2.reshape(n, 1)
V3_col = V3.reshape(n, 1)

matriz = np.concatenate((V1_col, V2_col, V3_col), axis=1)

print(matriz)
```

**Resultado:**

```text
[[ 1  3  0]
 [ 1  6  0]
 [ 4  4  1]
 [ 2  6  0]
 [ 4  7  0]
 [ 5  4  1]
 [ 9  2  1]
 [10  1  1]
 [ 3  5  0]
 [ 9  9  1]]
```

## Explicación

En este ejercicio se trabajó con funciones, vectores y matrices utilizando Python y NumPy. Primero se calculó el factorial de un número mediante una función. Después se generaron dos vectores con números aleatorios y se creó un tercer vector a partir de la comparación de sus elementos, asignando 0 cuando el valor del primer vector era menor que el segundo y 1 en caso contrario. Finalmente, los tres vectores se organizaron como columnas de una misma matriz, permitiendo visualizar conjuntamente los valores originales y el resultado de cada comparación.

---

# Ejercicio 2

```python
m = 4
n = 3

A = np.zeros((m, n), dtype=int)

print(A)
```

**Resultado:**

```text
[[0 0 0]
 [0 0 0]
 [0 0 0]
 [0 0 0]]
```

```python
j = 0

while j < n:
    A[:, j] = np.random.randint(-1, 4, m)
    j = j + 1

print(A)

A_original = A.copy()
```

**Ejemplo de resultado obtenido:**

```text
[[-1  1  1]
 [ 1 -1  1]
 [ 2  2  3]
 [ 0  0  3]]
```

```python
A_while = A_original.copy()

i = 0

while i < m:
    j = 0

    while j < n:
        if A_while[i, j] < 0:
            A_while[i, j] = -1
        else:
            A_while[i, j] = 5

        j = j + 1

    i = i + 1

print(A_while)
```

**Resultado:**

```text
[[-1  5  5]
 [ 5 -1  5]
 [ 5  5  5]
 [ 5  5  5]]
```

```python
A_for = A_original.copy()

for i in range(m):
    for j in range(n):
        if A_for[i, j] < 0:
            A_for[i, j] = -1
        else:
            A_for[i, j] = 5

print(A_for)
```

**Resultado:**

```text
[[-1  5  5]
 [ 5 -1  5]
 [ 5  5  5]
 [ 5  5  5]]
```

```python
np.array_equal(A_while, A_for)
```

**Resultado:**

```text
True
```

## Explicación

En este ejercicio se creó inicialmente una matriz de ceros y posteriormente se llenó con números enteros aleatorios utilizando un ciclo `while`. A partir de la matriz original se realizó una transformación en la que los valores negativos fueron reemplazados por -1 y los valores iguales o mayores que cero por 5. Esta transformación se realizó primero utilizando ciclos `while` y luego utilizando ciclos `for`. Finalmente, se compararon las dos matrices obtenidas y el resultado `True` permitió comprobar que ambos métodos producen exactamente el mismo resultado.

---

# Ejercicio 3

```python
import pandas as pd

datos = {
    "MASA": [71, 45, 50, 60, 61, 84, 55, 60],
    "ESTATURA": [183, 168, 164, 164, 167, 182, 168, 170],
    "GENERO": ["HOMBRE", "HOMBRE", "HOMBRE", "MUJER", "HOMBRE", "HOMBRE", "MUJER", "HOMBRE"],
    "ESTRATO": [2, 1, 1, 3, 3, 3, 3, 3],
    "FUMA": ["NO", "NO", "NO", "SI", "SI", "NO", "NO", "SI"]
}

df = pd.DataFrame(datos)

df
```

**Resultado:**

| | MASA | ESTATURA | GENERO | ESTRATO | FUMA |
|---|---:|---:|---|---:|---|
| 0 | 71 | 183 | HOMBRE | 2 | NO |
| 1 | 45 | 168 | HOMBRE | 1 | NO |
| 2 | 50 | 164 | HOMBRE | 1 | NO |
| 3 | 60 | 164 | MUJER | 3 | SI |
| 4 | 61 | 167 | HOMBRE | 3 | SI |
| 5 | 84 | 182 | HOMBRE | 3 | NO |
| 6 | 55 | 168 | MUJER | 3 | NO |
| 7 | 60 | 170 | HOMBRE | 3 | SI |

```python
df.describe(include="all")
```

Con esta instrucción se obtiene el análisis descriptivo de las variables numéricas y categóricas del conjunto de datos.

```python
subc1 = df.iloc[0:4]

subc1
```

**Resultado:**

| | MASA | ESTATURA | GENERO | ESTRATO | FUMA |
|---|---:|---:|---|---:|---|
| 0 | 71 | 183 | HOMBRE | 2 | NO |
| 1 | 45 | 168 | HOMBRE | 1 | NO |
| 2 | 50 | 164 | HOMBRE | 1 | NO |
| 3 | 60 | 164 | MUJER | 3 | SI |

```python
subc2 = df[["GENERO", "FUMA"]]

subc2
```

**Resultado:**

| | GENERO | FUMA |
|---|---|---|
| 0 | HOMBRE | NO |
| 1 | HOMBRE | NO |
| 2 | HOMBRE | NO |
| 3 | MUJER | SI |
| 4 | HOMBRE | SI |
| 5 | HOMBRE | NO |
| 6 | MUJER | NO |
| 7 | HOMBRE | SI |

```python
subc3 = df[["MASA", "ESTATURA", "ESTRATO"]]

subc3
```

**Resultado:**

| | MASA | ESTATURA | ESTRATO |
|---|---:|---:|---:|
| 0 | 71 | 183 | 2 |
| 1 | 45 | 168 | 1 |
| 2 | 50 | 164 | 1 |
| 3 | 60 | 164 | 3 |
| 4 | 61 | 167 | 3 |
| 5 | 84 | 182 | 3 |
| 6 | 55 | 168 | 3 |
| 7 | 60 | 170 | 3 |

## Explicación

En este ejercicio se utilizó Pandas para organizar la información de ocho estudiantes en un DataFrame compuesto por variables numéricas y categóricas. Una vez creada la tabla se realizó un análisis descriptivo general de los datos y posteriormente se generaron diferentes subconjuntos. El primero contiene únicamente los cuatro primeros estudiantes, el segundo reúne las variables categóricas género y hábito de fumar, y el tercero contiene las variables numéricas masa, estatura y estrato. De esta manera se practicó la creación, descripción y selección de información dentro de un DataFrame.