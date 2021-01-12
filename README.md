# frap
Toolbox for the analysis of FRAP experiments. It is built on the [trajaling](http://apicco.github.io/trajectory_alignment/) and [trajplot utilities](https://github.com/apicco/trajectory_plotting)

A frap object is defined as

`my_frap = Frap()`

Its content is loaded with

`my_frap.loadfrap(
	file_name = 'foo_frap.txt' ,
	dt = dt ,                                    
	t_unit = 's' ,
	frames = 0 ,                                 
	f = 1 )`

The time when photobleaching happens is extracted with `my_frap.tfrap()`.

The fluorescence intensity of the frap object can be normalised with 

`my_frap.frapnorm( w = 10 , full_range = False )`
where `w` is the nuber of frames before the photobleaching event, which are used to compute the average fluorescence intensity before photobleaching (default is `w = 10`). `full_range` is the normaglization range and can be `True` or `False` (default).
By default, frapnorm sets time 0 to be the first time point after photobleaching.

A frap experiment can be fit with

`popt , pcov = my_frap.fit( tmax = np.inf , maxfev = None )`

`popt` are the optimal fit values and `pcov` the estimated covariance of `popt`. `tmax` sets the upper range of timepoints (starting from 0, the first time point after photobleaching), which are used to compute the fit. `maxfev` is the max number of iterations, `None` uses the default (600). 

For simplicity, the half time and mobile fraction can also be computed as

`half_time = my_frap.ht()`

and

`mobile_fraction = my_frap.mf()`

The input parameters are the same of `Frap().fit()`, with the same defaults.
The half time of a frap experiment is measured with
