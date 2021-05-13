# Initializing the Cloud Controller client
from getpass import getpass
from cloudfoundry_client.client import CloudFoundryClient
import json
import os
import time

debug = True

cloud_controller     = '<cc api endpoint>'
foundation           = '<foundation name>'
verify_ssl           = False
proxy                = None

username = '<user>'
password = '<password>'

proxy_host = 'localhost'
proxy_port = '2878'

#tentative
namespace_prefix = 'pcf.cc-metrics.'

appsTotalName   = namespace_prefix + 'total-apps'
servicesTotalName = namespace_prefix + 'total-services'
spacesName      = namespace_prefix + 'spaces'
orgName         = namespace_prefix + 'orgs'
appsName        = namespace_prefix + 'apps'
servicesName    = namespace_prefix + 'services'
orgTotalName    = namespace_prefix + 'total-orgs '
spacesTotalName = namespace_prefix + 'total-spaces '
servicesBindingsName = namespace_prefix + 'service-bindings'
servicesBindingsTotalName = namespace_prefix + 'total-service-bindings'
servicesInstancesName = namespace_prefix + 'service-instances'
servicesInstancesTotalName = namespace_prefix + 'total-service-instances'

# Login can also use a token
client = CloudFoundryClient(cloud_controller, proxy=proxy, verify=verify_ssl)
client.init_with_user_credentials(username, password)

# Netcat dependency in the container
def sendMetric(metric):
    entireMetric = metric + '| nc -q0 ' + proxy_host + ' ' + proxy_port
    if debug==True:
        print(entireMetric)
    os.popen(entireMetric)
    

# List all organizations
orgs = client.v2.organizations
orgCounter = 0
for org in orgs:
    orgGUID = org['metadata']['guid']
    orgName = org['entity']['name']
    orgTags = ' orgGUID="' + orgGUID + '" orgName=' + orgName + ' '
    orgCounter +=1
    sendMetric('echo ' + orgName + ' ' + str(1) + ' source=' + foundation + orgTags)

sendMetric('echo ' + orgTotalName + ' ' + str(orgCounter) + ' source=' + foundation)

# List all spaces
spaces = client.v2.spaces
spacesCounter = 0
for space in spaces:
    orgGUID = space['entity']['organization_guid']
    spaceName = space['entity']['name']
    spaceGUID = space['metadata']['guid']
    spacesTags = ' spaceName=' + spaceName + ' spaceGUID="' + spaceGUID + '" orgGUID="' + orgGUID + '" '
    spacesCounter +=1
    sendMetric('echo ' + spacesName + ' ' + str(1) + ' source=' + foundation + spacesTags)

sendMetric('echo ' + spacesTotalName + ' ' + str(spacesCounter) + ' source=' + foundation)

# List applications
apps = client.v2.apps
appsCounter = 0
for app in apps:
    appState = app['entity']['state']
    appName = app['entity']['name']
    appGUID = app['metadata']['guid']
    spaceGUID = app['entity']['space_guid']
    diskQuota = app['entity']['disk_quota']
    appTags = ' appName=' + appName + ' appGUID="' + appGUID + '" state="' + appState + '"' + ' diskQuota=' + str(diskQuota) + ' spaceGUID="' + spaceGUID + '" '
    appsCounter +=1
    sendMetric('echo ' + appsName + ' ' + str(1) + ' source=' + foundation + appTags)

sendMetric('echo ' + appsTotalName + ' ' + str(appsCounter) + ' source=' + foundation)

# List all services
services = client.v2.services
servicesCounter = 0
for service in services:
    serviceName = service['entity']['label']
    serviceGUID = service['metadata']['guid']
    serviceTags = ' serviceName=' + serviceName + ' serviceGUID="' + serviceGUID + '" '
    servicesCounter +=1
    sendMetric('echo ' + servicesName + ' ' + str(1) + ' source=' + foundation + serviceTags)

sendMetric('echo ' + servicesTotalName + ' ' + str(servicesCounter) + ' source=' + foundation)

# List all service bindings
serviceBindings = client.v2.service_bindings
serviceBindingsCounter = 0
for sb in serviceBindings:
    sbGUID = sb['metadata']['guid']
    siGUID = sb['entity']['service_instance_guid']
    appGUID = sb['entity']['app_guid']
    sbTags = ' sbGUID="' + sbGUID + ' siGUID="' + siGUID + ' appGUID="' + appGUID + '" '
    serviceBindingsCounter +=1
    sendMetric('echo ' + servicesBindingsName + ' ' + str(1) + ' source=' + foundation + sbTags)

sendMetric('echo ' + servicesBindingsTotalName + ' ' + str(serviceBindingsCounter) + ' source=' + foundation)

# List all service instances
serviceInstances = client.v2.service_instances
serviceInstancesCounter = 0
for si in serviceInstances:
    siGUID = si['metadata']['guid']
    serviceGUID = si['entity']['service_guid']
    siTags = ' siGUID="' + siGUID + ' serviceGUID="' + serviceGUID + ' '
    serviceInstancesCounter +=1
    sendMetric('echo ' + servicesInstancesName + ' ' + str(1) + ' source=' + foundation + siTags)
