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
	0 : "I (a.u.)",
	1 : "dI/dV (a.u.)",
	2 : "d2I/dV2 (a.u.)",
	3 : "I (a.u.)",
	4 : "Re dI/dV (a.u.)",
	5 : "Im dI/dV (a.u.)",
	6 : "d2I/dV2 (a.u.)",
	7 : "Nada",
	8 : "Nada de nada",
	9 : "Nada de nada de nada",
	10 : "di_q",
	11 : "di^2_q",
	12 : "Topography (DAC 0)"
	}

	
class VerticalManipulation :
	
	def __init__(self, fname = "", plotting_mode = "V") :

		self.fname = fname
		self.fname_label = self.fname.split("\\")[-1]
		self.file = ""
		self.data = []
		self.finalTab = {}
		self.parameters = {"i" : [], "t" : [], "V" : [], "z" : []}
		self.Vertmandelay = 1
		self.VertSpecBack = 1
		self.opening_filter = []
		self.dataHeader = None
		self.plotting_mode = plotting_mode
		self.opening_file ()
		self.reading_header ()
		self.load_data ()
		self.compute_data ()
		self.plot_data ()
	

	def opening_file(self) :
	
		try :
			self.file = open(self.fname, "r")
		except:
			print "Unexpected error while opening the file."
			raise

			
	def reading_header(self) :
		
		i = " "
		n = 0
		STM_parameters = {}
		while i != "DATA\n" or "":
			i = self.file.next()
			# if i[0].isalpha() and (n > 3) and (i.split("=")[0] not in ["UserPreampCode", "HPIB_Address", "ActGainXYZ", "PSTMAFM.EXE_Date", "DATA\n"]) : # for a real reading !
			if i[0].isalpha() and (n > 3) and (i.split("=")[0] in ["Vertmandelay", "VertSpecBack"]) :
				STM_parameters[i.split("=")[0]] = double(i.split("=")[-1])
			n = n + 1

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

		for line in self.file :
			self.data.append (self.file.next().split("\t")[0:-1])
		array_width = len (self.data[0])
		try :
			self.data = hsplit (array (self.data), array_width)
		except RuntimeError :
			print ("Enable to split the read data buffer into column(s).")
			raise
		try :
			self.file.close()
		except IOError :
			print ("Enable to close the file.")
			raise
		
	def compute_data (self) :

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
	
		for i in self.finalTab :
			figure ()
			plot (self.parameters[self.plotting_mode], self.finalTab[i]["data"])
			title (self.finalTab[i]["header"])
			xlabel(_xlab[self.plotting_mode])
			ylabel(self.finalTab[i]["ylabel"])
			text (1.05, 1, self.fname_label, transform = gca().transAxes, rotation = 90)

			
			
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
				VerticalManipulation(self.fname, self.plotting)
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
