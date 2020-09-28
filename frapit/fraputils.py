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

	def loadfrap( self , file_name , sep = None , comment_char = '#', **attrs ) :
		self.load( file_name = file_name , sep = sep , comment_char = comment_char , **attrs )
	
		df = [ abs( self.f()[ i ] - self.f()[ i - 1 ] ) for i in range( 1 , len( self ) ) ] # delta f


		i =  df.index( max( df ) ) + 1 

		self.input_values( 'frapframe' , [ self.frames()[ i ] ] * len( self ) )

		if 't' in attrs.keys() :
			self.input_values( 'tfrap' , [ self.tfrap()[ i ] ] * len( self ) )

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
