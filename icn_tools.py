print "> Load icn_tools.py"

import enthought.traits.api as eta
import enthought.traits.ui.api as etua
import enthought.traits.ui.menu as etum
import enthought.traits.ui.wx.tree_editor as etuwt
import enthought.pyface.api as epa

VERT_enc = {
	0 : "Current",
	1 : "Differential Conductance (dI/dV)",
	2 : "Second derivative (d2I/dV2)",
	3 : "Current (ADC 0)",
	4 : "First derivative, real part (ADC 1)",
	5 : "First derivative, imaginary part (ADC 2)",
	6 : "Secondary derivative (ADC 3)",
	7 : "Nada",
	8 : "Nada de nada",
	9 : "Nada de nada de nada",
	10 : "di_q",
	11 : "di2_q",
	12 : "Topography (DAC 0)"
	}
	
VERT_yenc = {
	0 : "I",
	1 : "dI/dV",
	2 : "d2I/dV2",
	3 : "I",
	4 : "dI/dV",
	5 : "Imaginary",
	6 : "d2I/dV2",
	7 : "Nada",
	8 : "Nada de nada",
	9 : "Nada de nada de nada",
	10 : "di_q",
	11 : "di^2_q",
	12 : "Topography (DAC 0)"
	}


def deal_with_fname(fname) :
	"""
	>>> deal_with_fname("A120423.183450.VERT")
	'18:34:50 23/04/2012'
	"""
	return fname[8:10] + ":" + fname[10:12] + ":" + fname[12:14] + " "\
				+ fname[5:7] + "/" + fname[3:5] + "/20" + fname[1:3]


def convert_filename(filename):
	"""
	Function that uniformed the Windows or Unix pathes.
	A path with \ in it has to be return with /
	>>> convert_filename("C:\\mon fichier\\rpiquerel\\file.VERT")
	'C:/mon fichier/rpiquerel/file.VERT'
	>>> convert_filename("C:/mon fichier/rpiquerel/file.VERT")
	'C:/mon fichier/rpiquerel/file.VERT'
	"""
	filename = filename.replace("\r", '/r')
	filename = filename.replace("\f", '/f')
	return filename.replace("\\", '/')


def shortned_filename(filename):
	"""
	>>> print shortned_filename("C:/mon fichier/Rpiquerel/File.VERT")
	File.VERT
	"""
	return filename.split("/")[-1]


def key_equal(s, key_list):
	"""
	>>> key_equal('Num.X / Num.X=256', ['Num.X / Num.X'])
	True
	>>> key_equal('Num.X / Num.X=256', ['Num.X/Num.X'])
	False
	"""
	if key_list :
		for i in key_list :
			if i not in s.split("=")[0] :
				return False
	return True


def process_key_value_from_parameters(s, n, key_list=[], skip_rows=-1):
	"""
	>>> process_key_value_from_parameters("LengthX = 256", 0, ["LengthX"])
	('LengthX ', 256.0)
	>>> process_key_value_from_parameters("LengthX = 256", 0, ["LengthX"], 2)
	(None, None)
	>>> process_key_value_from_parameters("", 0)
	(None, None)
	>>> process_key_value_from_parameters("abc", 0)
	(None, None)
	>>> process_key_value_from_parameters(" abc", 0, ["abc"])
	(None, None)
	>>> process_key_value_from_parameters("=truc", 0, ["truc"])
	(None, None)
	"""
	if s and ("=" in s) and s[0].isalpha() and (n > skip_rows) and key_equal(s, key_list) :
				return (s.split("=")[0], double(s.split("=")[-1]))
	return (None, None)

class VerticalManipulation :
	
	def __init__(self, fname = "", plotting_mode = "V") :

		self.fname = convert_filename(fname)
		self.fname_label = shortned_filename(fname)
		self.file = None
		self.data = []
		self.finalTab = {}
		self.parameters = {"i" : [], "t" : [], "V" : [], "z" : []}
		self.Vertmandelay = 1
		self.VertSpecBack = 1
		self.opening_filter = []
		self.dataHeader = None
		self.plotting_mode = plotting_mode
	

	def open_file(self) :
		"""
		The file has to be open correctly.
		>>> vm = VerticalManipulation("test_file.VERT")
		>>> vm.open_file()
		>>> print vm.file != None
		True
		>>> vm = VerticalManipulation("")
		>>> vm.open_file()
		>>> print vm.file != None
		False
		"""
		if self.fname :
			try :
				self.file = open(self.fname, "r")
				return
			except :
				print "Warning : did not open the file correctly"
		self.file = None
	

	def close_file(self) :
		self.file.close()

			
	def reading_header(self) :
		"""
		>>> vm = VerticalManipulation("test_file.VERT")
		>>> vm.open_file()
		>>> vm.reading_header()
		>>> print "Vertmandelay : " + str(vm.Vertmandelay) + ", VertSpacBack : " + str(vm.VertSpecBack)
		Vertmandelay : 61.0, VertSpacBack : 1.0
		>>> vm.dataHeader
		17
		>>> vm.finalTab.keys()
		[0, 4]
		"""
		
		STM_parameters = {}
		skip_rows = 3
		key_list = ["Vertmandelay", "VertSpecBack"]

		for i in range (skip_rows) :
			self.file.next()

		for s in self.file :
			if "DATA" in s :
				break
			if s and ("=" in s) and s[0].isalpha() :
				s0, s1 = s.split("=")
				if s0 in key_list :
					STM_parameters[s0] = double(s.split("=")[-1])

		for k in key_list :
			if STM_parameters.has_key(k) :
				pass
			else :
				print "Warning : problem to read the STM parameters"
				raise
		self.Vertmandelay = STM_parameters["Vertmandelay"]
		self.VertSpecBack = STM_parameters["VertSpecBack"]

		try :
			self.dataHeader = int(self.file.next().split(" ")[-1])
		except ValueError:
			print "Could not deduce headers."
			raise

		for i in VERT_enc :
			if self.dataHeader & (1 << i) :
				self.finalTab[i] = {"name": None, "header" : VERT_enc[i], "ylabel" : VERT_yenc[i], "data" : None}
				
			
	def load_data (self) :
		"""
		>>> vm = VerticalManipulation("test_file.VERT")
		>>> vm.open_file()
		>>> vm.reading_header()
		>>> vm.load_data()
		>>> print "array_width : " + str(vm.array_width)
		array_width : 5
		"""

		for line in self.file :
			self.data.append (self.file.next().split("\t")[0:-1])
		self.array_width = len (self.data[0])

		try :
			self.data = hsplit (array (self.data), self.array_width)
		except RuntimeError :
			print ("Enable to split the read data buffer into column(s).")
			raise
		

	def compute_data (self) :
		"""
		>>> vm = VerticalManipulation("test_file.VERT")
		>>> vm.open_file()
		>>> vm.reading_header()
		>>> vm.load_data()
		>>> vm.compute_data()
		>>> print vm.parameters["i"][0], vm.parameters["V"][0], vm.parameters["z"][0], vm.parameters["t"][0], 
		1.0 -1198.83 0.0 0.00122
		>>> print len(vm.parameters["i"])
		4096
		>>> print vm.parameters["i"][4095], vm.parameters["V"][4095], vm.parameters["z"][4095], vm.parameters["t"][4095], 
		8191.0 -1199.41 0.0 9.99302
		"""

		self.parameters["i"] = double(self.data[0]).T[0]
		self.parameters["V"] = double(self.data[1]).T[0]
		self.parameters["z"] = double(self.data[2]).T[0]
		
		# Convert the index of the data in vertical manipulation time
		# The formula seems tricky but there is a 20e-6 s delaytime to take into account
		self.parameters["t"] = array(double(self.data[0]).T[0]) * 20e-6 * self.Vertmandelay / (2 - self.VertSpecBack)
		
		n = 0
		for i in VERT_enc :
			if self.dataHeader & (1 << i) :
				self.finalTab[i]["data"] = double (self.data [n + 3]).T[0]
				n = n + 1

				
	def plot_data (self) :
		
		_xlab = {
			"i" : "Index",
			"t" : "Duration (s)",
			"V" : "Bias Voltage (mV)",
			"z" : "Height (Angs)"
		}
	
		# for i in [4] : #self.finalTab :
		# 	figure ()
		# 	plot (self.parameters[self.plotting_mode], self.finalTab[i]["data"], "r", label = self.finalTab[i]["ylabel"] + " " + deal_with_fname(self.fname_label))
		# 	title (self.finalTab[i]["ylabel"] + " " + deal_with_fname(self.fname_label))
		# 	xlabel(_xlab[self.plotting_mode])
		# 	ylabel(self.finalTab[i]["ylabel"])


		figure ()
		plot (self.parameters["V"], self.finalTab[4]["data"], "r", label = "dI/dV " + deal_with_fname(self.fname_label))
		title ("dI/dV" + " " + deal_with_fname(self.fname_label))
		xlabel("Bias (mV)")
		ylabel("Differential conductance")


	def load_file(self) :
		self.open_file()
		self.reading_header()
		self.load_data()
		self.compute_data()
		self.plot_data()
		self.close_file()
			
			
class UiTest(eta.HasTraits):

	def __init__(self, fname = ""):

		self.data = eta.Dict()
		self.fname = eta.File()
		self.plotting = eta.String()
		self.open_VERT = eta.Button("Open VERT")
		self.only_I = False
		self.only_dIdV = False
		self.pointers = []
		self.fname = os.getcwdu ()
		self.plotting = "V"

		
	def _load_VERT (self) :

		if self.fname[-5:-1] == ".VER" :
			try :
				vm = VerticalManipulation(self.fname, self.plotting)
				vm.open_file ()
				vm.reading_header ()
				vm.load_data ()
				vm.compute_data ()
				vm.plot_data ()
				vm.close_file ()
			except :
				print("Warning : Fail to open the vertical manipulation.")
				raise
		else:
			print("Warning : " + self.fname + " type not known.")
			return

			
	def _load_VERT_vs_bias (self) :

		self.plotting = "V"
		self._load_VERT ()

		
	def _load_VERT_vs_index (self) :

		self.plotting = "i"
		self._load_VERT ()

		
	def _load_VERT_vs_duration (self) :

		self.plotting = "t"
		self._load_VERT ()
		
		
	def _load_VERT_vs_height (self) :

		self.plotting = "z"
		self._load_VERT ()		
	
	
	open_VERT_vs_bias = etum.Action(name = 'VERT vs bias', action = '_load_VERT_vs_bias')
	open_VERT_vs_index = etum.Action(name = 'VERT vs index', action = '_load_VERT_vs_index')
	open_VERT_vs_duration = etum.Action(name = 'VERT vs duration', action = '_load_VERT_vs_duration')
	open_VERT_vs_height = etum.Action(name = 'VERT vs height', action = '_load_VERT_vs_height')
	
	view = etua.View (
		# etua.Item("data", style="simple"),
		# etua.Item('fname', editor=etua.FileEditor(filter = ['*.plot'], auto_set = True), style = "custom"),
		etua.Item('fname', editor=etua.FileEditor(auto_set = True), style = "custom"),
		toolbar = etum.ToolBar(open_VERT_vs_bias, open_VERT_vs_index, open_VERT_vs_duration, open_VERT_vs_height),
		resizable = True,
		scrollable = True,
		title= "Vertical Manipulation UI",
		height = 640,
		width = 800
	)

	
def uitest(fname = ""):

	wxuitest = UiTest(fname)
	wxuitest.configure_traits()


if False and __name__ == "__main__":
    import doctest
    doctest.testmod()

