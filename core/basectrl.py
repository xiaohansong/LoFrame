class BaseCtrl(object):
	def __init__(self, msg_upload, session):
		self.msg = msg_upload
		self.extraheader = {}
		self.session = session
		self.process_map = {}

	def file(self, filename):
		self.process_map['FILE'] = filename