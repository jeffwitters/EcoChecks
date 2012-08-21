"""
middleware.py

Created by Robert Cadena on 2009-06-23.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

def here_now(request):
		if hasattr(request, 'here_now'):
			return { 'here_now' : getattr(request, 'here_now') }
 	
		return {}