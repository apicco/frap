from trajalign.traj import Traj
import numpy as np

class Frap( Traj ) :

	__slots__ = Traj.__slots__
	__slots__.append( '_tfrap' )
	__slots__.append( '_frapframe' )

	def __init__( self , **annotations ):

		# Frap main attributes
		super().__init__( **annotations )
		self._tfrap = np.array( [] , dtype = 'float64' )
		self._frapframe = np.array( [] , dtype = 'int' )

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
