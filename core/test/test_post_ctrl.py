from controller.post import Post

def test_post_1():
	upload = {"DEST":"/post", "name":"Jack"}
	session = {}
	po = Post(upload, session)
	po.index()
	assert po.process_map["FILE"] == "post.html"
	assert po.process_map["name"] == "Jack"
