from core.basectrl import BaseCtrl
import logging

class Post(BaseCtrl):
	def __init__(self, msg_upload, session):
		super(Post, self).__init__(msg_upload, session)
		self.logger = logging.getLogger(__name__)
	def index(self):
		self.process_map["FILE"] = "post.html"
		self.process_map["name"] = self.msg["name"]
		for m in self.msg:
			self.logger.debug(m + ", " + self.msg[m])
		if "prev" not in self.session:
			self.process_map["prev"] = "no"
			self.process_map["last"] = " -- "
			self.session["prev"] = self.msg["name"]
		else:
			self.process_map["prev"] = "yes"
			self.process_map["last"] = self.session["prev"]
			self.session["prev"] = self.msg["name"]