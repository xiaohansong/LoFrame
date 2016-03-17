from core.basectrl import BaseCtrl

class Root(BaseCtrl):
	def __init__(self, msg_upload, session):
		super(Root, self).__init__(msg_upload, session)

	def index(self):
		self.process_map["FILE"] = "index.html"
		self.process_map["greet"] = "Hello"