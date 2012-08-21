"""
trails.py

Created by Robert Cadena on 2009-06-23.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from django import template
register = template.Library()

def here_now(parser, token):
	try:
		tag_name, here_name, output = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.content.split()[0]
	
	return HereNowNode(here_name, output)

register.tag('here_now', here_now)

class HereNowNode(template.Node):
	def __init__(self, here_name, output_var='here'):
		self.here_name = here_name
		self.output_var = output_var
		
	def render(self, context):
		if not context.has_key('here_now'):
			return "" 
		
		if context['here_now'] == self.here_name:
			return self.output_var
		