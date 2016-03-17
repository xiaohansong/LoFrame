from controller.submit import Submit

def test_submit_1():
	upload = {"DEST":"/submit"}
	session = {}
	sb = Submit(upload, session)
	sb.index()
	assert sb.process_map["FILE"] == "submit.html"
