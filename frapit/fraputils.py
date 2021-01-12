from trajalign.traj import Traj
from scipy.optimize import curve_fit
import numpy as np

class Frap( Traj ) :

	__slots__ = Traj.__slots__
	__slots__.append( '_tfrap' )
	__slots__.append( '_frapframe' )
	__slots__.append( '_mf' ) # mobile fraction
	__slots__.append( '_ht' ) # half time

	def __init__( self , **annotations ):

		# Frap main attributes
		super().__init__( **annotations )
		self._tfrap = np.array( [] , dtype = 'float64' )
		self._frapframe = np.array( [] , dtype = 'int' )

		self._mf = np.array( [] , dtype = 'float64' )
		self._ht = np.array( [] , dtype = 'float64' )

	def frapframe( self ) : 

		if len( self._frapframe ) :
			return self._frapframe[ 0 ]
		else :
			raise AttributeError( 'frapframe is not defined' )
	
	def tfrap( self ) : 

		if len( self._tfrap ) :
			return self._tfrap[ 0 ]
		else :
			raise AttributeError( 'tfrap is not defined' )

	def loadfrap( self , file_name , sep = None , comment_char = '#', dt = np.nan , t_unit = '' , **attrs ) :

		# load the frap data, min requirement is frame and f, t can be added throught dt.
		self.load( file_name = file_name , sep = sep , comment_char = comment_char , **attrs )

		# load the time information
		if dt : 
			if t_unit : 
				self.time( dt , unit = t_unit )
			else :
				raise AttributeError( 'Please, specify the unit' )

		# delta in fluorescence intenstiy to find the frap time and frame
		df = [ abs( self.f()[ i ] - self.f()[ i - 1 ] ) for i in range( 1 , len( self ) ) ] 
		i =  df.index( max( df ) ) + 1 

		# assign the frap frame and time to frapframe and tfrap
		self.input_values( 'frapframe' , [ self.frames()[ i ] ] * len( self ) )

		# annotate the file_name
		self.annotations( 'file' , file_name )

		if 't' in self.attributes() :
			self.input_values( 'tfrap' , [ self.t()[ i ] ] * len( self ) )

	def frapnorm( self , w = 10 , full_range = False ) :

		i_f = list( self.frames() ).index( self.frapframe() )
		l = len( self )

		mf = np.mean( self.f()[ max( 0 , i_f - w ) : i_f ] ) # average the fi before photobleaching at i_f

		fn = [ self.f()[ i ] / mf for i in range( l ) ]

		if full_range :
	
			fn0 = fn[ i_f ]
			# fn[ i ] * mf = self.f()[ i ]
			# fn0 * mf = self.f()[ i_f + 1 ]
			# thus :
			fn = [ ( fn[ i ] - fn0 ) * mf / ( mf - fn0 * mf ) for i in range( l ) ]

		self.input_values( 'f' , fn )
		self.input_values( 'frames' , self.frames() - self.frapframe() )
		if 't' in self.attributes() :
			self.input_values( 't' , self.t() - self.tfrap() )

	def fit( self , tmax = np.inf , maxfev = None ) :

		# define the data used to perform the fitting
		x =  [ self.t( i ) for i in range( len( self ) )  if ( self.t( i ) >= 0 ) & ( self.t( i ) < tmax ) ]
		y =  [ self.f( i ) for i in range( len( self ) )  if ( self.t( i ) >= 0 ) & ( self.t( i ) < tmax ) ]

		if maxfev : 
			popt , pcov = curve_fit( self.func , x , y , maxfev = maxfev )
		else :
			popt , pcov = curve_fit( self.func , x , y )

		self._mf = np.array( [ popt[ 0 ] , np.sqrt( np.diag( pcov )[ 0 ] ) ] )

		self._ht = np.array( [ np.log( 2 ) / popt[ 1 ] , np.sqrt( np.diag( pcov )[ 1 ] ) * np.log( 2 ) / popt[ 1 ] ** 2 ] )
		
		return popt , pcov 

	def func( self, x , A , t ) :

		return A * ( 1 - np.exp( - t * x ) )

	def mf( self , *kwargs ) : 

		if ( ( kwargs is None ) & ( len( self._mf ) ) ) :

			return self._mf

		else :
			
			self.fit( *kwargs )
			return self._mf
		

	def ht( self , *kwargs ) :
		
		if ( ( kwargs is None ) & ( len( self._ht ) ) ) :

			return self._ht

		else :
			
			self.fit( *kwargs )
			return self._ht

