import importlib
from config import Config
import logging
class API(object):
	logger = logging.getLogger(__name__)
	@staticmethod
	def runControllerByClient(client):
		raw_request = client.msg_upload["DEST"]
		# split request by '/' to get the path_info.
		API.logger.info("requested: " + raw_request)
		path_info = raw_request.split('/')
		controller = ""
		request = ""
		ctrl = None
		conf = Config()
		default_req = conf.config_directory["DEF"]
		default_ctrl = conf.config_directory['DCON']
		if path_info[1] == '':
			# the request is root directory. Ask for default controller.
			controller = default_ctrl
			request = "/" + default_req
		else:
			# select the first part of path as the controller name.
			if "." in path_info[1]:
				controller = default_ctrl
				request = "/" + path_info[1]
			else:
				controller = path_info[1]			
				request = raw_request[len(controller) + 1:]
				if len(request) <= 1:
					request = "/" + default_req
		API.logger.debug("controller: " + controller)
		try:
			control_module = importlib.import_module("controller." + controller)
			ctrl = getattr(control_module, controller[0].upper() + controller[1:])
		except Exception:
			# for undefined behavior, go to E404 Not Found.
			API.logger.exception("importlib exception")
			return None
		#Controller should take msg_upload and session. 
		ctrl_obj = ctrl(client.msg_upload, client.session)
		try:
			API.logger.debug(request[1:])
			if '.' in request[1:]:
				# this is a file.
				eval("ctrl_obj.file('" +request[1:] + "')")
			else:
				eval("ctrl_obj." + request[1:] + "()")
		except Exception:
			API.logger.exception("Process exception")
			return None
		return ctrl_obj