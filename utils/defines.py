
class Defines:
	def __init__(self):
		self.params = {}
		# Amount of light captured by the camera.
		# Can be used to increase/decrease brightness in case pixels are over-saturated.
		# Recommended Range: 0.1 to 10.0
		self.params['EXPOSURE'] = 2.0

		# self.params['N_WAVELENGTHS'] = 0

	def __getitem__(self, k):
		return self.params[k]

	def __setitem__(self, k, x):
		self.params[k] = x
