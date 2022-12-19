#==========================importacion y lectura==============================
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# aplicamos la utilidad de seaborn
sns.set()

# Definimos una variable con la ruta al archivo csv
path="/listings.csv"

# El archivo listings.csv utilizado es "http://data.insideairbnb.com/germany/bv/munich/2022-06-21/data/listings.csv.gz"

#==========================definición de funciones==============================

def string_to_float(value):
      ''' Limpia el formato de un numero de una celda
          en formato string, convirtiendolo a flotante '''   
      return float( value.replace('$', '').replace(',', '') )

def avarage(l, n_decimal=2 ):
    ''' Calcula el promedio de una lista '''
    return round(sum(l) / len(l), n_decimal)

def min_value(l):
    ''' Obtiene el menor valor de una lista '''
    return min(l)

def summatory(l):
    ''' Obtiene la suma de todos los elementos de una lista '''
    return sum(l)

def count(l):
    ''' toma una lista, y retorna un diccionario
        que asocia a cada elemento de la lista
        el numero de veces que este aparece en la lista 
    '''
    return dict((i, l.count(i)) for i in set(l))
  
#==========================estructura de datos==============================

def create_dict(as_key, as_value, converter=None, foo=None):
    ''' as_key=<String>
        as_value=<String>
        converter=[function]
        foo=[function]

        as_key toma como valor un string con el nombre de la columna a utilizar para filtrar los valores que seran _
        utilizados como keys.

        as_value toma como valor un string con el nombre de la columna que se va a utilziar para filtrar los valores _
        que seran concatenados a una lista y asignados las disntas keys procesadas

        converter toma una funcion que sera usada para formatear los valores antes de ser asignados al array utilizado _
        como filtro de valores

        foo toma una funcion que sera aplicada al array resultante de aplicar todos los filtros anteriores _
        sobrescribiendo el valor final
    '''

    with open(path, newline='') as f:

        d = {}
        reader = csv.DictReader(f, delimiter=',')
        
        for row in reader:
            key = row[ as_key ]
            element = converter(row[as_value]) if converter else row[as_value]
            
            if  key not in d.keys():
                d[ key ] = []
            
            d[ key ].append( element )
        
        # Si se definio una función como parametro para aplicar, se sobreescriben los elementos modificados
        if foo :
            for k,v in d.items():
                d[ k ] = foo( v )

        return d
      
#==========================Nuevas estruturas==============================

menor_precio_por_cantidad_habitaciones = create_dict( "bedrooms", "price", string_to_float, min_value)
cantidad_reseñas_por_barrio = create_dict("neighbourhood_cleansed", "number_of_reviews", string_to_float, summatory)
cantidad_tipo_habitacion_por_barrio = create_dict("neighbourhood_cleansed", "room_type", foo=count)
precio_promedio_por_barrio = create_dict("neighbourhood_cleansed", "price", string_to_float, avarage )

#==========================definición de funciones para graficos==============================

def create_bar(dictio, xlabel=None, ylabel=None, title=None):
    # Crea un gráfico de barras
    plt.figure(figsize=(10, 8))
    plt.xticks(rotation=90, fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.title(title, fontsize=20)
    plt.bar(dictio.keys(), dictio.values())

def create_pie(clave, dictio, name=None):
    # crea un gráfico de torta
    plt.figure(figsize=(3, 3))
    plt.title(name, fontsize=10)
    plt.pie(dictio.values(), labels=dictio.keys())

#==========================pregunta 1==============================

create_bar(menor_precio_por_cantidad_habitaciones, 
           'cantidad de habitaciones', 'menor precio',
           'menor precio por cantidad de habitaciones')

#==========================pregunta 2==============================

create_bar(menor_precio_por_cantidad_habitaciones, 
           'cantidad de habitaciones', 'menor precio',
           'menor precio por cantidad de habitaciones')

#==========================pregunta 3==============================

for barrio, reviews in cantidad_reseñas_por_barrio.items():
    if reviews >= 5000:
        create_pie(barrio, cantidad_tipo_habitacion_por_barrio[barrio],
                   "tipos de habitaciones en {0}".format(barrio))
        
#==========================pregunta 4==============================

create_bar(precio_promedio_por_barrio, 
           'barrios', 'precio promedio', 'precio promedio por barrio')
