import os
import glob
import pandas as pd
import numpy as np

abundances=[]
family=[]
samples=[]
        

#se leen los archivos de la carpeta

for filename in glob.glob('*.txt'):
	#por cada archivo dentro de la carpta, abrimos y generamos un arreglo de las lineas
	#dentro del archivo
	#tambien extraemos los nombres de cada muestra y la guardamos en un arreglo
	
	f=open(filename)
	lines=f.readlines()
	sample_name=filename.split('-')[0]
	samples.append(sample_name)

	#Por cada linea del archivo, extraemos las cuarta columna
	for x in lines:
		value=x.split('\t')[3]
		
		#Vemos si el valor corresponde a F1 o F2

		if (value=='F' or value=='F1'):
                        #Si se cumple la condicion, extraemos el taxa_id

			taxa_id=x.split("\t")[4]
			
			#Desde donde se encuentra el valor con F1 o F, definimos un rango, desde donde
			#se comienzan a recorrer las lineas desde el valor encontrado en reversada, hasta encontrar un valor 'O'
			
			top_range=int(lines.index(x))
			reversed_range=range(top_range,0,-1)
			
			#ademas vamos a extraer los valores de abundancia correspondiente a la fila encontrada
			#Le adjuntamos el taxa_id y sample_name para luego poder identificarlo mejor al agregarlo a la matriz
			#Por ultimo se incluye en el arreglo
			ab=x.split('\t')[0]
			ab_id=ab+"-"+taxa_id+"-"+sample_name
			abundances.append(ab_id)

             		#Se extrae ademas el nombre del organismo con el que estamos trabajandoi
			organism=x.split('\t')[5]
			organism_no_spaces="-".join(organism.split())
			
			#Aqui ya empezamos a buscar el orden correspondiente a la familia
			
			for i in reversed_range:

				linea=lines[i]
				orden=linea.split('\t')[3]

                                #Si la columna 4 del archivo corresponde a un 'O', es porque se encontro un orden
				if(orden=='O'):
					#Se comienzan a concatenar los datos para definir los nombres de las familias
					taxa=linea.split('\t')[5]
					taxa_strip=taxa.strip("\n")
				
					family_name=taxa_strip+" "+organism_no_spaces+" "+taxa_id
					family_no_spaces="_".join(family_name.split())
				
					if(family_no_spaces not in family) :
						family.append(family_no_spaces)
						break

					break
#A estas alturas, ya comenzamos a confeccionar la matriz, donde el nombre de las muestras
#seran las columnas y las familias junto con el orden asociado y el taxa_id seran las filas

ncolumn=len(samples)
nrows=len(family)
count=0

#Llenamos filas y columnas
matrix = pd.DataFrame(index=np.arange(nrows), columns=samples)
for i in family:
	matrix.rename(index={count:i},inplace=True)
	count=count+1


columns=matrix.columns
rows=matrix.index

#Llenamos la matriz con los valores de abundancia
for a in abundances:

	tax_id=a.split('-')[1]
	smp_name=a.split('-')[2]
	abd=a.split('-')[0]

	for c in columns:
		if(c==smp_name):
			for r in rows:
				r_id=r.split("_")[2]
				if (tax_id==r_id):
					matrix.at[r,c]=abd
					break	
matrix.fillna('0', inplace=True)
matrix.to_csv('matrix.tsv', sep ='\t')
 
pd.set_option("display.max_rows", None, "display.max_columns", None)

print(matrix)
