#from fabric import state 

config.fab_hosts = ['ecochecks.org']


def hello():
    "Prints hello."
    local("echo hello")

def deploy():
    global env
    #local("rsync -aCq --include=core $(fab_host): /var/www/vhosts/ecochecks.org/app/ecocheck")
    #local("Echo whut: %s" % env.host_string)
    exclude = ['*.pyc', '.*', 'fabfile.*', 'devel_settings.*', 'local_settings.*']
    rsync_project("/var/www/vhosts/ecochecks.org/app/", delete=True, exclude=exclude)
    #run("echo hello from $(fab_host) to $(fab_user)")
   

