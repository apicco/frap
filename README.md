# FRAP Toolbox for the analysis of FRAP experiments. 

It is built on [trajalign](http://apicco.github.io/trajectory_alignment/) and [trajplot](https://github.com/apicco/trajectory_plotting)

You can test this toolbox with some trajectory example data and in the [Google Colaboratory](https://bit.ly/frapit). The Colaboratory also gives the possibility to upload and analyse your data: https://bit.ly/analyse-your-frap: 

## Image preparation

The image needs to be background subtracted and corrected for photobleaching: the photobleaching caused by imaging and the photobleaching caused by the FRAP event itself.

When imaging yeast cells with epifluorescence illumination to do local photobleaching, we can correct the Image with the BGN_FRAP_V1.ijm FIJI plugin. Yeast cells generally have a distinctive cytoplasmatic background, allowing for easy cell boundary detection. The plugin performs
1) background subtraction 
2) detects the cell 
3) and levels the brightness of the cytoplasm to correct for any photobleaching.

The plugin must be run on a crop of the single cell where the FRAP experiment is performed. A larger field of view would dilute the photobleaching correction following the actual FRAP experiment.
Two images are output:
\_FRAPN.tif, the image background subtracted and normalised for FRAP, and 
\_FRAPN_MD.tif, which is \_FRAPN.tif with the cytoplasmatic background subtracted by median filtering.

Generally, \_FRAPN.tif should be used to quantify the FRAP. It is sufficient to circle the photo-bleached spot and measure its intensity over time (for example, with Image>Stacks>Plot Z-axis Profile). The values can be saved on a .txt file.
 
## Trajectory analysis 

A FRAP object is defined as

`my_frap = Frap()`

Its content is loaded with

`my_frap.loadfrap( file_name = 'foo_frap.txt' , dt = dt , t_unit = 's' , frames = 0 , f = 1 )`

The first time point after photobleaching happens is extracted with `my_frap.tfrap()`, and the first frame with `my_frap.frapframe()`.

The fluorescence intensity of the FRAP object can be normalised with 

`my_frap.frapnorm( w = 10 , full_range = False )`

where `w` is the number of frames before the photobleaching event, which are used to compute the average fluorescence intensity before photobleaching (default is `w = 10`). `full_range` is the normalisation range and can be `True` or `False` (default).
By default, frapnorm sets time 0 to be the first time point after photobleaching (i.e. `my_frap.frapnorm().tfrap()` is equal to 0 )

The fit of a FRAP experiment is done with

`popt , pcov = my_frap.fit( tmax = np.inf , maxfev = None )`

`popt` contains the optimal fit values, and `pcov` is the estimated covariance of `popt`. `tmax` sets the upper range of time points (starting from 0, the first time point after photobleaching), which are used to compute the fit. `maxfev` is the max number of iterations, `None` uses the default (600). 

For simplicity, the half-time and mobile fraction can also be computed as

`half_time = my_frap.ht()`

and

`mobile_fraction = my_frap.mf()`

The input parameters are the same as `Frap().fit()`, with the same defaults.
The half-time of a FRAP experiment is measured with
