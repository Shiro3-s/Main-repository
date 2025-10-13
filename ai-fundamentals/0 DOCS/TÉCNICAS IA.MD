# TÉCNICAS MÁS UTILIZADAS 

## Definiciones de analítica de datos: 
**COLUMNAS** = Variables
**FILAS** = Observaciones

## Para Clasificación


**k-vecinos más cercanos (k-NN)**

Clasifica según la mayoría de los k vecinos más cercanos.

**Naive Bayes**

Clasificador probabilístico basado en el Teorema de Bayes

**Árboles de Decisión**

Estructura de árbol con reglas de decisión "si-entonces"

**Máquinas de Vectores de soporte (SVM)**

Busca hiperplano óptimo que separa las clases

**Regresión logística**

Modela probabilidades usando la función

## PARA REGRESIÓN

**Regresión Lineal**

Modela relación lineal entre variables dependientes e independientes

**Árboles de Desición para Regresión**

Similar a los árboles de clasificación, pero predice valores continuos.

**SVR (Support Vector Regression)**

Versión de SVM adaptada para predecir valores continuos.

**Random Forest Regressor**

Conjunto de datos de decisión para regresión

**K-Vecinos más Cercanos (k-NN)**

Algoritmo "perezoso" (no aprende, memoriza) que clasifica un nuevo punto basándose en la clase mayoritaría de sus 'k' vecinos más cercanos en el conjunto de entrenamiento.

### ¿COMO FUNCIONA?

- Elegir un valor 'k'
- Calcular distancias entre el nuevo punto y todos los puntos de entrenamiento.
- Identificar los 'k' vecinos más cercanos.
- Asignar la clase más frecuente entre esos vecinos.

#### VENTAJAS

- Simple de entender
- Es rápido para empezar
- Funciona para clasificación y regresión.
- Añadir nuevos datos es trivial.

#### DESVENTAJAS

- Lento con grandes datos
- Sensible a la escala

### 1.
### 2. 
### 3. Preparar datos

## Necesita:

- Un conjunto de datos de entrenamiento con características (X columnas con valores numéricos) y etiquetas (y esta es la variable objetivo).
- Un conjunto de datos de prueba para validar el modelo.

## Pasos críticos:

- Normalizar/Estandarizar. Este paso es fundamental. Dato que K-NN se basa en distancias, las características con escalas más grandes dominarán a las escalas pequeñas. La estandarización asegura que todas las características contribuyan por igual.
- Validar datos: Típicamente se usa una división de 70-80% para entrenamiento y 20-30% para prueba.

### 4. Elegir Valor de K

La elección de k (el número de vecinos a considerar) es clave para el rendimiento del modelo.

- **K pequeño (ej: 1-3):** El modelo es muy sensible al ruido y a los datos atípicos (*outlier*), lo que puede llevar a un sobreajusto (*overfitting*)
- **K grande**La predicción se vuelve más estable y suave, pero se corre el riesgo de perder detalles locales importantes y causar subajuste (*underfitting*).
- **Regla general (Punto de partida):** Prueba con *k = n^(1/2)*, donde n es el número de muestras de entrenamiento.
- **Mejor práctica:** Utiliza validación cruzada (*cross-validation*) para probar un rango de valores de *k* y encontrar el que ofrezca el mejor rendimiento en datos no vistos.

### 5. Seleccionar la Métrica de Distancia

La cercanía se mide con una métrica de distancia. Las más comunes son:

- **Distancia Euclidiana**: La más usada. Es la distancia en línea recta entre dos puntos. Ideal para datos densos y -> **Distancia de Manhattan**: La suma de las diferencaias absolutas entre coordewnadas, Es como movese por una cuadrícula (solo giros de 90 grados). Funciona bien es espacios de alta dimensionalidad.
- **Distancia de Minkowski**: Una generalización de las dos anteriores. Con un parametro *p*, si *p=1* es Manhattan y si *p=2* es Euclidiana.

### 6. Implementar el Algoritmo

El proceso para predecir un nuevo punto es el siguiente:

**1. Calcular la distancia** del nuevo punto a todos los puntos del conjunto de entrenamiento usando la métrica elegida.
**2. Ordenar las distancias** de menor a mayor y seleccionar los K puntos con las distancias más pequeñas (los K vecinos más cercanos).
**3. Realizar la predicción**:
    - **Para Clasificación**: Contar las etiquetas de los K vecinos y asignar la clase más frecuente (voto mayoritario).
    - **Para Regresión**: Calcular el promedio de los valores de los K vecinos.

### 7. Evaluar el Rendimiento
=
Para saber qué tan bueno es el modelo, usar las métricas de evaluación apropiadas:
    **Para clasificación**: Exactitud (*accuracy*), precisión, recall, *F1-score* y la *matriz de confusión*.
    **Para regresión**: *Error Cuadrático Medio (MSE)*, *Raíz del Error Cuadrático Medio (RMSE)* o el *Coeficiente de Determinación (R^2)*

### 8. Optimizar el Modelo

Si el rendimiento no es el esperado, puede probar lo siguiente:

**Ajustar el valor de K:** Es el hiperpárametro más importante.
**Probar diferentes métricas de distancias:** A veces, Manhattan funciona mejor que Euclidiana, o viceversa.
**Usar pesos en la votación:** Dar más importancia a los vecinos más cercanos. En lugar de que cada vecino tenga un voto igual, los más próximos tienen más influencia.
**Reducir la dimensionalidad**. Si tienes muchas características, usa técnicas como el Análisis de Componentes Principales (PCA) para combatir la "maldición de la dimensionalidad".
**Para grandes conjuntos de datos:** Considera usar estructuras de datos optimizadas como KD-Trees o Ball-Trees para acelerar la búsqueda de los vecinos más cercanos.
    
