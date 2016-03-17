'''
This test file mainly test the integrations with api.

'''

from ..receiver import Receiver
from ..client import Client
from ..processor import Processor
from ..connector import Connector
from ..api import API # Because user folder is at the same level as the main.py.
from ..status import Status
from ..status import Status_OK
from ..status import Status_NOTFOUND
from ..filetype import Filetype
from ..filetype import Filetype_text
from ..filetype import Filetype_image
from ..filetype import Filetype_pdf
from ..filetype import Filetype_download

def set_up_client():
	cl = Client("uid", None, None)
	Client.client_info["uid"] = cl
	return cl

def set_up_client_msg_upload(client, key, value):
	client.msg_upload[key] = value

def test_api_received():
	cl = set_up_client()
	set_up_client_msg_upload(cl, "DEST", "/")
	ctrl = API.runControllerByClient(cl)
	assert "FILE" in ctrl.process_map
	assert ctrl.extraheader == {}

