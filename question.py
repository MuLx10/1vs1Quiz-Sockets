
class Question(object):
	"""docstring for Question"""
	def __init__(self, file_name):
		self.file = open(file_name,'r')

	def next_question(self):
		line = self.file.readline().strip('\n')
		return line

		
		