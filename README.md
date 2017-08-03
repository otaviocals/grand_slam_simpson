# Grand Slam - Simpson Analysis Tool #
### Escrito por Otavio Cals ###
### Agosto/2017 ###

=========

### Introducao ###

### Utilizacao ###

### Programa ###
Escrito em python com interface grafica criada utilizando [Kivy](https://kivy.org/).

1. Scripts Originais
	* webscraper.py: Acessa um link do Banco Central atraves da plataforma Selenium, obtem a tabela de cotacao de juros e a salva em formato .csv
	* main.py: Gera e controla a interface grafica. Chama periodicamente a funcao de webscraping, fornecendo os links a serem acessados.
2. Scripts Importados
	* win32timezone.py: Script para lidar com datas e horarios em Windows
	* file.py, form.py, notification.py, tools.py, xbase.py, xpopup.py: Scripts do plugin [Xpopup](http://github.com/kivy-garden/garden.xpopup) para Kivy. Fornecem a visualizacao de pastas para escolha de diretorio destino.
3. Specs
	* Scripts para compilacao do programa utilizando pyinstaller.
4. Logos
	* Logos do [Cals Emporium](https://cals.herokuapp.com).

### Compilacao ###

Novas veroes podem ser compiladas utilizando o pyinstaller e os specs fornecidos (main_linux.spec para compilar versoes para Linux e main_windows.spec para versoes para Windows).
A pessoa deve alterar o diretorio destino no campo "pathex" dos specs. Deve-se certificar tambem que as bibliotecas listadas em main.py e webscraper.py estao instaladas.
