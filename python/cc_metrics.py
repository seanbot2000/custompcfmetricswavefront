# Initializing the Cloud Controller client
from getpass import getpass
import cf_api
import json
import os
import time

debug = True

cloud_controller     = 'https://api.sys.xxx.xxx'
deploy_client_id     = 'cf'
deploy_client_secret = ''
verify_ssl           = False

username = ''
Password = ''

proxy_host = 'localhost'
proxy_port = '2878'

metrics_pre = ''

AppsTotalName   =  metrics_pre + '.TotalApps'
ServicesTotalName = metrics_pre + '.TotalServices'
SpacesName      = metrics_pre + '.Spaces'
OrgName         = metrics_pre + '.Orgs'
AppsName        = metrics_pre + '.Apps'
ServicesName    = metrics_pre + '.Services'
OrgTotalName    = metrics_pre + '.TotalOrgs '
SpacesTotalName = metrics_pre + '.TotalSpaces '

cc = cf_api.new_cloud_controller(
    cloud_controller,
    client_id=deploy_client_id,
    client_secret=deploy_client_secret,
    username=username,
    password=Password,
    verify_ssl=verify_ssl
)

def sendMetric(metric):
    entireMetric = metric + '| nc -q0 ' + proxy_host + ' ' + proxy_port
    if debug==True:
        print(entireMetric)
    os.popen(entireMetric)

# List all organizations
req = cc.organizations()
res = req.get()
orgs = res.resources
orgCounter = 0
for r in orgs:
    OrgTags = ' OrgGUID="' + r.guid + '" OrgName=' + r.name + ' '
    orgCounter +=1
    sendMetric('echo ' + OrgName + ' ' + str(1) + ' source=' + r.name + OrgTags)
    
sendMetric('echo ' + OrgTotalName + ' ' + str(orgCounter) + ' source=CF')

# List all spaces
res = cc.spaces().get()
spaces = res.resources
SpacesCounter = 0
for r in spaces:
    OrgGUID = r.organization_guid
    SpacesTags = ' SpacesName=' + r.name + ' SpacesGUID="' + r.guid + '" OrgGUID="' + OrgGUID + '" '
    SpacesCounter +=1
    sendMetric('echo ' + SpacesName + ' ' + str(1) + ' source=' + r.name + SpacesTags)
    
sendMetric('echo ' + SpacesTotalName + ' ' + str(SpacesCounter) + ' source=CF')

# List applications
res = cc.apps().get()
apps = res.resources
AppsCounter = 0
for r in apps:
    si = r.service_bindings_url
    si = si.replace('/v2/apps/','')
    si = si.replace('/service_bindings','')
    AppState = r.state
    AppsTags = ' AppsName=' + r.name + ' AppsGUID="' + r.guid + '" siGUID="' + si + '" state="' + AppState + '" '
    AppsCounter +=1
    sendMetric('echo ' + AppsName + ' ' + str(1) + ' source=' + r.name + AppsTags)
    
sendMetric('echo ' + AppsTotalName + ' ' + str(AppsCounter) + ' source=CF')

# List all service instances
res = cc.service_instances().get()
services = res.resources
ServicesCounter = 0
for r in services:
    si = r.service_bindings_url
    si = si.replace('/service_bindings','')
    si = si.replace('/v2/service_instances/','')
    ServiceTags = ' ServiceName=' + r.name + ' ServicesGUID="' + si + '" '
    ServicesCounter +=1
    sendMetric('echo ' + ServicesName + ' ' + str(1) + ' source=' + r.name + ServiceTags)
    
sendMetric('echo ' + ServicesTotalName + ' ' + str(ServicesCounter) + ' source=CF')


# Find a stack by name
res = cc.stacks().get()
stacks = res.resource
if debug == True:
    print(stacks)
