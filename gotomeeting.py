# encoding: utf-8

import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

def get_authcode():

  HOST = 'localhost'
  PORT = 8123

  #client_id='29eGiSvJtwpgPAo3sP8SPF76oN4Cce7e',
  #client_secret='your_client_secret',
  #scope='https://api.citrixonline.com/oauth/authorize',
  #redirect_uri="http://{}:{}".format( HOST, PORT ) )

def main(wf):

  import re

  # build argument parser to parse script args and collect their
  # values
  parser = argparse.ArgumentParser()
  
  # add an optional (nargs='?') --apikey argument and save its
  # value to 'apikey' (dest). This will be called from a separate "Run Script"
  # action with the API key
  parser.add_argument( '--setkey', dest='apikey', nargs='?', default=None )

  # add an optional query and save it to 'query'
  parser.add_argument( 'query', nargs='?', default=None )

  # parse the script's arguments
  args = parser.parse_args(wf.args)

  ####################################################################
  # Save the provided API key
  ####################################################################

  # decide what to do based on arguments
  if args.apikey:
  
    log.info ( "Preparing to determine API keys" )
  
    # https://api.citrixonline.com/oauth/authorize?client_id=29eGiSvJtwpgPAo3sP8SPF76oN4Cce7e

    wf.save_password('gtm_api_key', args.apikey)
    
    return 0

  ####################################################################
  # Check that we have an API key saved
  ####################################################################

  try:
  
    api_key = wf.get_password('gtm_api_key')
    
  except PasswordNotFound:  # API key has not yet been set

    wf.add_item('No API key set.',
                'Please use gtm set host to set your GoToMeeting host id.',
      valid=False,
      icon=ICON_WARNING)
      
    wf.send_feedback()
      
    return 0

  query = args.query

  # Get query from Alfred
  if len(query):
  
    meeting = re.sub( r"-", "", re.sub( r"\s+", "", query ) )

    wf.add_item(title=str.format( "Join GoToMeeting {}", meeting ),
      subtitle=meeting,
      arg=meeting,
      largetext=meeting,
      valid=(len(meeting)==9))
            
    wf.send_feedback()

  if len(api_key):
  
    meeting = re.sub( r"-", "", re.sub( r"\s+", "", api_key ) )

    wf.add_item(title=str.format( "Host GoToMeeting {}", meeting ),
      subtitle=meeting,
      arg=meeting,
      largetext=meeting,
      valid=(len(meeting)==9))
            
    wf.send_feedback()

  return 0

if __name__ == u"__main__":

  wf = Workflow( update_settings={
    # Your username and the workflow's repo's name
    'github_slug': 'lonniev/com.predictableresponse.alfred.gotomeeting',
    'frequency': 7
  })
  
  log = wf.logger
  
  if wf.update_available:
    # Download new version and tell Alfred to install it
    # Add a notification to top of Script Filter results
    wf.add_item('New version available',
                'Action this item to install the update',
                autocomplete='workflow:update',
                icon=ICON_INFO)
  
  sys.exit(wf.run(main))