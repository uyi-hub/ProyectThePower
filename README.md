# ProyectThePower 🗂 
## README.MD

:fa-step-forward: Repositorio ejemplo para el proyecto practico de EDA del master en data analytics de The Power

------------

- **Descripción**
Para este primer proyecto del MBA de Data Analytics el objetivo era realizar un analisis EDA con un conjunto de datos a elección. He elegido, a través de Kuggle, un conjunto de datos que contenia información sobre las viviendas en venta de la comunidad de Madrid a través de la plataforma Idealista. El objetivo es detectar patrones en los precios de las viviendas, ya que el aumento en algunas zonas y en otras no, hace variar el precio actual con el anterior. Teniendo en cuenta el tipo de vivienda, habitaciones, baños, localización, etc...

- **Estructura del proyecto:**
  Dataset bruto (raw)
[Datos idealista .csv.zip](https://github.com/user-attachments/files/24650134/Datos.idealista.csv.zip)
  Dataset limpio (clean)
 [Ver Google Sheet] https://docs.google.com/spreadsheets/d/1WP0Bnx5O9zxu2nfk-Ut1MEJ97IViJWlk8SFA0a5qfuY/edit?usp=sharing
  📊 Dashboard interactivo en Google Sheets:  
[Ver Google Sheet]((https://docs.google.com/spreadsheets/d/1WP0Bnx5O9zxu2nfk-Ut1MEJ97IViJWlk8SFA0a5qfuY/edit?usp=sharing))

- **Resultado del proyecto:**
Empezando por el inicio de la transformacion de los datos en crudo, opte por ocultar la columna de "Pecio Anterior" ya que era un dato que no iba a utilizar y no me servia a la hora del resultado final del EDA. Luego pase a formato moneda la columna de "Precio Actual" y decidi completar con "ND" los casilleros vacios, tanto de la columna de "Ascensor" como la de "Localizacion", la de "Plantas" y la de "Tag", ya que eran datos que no tenia manera de comprobar.
 Luego de la limpieza de los datos, una vez que me ha quedado en limpio el dataset, empece a realizar las tablas dinamicas para luego obtener los graficos correspondientes con el objetivo de crear el Dashboard final. Para esto me enfoque en el dato duro que le puede llegar a interesar a un potencial cliente de compra de piso en Madrid, imaginando que es una persona que no tiene una zona especifica donde desea vivir o comprar sino que puede llegar a ser una compra por inversion o algo por el estilo, lo cual seria de interes mostrar los datos de varias zonas, agregando dos KPIs sobre la cantidad de barrios que hay y el precio medio de compra en Madrid.

- **Observaciones:**
-  He tenido algunos problemas utilizando sheets con los segmentadores y filtros creo, me parece que se podrian utilizar mas y mejor pero no logre hacerlo. Tambien queriendo cortar el dashboard de la hoja de calculo de las tablas dinamicas para dejarlo aislado en una nueva (no se ni si es posible en sheets) pero no me lo permitio hacer.
  Y por utlimo añadiria un grafico de habitaciones, precio actual y zonas, con un segmentador especial que me permita observar por zonas de Madrid cuanto me sale un piso de 1, 2 o 3 habitaciones en cada zona de la ciudad y de ahi sacar un KPI con un top 3 de zonas mas economicas para cada tipo de cantidad de habitaciones. 
