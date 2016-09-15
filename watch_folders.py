import re, sys, dropbox, os, subprocess, time
import os.path
from fuzzywuzzy import process
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from slackclient import SlackClient

# Sandwich API Authorization flow
sys.path.append('/Users/sanvidpro/Desktop/sandwichvideo')
import sandwich
authy = sandwich.get_auth('/Volumes/Sandwich/assets/python/auth.csv')
token = authy['slack']['token'] 
sc = SlackClient(token)

chan = 'C12PL8TSS'
server_directory = '/Volumes/Sandwich/projects/'
project = ''

sys.path.append('/Users/sanvidpro/Desktop/sandwichvideo')
import sandwich

server_directory = '/Volumes/Sandwich/projects/'

project = raw_input("Which project's shots would you like to watch?: ")

def begin_watch(project):
    print 'Attempting to begin watcher'
    print project
    directory_watchdog(project)
    print('Now watching the shots folder for ' +str(project))
    watcher = threading.Thread(target=main())
    watcher.daemon = True
    watcher.start()
    
class directory_watch_handler(PatternMatchingEventHandler):
    patterns = ["*.mov", "*.btsv"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_created(self, event):
        self.process(event)
        try:
            new_shot = os.path.split(event.src_path)
            new_shot = new_shot[1]
            new_shot = new_shot.split('.')
            new_shot = new_shot[0]
            send_to_slack('New version of: ' +str(new_shot))
        except:
            print("You fucked something up")
        send_to_slack(event.src_path)

def directory_watchdog(project):
    path = server_directory + fuzzy_match(project) + '/editorial/_to editorial/shots/'
    print path
    observer = Observer()
    observer.schedule(directory_watch_handler(), path, recursive = True)
    observer.start()
    return project
    
def fuzzy_match(project):
    directory_listing = os.listdir(server_directory)
    dir_temp = process.extract(project,directory_listing,limit=1)
    output_directory = dir_temp[0]
    output_directory = output_directory[0]
    return output_directory
    
def send_to_slack(slackput):
    try:
        sc.rtm_send_message(chan,slackput)
    except:
        print 'Something happened while attempting to send your message to slack'
        
def main():
      
    for attempt in range(100):
        if sc.rtm_connect():
            while True:
                time.sleep(4)
        else:
            print "Couldn't connect to Slack"
            
begin_watch(project)    
main()
