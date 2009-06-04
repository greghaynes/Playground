import os
import urllib
import models
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app

def loginRequired(func):
  def wrapper(self, *args, **kw):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      func(self, *args, **kw)
  return wrapper

class IssueTrackerRequestHandler(webapp.RequestHandler):
	def template_path(self, filename):
		return os.path.join(os.path.dirname(__file__), 'templates/' + filename)
	def render_to_response(self, filename, template_args):
		self.response.out.write(template.render(self.template_path(filename), self.template_params(template_args)))
	def logout_url(self, path=None):
		if path:
			return users.create_logout_url(path)
		else:
			return users.create_logout_url('/')
	def template_params(self, params):
		user = users.get_current_user()
		if user:
			params['logout_url'] = self.logout_url()
			params['user'] = user
		return params

class ProjectPageRequestHandler(IssueTrackerRequestHandler):
	def project_from_tag(self, tag):
		q = models.Project.all()
		q.filter('tag =', tag)
		result = q.fetch(1)
		if len(result) == 1:
			return result[0]
		return None
	def is_member(self, project):
		q = models.UserMemberships.all()
		q.filter('user =', users.get_current_user())
		q.filter('project =', project)
		result = q.fetch(1)
		return len(result) == 1

class MainPage(IssueTrackerRequestHandler):
	def get(self):
		self.render_to_response('index.html', {})

class ProjectIssuesPage(ProjectPageRequestHandler):
	def get(self, project_tag):
		project = self.project_from_tag(project_tag)
		if project:
			args = { 'project' : project }
			if not users.get_current_user() or not self.is_member(project):
				args['can_join'] = True
			self.render_to_response('project/issues.html', args)
		else:
			'No project with tag found'
			self.render_to_response('project/issues.html', {})

class ProjectCreatePage(IssueTrackerRequestHandler):
	@loginRequired
	def get(self):
		self.render_to_response('project/create.html', {}
			)
	@loginRequired
	def post(self):
		project_name = self.request.POST.get('name')
		project_tag = self.request.POST.get('tag')
		desc = self.request.POST.get('description')
		user = users.get_current_user()
		if project_name and project_tag:
			proj = models.Project(name=project_name, tag=project_tag, creator=user)
			proj.put()
			membership = models.UserMemberships(user=user, project=proj)
			membership.put()
		self.redirect('/account/dashboard.html')

class ProjectJoinPage(ProjectPageRequestHandler):
	@loginRequired
	def get(self, project_tag):
		project = self.project_from_tag(project_tag)
		if project:
			if not self.is_member(project):
				membership = models.UserMemberships(user=users.get_current_user(), project=project)
				membership.put()
			self.redirect('/project/'+project_tag+'/issues.html')
		else:
			self.render_to_response('project/issues.html', {})	

class SignupPage(IssueTrackerRequestHandler):
	@loginRequired
	def get(self):
		self.render_to_response('account/signup.html', {}
			)

class AccountDashboardPage(IssueTrackerRequestHandler):
	@loginRequired
	def get(self):
		q = models.UserMemberships.all()
		q.filter('user =', users.get_current_user())
		result = q.fetch(10)
		projects = []
		for membership in result:
			projects.append(membership.project)
		self.render_to_response('account/dashboard.html', {
			'projects': projects})

def main():
	urls = [
			(r'/project/(.*)/issues.html', ProjectIssuesPage),
			('/project/create.html', ProjectCreatePage),
			('/project/(.*)/join.html', ProjectJoinPage),
			('/account/signup.html', SignupPage),
			('/account/dashboard.html', AccountDashboardPage),
			('/', MainPage)]
	application = webapp.WSGIApplication( urls, debug=True)
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

