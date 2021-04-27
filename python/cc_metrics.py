# Initializing the Cloud Controller client
from getpass import getpass
import cf_api
import json
import os
import time

debug = True

cloud_controller     = 'https://CHANGEME/'
deploy_client_id     = 'cf'
deploy_client_secret = ''
verify_ssl           = False

username = 'CHANGEME'
Password = 'CHANGEME'

proxy_host = 'CHANGEME'
proxy_port = '2878'

AppsTotalName   = 'pcf.prime.TotalApps '
ServicesTotalName = 'pcf.prime.TotalServices'
SpacesName      = 'pcf.prime.Spaces'
OrgName         = 'pcf.prime.Orgs'
AppsName        = 'pcf.prime.Apps'
ServicesName    = 'pcf.prime.Services'
OrgTotalName    = 'pcf.prime.TotalOrgs '
SpacesTotalName = 'pcf.prime.TotalSpaces '

cc = cf_api.new_cloud_controller(
    cloud_controller,
    client_id=deploy_client_id,
    client_secret=deploy_client_secret,
    username=username,
    password=Password,
).set_verify_ssl(verify_ssl)

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
    OrgTags = ' OrgName=' + r.name + ',OrgGUID="' + r.guid + '" '
    orgCounter +=1
    sendMetric('echo ' + OrgName + ' ' + str(1) + ' source=' + r.name + OrgTags)
    
sendMetric('echo ' + OrgTotalName + ' ' + str(orgCounter) + ' source=CF')

# List all spaces
res = cc.spaces().get()
spaces = res.resources
SpacesCounter = 0
for r in spaces:
    OrgGUID = r.organization_guid
    SpacesTags = ' SpacesName=' + r.name + ',SpacesGUID="' + r.guid + '",OrgGUID="' + OrgGUID + '" '
    SpacesCounter +=1
    sendMetric('echo ' + SpacesName + ' ' + str(1) + ' source=' + r.name + SpacesTags)
    
sendMetric('echo ' + SpacesTotalName + ' ' + str(SpacesCounter) + ' source=CF')

# List all applications per org
res = cc.organizations().get()
orgs = res.resources
for o in orgs:
    res = cc.apps().get()
    apps = res.resources
    AppsCounter = 0
    for r in apps:
        si = r.service_bindings_url
        si = si.replace('/v2/apps/','')
        si = si.replace('/service_bindings','')
        AppState = r.state
        AppsTags = ' AppsName=' + r.name + ',AppsGUID="' + r.guid + '",siGUID="' + si + '",state=' + AppState + ',org=' + o.name + ' '
        AppsCounter +=1
        sendMetric('echo ' + AppsName + ' ' + str(1) + ' source=' + r.name + AppsTags)
    
sendMetric('echo ' + AppsTotalName + ' ' + str(AppsCounter) + ' source=CF')

# List all service instances
res = cc.service_instances().get()
services = res.resources
ServicesCounter = 0
for r in services:
    si = r.service_bindings_url
    si = si.replace('/v2/apps/','')
    si = si.replace('/service_bindings','')
    ServiceState = r.state
    ServiceTags = ' ServiceName=' + r.name + ', ServicesGUID="' + si + '",state=' + ServiceState + ' '
    ServicesCounter +=1
    sendMetric('echo ' + ServicesName + ' ' + str(1) + ' source=' + r.name + ServiceTags)
    
sendMetric('echo ' + ServicesTotalName + ' ' + str(ServicesCounter) + ' source=CF')


# Find a stack by name
res = cc.stacks().get()
stacks = res.resource
if debug == True:
    print(stacks)