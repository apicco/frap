# frap
Toolbox for the analysis of FRAP experiments. It is built on the [trajaling](http://apicco.github.io/trajectory_alignment/) and [trajplot utilities](https://github.com/apicco/trajectory_plotting)

A frap object is defined as

`my_frap = Frap()`

Its content can be loaded with

`x.loadfrap(
	file_name = path + '/' + d + '/' + f ,       
	dt = dt ,                                    
	t_unit = 's' ,
	frames = 0 ,                                 
	f = 1 )`
