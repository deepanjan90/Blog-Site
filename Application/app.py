from mongoengine import *
from model import *
from flask import Flask,request,current_app,render_template,redirect, url_for
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import datetime
#connect('') #connecting to local mongo db

#connecting to mongo atlas
connect('',host='')

app = Flask(__name__, static_url_path='', static_folder='web/static',template_folder='web/templates')
app.config['SECRET_KEY'] = 'sldkf'
api = Api(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

class HelloWorld(Resource):
	def get(self):
		return {'hello': 'world'}

class Login(Resource):
	def post(self):
		requestData = request.get_json(force=True)
		email = requestData['email']
		password = requestData['password']

		userObj = User.objects(email=email,password=password).first()
		if userObj is None:
			return {'login':'failed'}
		else:
			#session['user'] = email
			#session['passwd'] = password
			return {'login':'success', 'userid':str(userObj.id), 'handle':userObj.handle}

class Logout(Resource):
	def get(self):
		session['user'] = None

class Register(Resource):
	def post(self):		
		try:
			requestData = request.get_json(force=True)
			userObj = User(email=requestData['email'])
			userObj.first_name=requestData['first_name']
			userObj.last_name=requestData['last_name']
			userObj.handle=requestData['handle']
			userObj.password=requestData['password']
			userObj.save()
			#session['user'] = userObj.email
			#session['passwd'] = userObj.password
		except NotUniqueError as e:
			return {'registration':'failed', 'message': 'user alread exists'}
		except Exception as e:
			print (e)
			return {'registration':'failed', 'message': 'internal error'}

		return {'registration':'success','userid':str(userObj.id),'handle':userObj.handle}

class Users(Resource):
	def get(self,userid):
		requestData = request.get_json(force=True)

		userObj = User.objects(pk=userid).first()
		if userObj is None:
			return {'User':'failed', 'message': 'User not found'}
		else:
			return {'handle':userObj.handle}

class BlogPostSingle(Resource):
	def get(self,blogid):
		try:
			blogPost = Blog.objects(pk=blogid).first()
			return blogPost.to_json()
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostPopular(Resource):
	def get(self,page=1,limit=4):
		try:
			offset = (page - 1) * limit
			blogPost = Blog.objects().order_by('-created').skip(offset).limit(limit).fields(id=1,title=1)
			return blogPost.to_json()
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostGetByTitle(Resource):
	def get(self,title,page=1,limit=4):
		try:
			offset = (page - 1) * limit
			blogPost = Blog.objects().filter(title__icontains=title).order_by('-created').skip(offset).limit(limit)
			return blogPost.to_json()
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostGetByTag(Resource):
	def get(self,tag,page=1,limit=4):
		try:
			offset = (page - 1) * limit
			blogPost = Blog.objects(tags=tag).order_by('-created').skip(offset).limit(limit)
			return blogPost.to_json()
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostGet(Resource):
	def get(self,page=1,limit=10):
		try:
			offset = (page - 1) * limit
			blogPost = Blog.objects().order_by('-created').skip(offset).limit(limit)
			return blogPost.to_json()
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPost(Resource):
	def post(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = TextPost(title=requestData['title'], author=userObj)
				blogPost.content = requestData['content']
				blogPost.summary = requestData['summary']
				blogPost.tags = requestData['tags']
				blogPost.authorhandle = userObj.handle
				blogPost.save()
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
				if blogPost is None:
					return {'BlogPost':'failed','message':'Blog not found'}
				blogPost.update(title=requestData['title'],
					content=requestData['content'],
					summary=requestData['summary'],
					tags=requestData['tags'],
					modified=datetime.datetime.utcnow)
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

	def delete(self,userid):
		userObj = User.objects(pk=userid).first()
		if userObj is None:
			return {'BlogPost':'failed','message':'User not found'}
		else:
			requestData = request.get_json(force=True)
			blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
			if blogPost is None:
				return {'BlogPost':'failed','message':'Blog not found'}
			blogPost.delete()
			return {'BlogPost':'success'}

class BlogPostAddLike(Resource):	
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
				if blogPost is None:
					return {'BlogPost':'failed','message':'Blog not found'}
				blogPost.update(like=blogPost.like+1)
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostRemoveLike(Resource):	
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
				if blogPost is None:
					return {'BlogPost':'failed','message':'Blog not found'}
				blogPost.update(like=blogPost.like-1)
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}	

class BlogPostAddDisLike(Resource):	
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
				if blogPost is None:
					return {'BlogPost':'failed','message':'Blog not found'}
				blogPost.update(dislike=blogPost.dislike+1)
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}

class BlogPostRemoveDisLike(Resource):	
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPost':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['id'],author=userObj).first()
				if blogPost is None:
					return {'BlogPost':'failed','message':'Blog not found'}
				blogPost.update(dislike=blogPost.dislike-1)
				return {'BlogPost':'success'}
		except Exception as e:
			print (e)
			return {'BlogPost':'failed','message':'Internal Error'}	

class BlogPostCommentCount(Resource):	
	def get(self,blogid):
		try:
			blogPost = Blog.objects(pk=blogid).first()
			if blogPost is None:
				return {'BlogPostComment':'failed','message':'Blog not found'}
			
			comments = Comment.objects(blog=blogPost)
			return {'count':len(comments)}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class BlogPostCommentGet(Resource):	
	def get(self,blogid,page=1,limit=10):
		try:
			blogPost = Blog.objects(pk=blogid).first()
			if blogPost is None:
				return {'BlogPostComment':'failed','message':'Blog not found'}
			offset = (page - 1) * limit
			comments = Comment.objects(blog=blogPost).skip(offset).limit(limit)
			return comments.to_json()
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class BlogPostComment(Resource):
	def post(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				
				comment = Comment(author=userObj,blog=blogPost)
				comment.authorhandle = userObj.handle
				comment.content = requestData['content']
				comment.save()
				blogPost.commentcount = Comment.objects(blog=blogPost).count()
				blogPost.save()
				return {'BlogPostComment':'success','comment':comment.to_json()}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj,blog=blogPost).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.content = requestData['content']
				commentObj.modified=datetime.datetime.utcnow
				print(commentObj.modified)
				commentObj.save()
				return {'BlogPostComment':'success','comment':commentObj.to_json()}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

	def delete(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj,blog=blogPost).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.delete()
				blogPost.commentcount = Comment.objects(blog=blogPost).count()
				blogPost.save()
				return {'BlogPostComment':'success'}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class CommentAddLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.like = commentObj.like + 1;
				commentObj.save()
				return {'BlogPostComment':'success'}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class CommentRemoveLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.like = commentObj.like - 1;
				commentObj.save()
				return {'BlogPostComment':'success'}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class CommentAddDisLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.dislike = commentObj.dislike + 1;
				commentObj.save()
				return {'BlogPostComment':'success'}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class CommentRemoveDisLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'BlogPostComment':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				blogPost = Blog.objects(pk=requestData['blogid']).first()
				if blogPost is None:
					return {'BlogPostComment':'failed','message':'Blog not found'}
				commentObj = Comment.objects(pk=requestData['commentid'],author=userObj).first()
				if commentObj is None:
					return {'BlogPostComment':'failed','message':'comment not found'}
				commentObj.dislike = commentObj.dislike - 1;
				commentObj.save()
				return {'BlogPostComment':'success'}
		except Exception as e:
			print (e)
			return {'BlogPostComment':'failed','message':'Internal Error'}

class CommentReply(Resource):	
	def get(self,userid,commentid,page=1,limit=1):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				commentObj = Comment.objects(pk=commentid).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				
				replies = Reply.objects(author=userObj,comment=commentObj)
				return comments.to_json()
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

	def post(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				
				reply = Reply(author=userObj,comment=commentObj)
				reply.authorhandle = userObj.handle
				reply.content = requestData['content']
				reply.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.content = requestData['content']
				replyObj.modified = datetime.datetime.utcnow
				replyObj.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

	def delete(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.delete()
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

class ReplyAddLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.like = replyObj.like + 1;
				replyObj.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

class ReplyRemoveLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.like = replyObj.like - 1;
				replyObj.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

class ReplyAddDisLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.dislike = replyObj.dislike + 1;
				replyObj.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

class ReplyRemoveDisLike(Resource):
	def put(self,userid):
		try:
			userObj = User.objects(pk=userid).first()
			if userObj is None:
				return {'CommentReply':'failed','message':'User not found'}
			else:
				requestData = request.get_json(force=True)
				commentObj = Comment.objects(pk=requestData['commentid']).first()
				if commentObj is None:
					return {'CommentReply':'failed','message':'Comment not found'}
				replyObj = Reply.objects(pk=requestData['replyid'],author=userObj,comment=commentObj).first()
				if replyObj is None:
					return {'CommentReply':'failed','message':'reply not found'}
				replyObj.dislike = replyObj.dislike - 1;
				replyObj.save()
				return {'CommentReply':'success'}
		except Exception as e:
			print (e)
			return {'CommentReply':'failed','message':'Internal Error'}

#test API
api.add_resource(HelloWorld, '/hello')

#User
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Users, '/user/handle/<string:userid>')

#Blog
api.add_resource(BlogPostGetByTitle,'/blogpost/get/title/<string:title>','/blogpost/get/title/<string:title>/<int:page>/<int:limit>')
api.add_resource(BlogPostGetByTag,'/blogpost/get/tag/<string:tag>','/blogpost/get/tag/<string:tag>/<int:page>/<int:limit>')
api.add_resource(BlogPostPopular,'/blogpost/popular','/blogpost/popular/<int:page>/<int:limit>')
api.add_resource(BlogPostGet,'/blogpost/get','/blogpost/get/<int:page>/<int:limit>')
api.add_resource(BlogPost, '/blogpost/<string:userid>')
api.add_resource(BlogPostSingle, '/blogpost/single/<string:blogid>')
api.add_resource(BlogPostAddLike, '/blogpost/like/<string:userid>')
api.add_resource(BlogPostRemoveLike, '/blogpost/removelike/<string:userid>')
api.add_resource(BlogPostAddDisLike, '/blogpost/dislike/<string:userid>')
api.add_resource(BlogPostRemoveDisLike, '/blogpost/removedislike/<string:userid>')

#Comment
api.add_resource(BlogPostCommentCount, '/blogpost/comment/count/<string:blogid>')
api.add_resource(BlogPostCommentGet, '/blogpost/comment/get/<string:blogid>','/blogpost/comment/get/<string:blogid>/<int:page>/<int:limit>')
api.add_resource(BlogPostComment, '/blogpost/comment/<string:userid>')
api.add_resource(CommentAddLike, '/blogpost/comment/like/<string:userid>')
api.add_resource(CommentRemoveLike, '/blogpost/comment/removelike/<string:userid>')
api.add_resource(CommentAddDisLike, '/blogpost/comment/dislike/<string:userid>')
api.add_resource(CommentRemoveDisLike, '/blogpost/comment/removedislike/<string:userid>')

#Reply
api.add_resource(CommentReply, '/blogpost/reply/<string:userid>','/blogpost/comment/<string:userid>/<string:commentid>','/blogpost/comment/<string:userid>/<string:commentid>/<int:page>/<int:limit>')
api.add_resource(ReplyAddLike, '/blogpost/reply/like/<string:userid>')
api.add_resource(ReplyRemoveLike, '/blogpost/reply/removelike/<string:userid>')
api.add_resource(ReplyAddDisLike, '/blogpost/reply/dislike/<string:userid>')
api.add_resource(ReplyRemoveDisLike, '/blogpost/reply/removedislike/<string:userid>')

@app.route("/home")
def home():  
    return render_template('index.html')
    '''blogid = '5aa8ad9d4e921210c81b5c97'
    return redirect(url_for('blog',blogid=blogid))'''

@app.route("/blog/<blogid>")
def blog(blogid):  
    return render_template('single.html', blogid=blogid)

@app.route("/blog/tag/<tag>")
def blogtag(tag):  
    return render_template('blog-tag.html', tag=tag)

@app.route("/blog/title/<title>")
def blogtitle(title):  
    return render_template('blog-title.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)