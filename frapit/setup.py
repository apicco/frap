from distutils.core import setup

setup( name = 'frap' ,
		version = '0.0' ,
		description = 'Utilities to analyse FRAP data, based on the trajalign library' ,
		author = 'Andrea Picco',
		author_email = 'andrea.picco@unige.ch',
		url = 'http://apicco.github.io/frap/',
		download_url = 'https://github.com/apicco/frap/archive/master.zip',
		packages = [ 'frapit' ],
		license = 'The software is distributed under the terms of the GNU General Public License Version 3, June 2007. Trajalign is a free software and comes with ABSOLUTELY NO WARRANTY. You are welcome to redistribute the software. However, we appreciate is use of such software would result in citations of Picco, A., Kaksonen, M., _Precise tracking of the dynamics of multiple proteins in endocytic events_,  Methods in Cell Biology, Vol. 139, pages 51-68 (2017) http://www.sciencedirect.com/science/article/pii/S0091679X16301546'

		)
