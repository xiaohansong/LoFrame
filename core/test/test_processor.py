"""
This test file tests about:
1. core.config.py
2. core.receiver.py
3. core.processor.py
"""
from ..receiver import Receiver
from ..client import Client
from ..processor import Processor
from ..connector import Connector
from ..config import Config

class TestProcessor():

	def get_config(self):
		config = Config()
		return config.config_directory

	def test_config(self):
		config_directory = self.get_config()
		assert "E404" in config_directory
		assert "ROOT" in config_directory
		assert "PORT" in config_directory

	def test_client_process(self):
		# add Receiver parameter
		root_head = "GET / HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nCookie: uuid=\"7f684085-da58-407b-9663-a7488680078e\"\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		r.cl.msg_upload = msg_up
		r.cl.upload_ready = True
		assert r.cl.msg_upload['DEST'] == '/'
		default_req = self.get_config()['DEF']
		assert default_req == "index"
		p = Processor(r.cl)
		p.process()
		assert type(p.filetype).__name__ == "Filetype_text"
		assert type(p.filetype.status).__name__ == "Status_OK"
		assert "</html>" in p.filetype.body
		assert "</html>" in p.filetype.sendinfo()
		assert "text" in p.filetype.sendinfo()
		#check header
		assert p.filetype.header.connection_line == "Connection: close\r\n"
		#check session list
		assert r.cl != None
		b = False
		for key,value in Client.client_info.iteritems():
			if r.cl == value:
				b = True
		assert b

	def test_file_process(self):
		root_head = "GET /Olympic-logo.png HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nCookie: uuid=\"7f684085-da58-407b-9663-a7488680078e\"\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		r.cl.msg_upload = msg_up
		r.cl.upload_ready = True
		assert r.cl.msg_upload['DEST'] == '/Olympic-logo.png'
		default_req = self.get_config()['DEF']
		assert default_req == "index"
		p = Processor(r.cl)
		p.process()
		assert type(p.filetype).__name__ == "Filetype_image"


	def test_client_process_messed_input(self):
		root_head = "  "
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		assert msg_up == None
		cl = Client(None, None, None)
		cl.msg_upload = msg_up
		cl.upload_ready = True
		p = Processor(cl)
		p.process()
		assert p.filetype == None
		for key,value in Client.client_info.iteritems():
			assert cl != value

	def test_receiver_process(self):
		root_head = "GET / HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nCookie: uuid=\"7f684085-da58-407b-9663-a7488680078e\"\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		assert "DEST" in msg_up
		assert len(Client.client_info) != 0
		assert Client.client_info.get("7f684085-da58-407b-9663-a7488680078e", None) != None
		assert "METHOD" in msg_up
		assert msg_up.get("DEST", None) == '/'
		assert msg_up.get("METHOD", None) == 'GET'

	def test_post_receiver_process(self):
		root_head = "POST /submit/success HTTP/1.1\r\nHost: localhost:5784\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nCookie: uuid='be7f855c-1ad1-4273-ad2d-62cbd0826340'\r\nContent-Length: 45\r\n\r\nname=test&email=sxhan92%40gmail.com&code=teco"	
		
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		assert "DEST" in msg_up
		assert len(Client.client_info) != 0
		assert Client.client_info.get("7f684085-da58-407b-9663-a7488680078e", None) != None
		assert "METHOD" in msg_up
		assert msg_up.get("DEST", None) == '/submit/success'
		assert msg_up.get("METHOD", None) == 'POST'
		assert msg_up.get("name", None) == "test"
		assert msg_up.get("email", None) == "sxhan92@gmail.com"
		assert msg_up.get("code", None) == "teco"


	def test_receiver_process_nouuid(self):
		root_head = "GET / HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		assert len(Client.client_info) != 0
		assert "DEST" in msg_up
		assert "METHOD" in msg_up
		assert msg_up.get("DEST", None) == '/'
		assert msg_up.get("METHOD", None) == 'GET'

	def test_receiver_junk_message(self):
		empty_head = ""
		r = Receiver(None,None,None)
		msg_up = r.process(empty_head)
		assert msg_up == None
		curly_head = "{}"
		r = Receiver(None,None,None)
		msg_up = r.process(curly_head)
		assert msg_up == None

	def test_receiver_split_get_message(self):
		root_head = "GET /post.html?var1=20&var2=comeon HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head)
		assert "var1" in msg_up
		assert "var2" in msg_up
		assert msg_up["DEST"] == "/post.html"
		assert msg_up["var1"] == "20"
		assert msg_up["var2"] == "comeon" 
		
		root_head2 = "GET /errorinput?var1=&var2= HTTP/1.1\r\nUser-Agent: curl/7.37.1\r\nHost: localhost:5783\r\nAccept: */*\r\n\r\n"
		r = Receiver(None,None,None)
		msg_up = r.process(root_head2)
		assert "var1" in msg_up
		assert "var2" in msg_up
		assert msg_up["DEST"] == "/errorinput"
		assert msg_up["var1"] == ""
		assert msg_up["var2"] == "" 
