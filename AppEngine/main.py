from flask import Flask
from flask_assistant import Assistant, ask, tell
import boto3
import random
import traceback
import os
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger=logging.getLogger()
logger.setLevel(logging.INFO) 

aDict={}
logger = logging.getLogger()
qTable = []
qTablesize = 0

app = Flask(__name__)
assist = Assistant(app, route='/')

@app.before_first_request
def abc():
    logger.info("Initializing Table")
    initTable()

@app.route('/test')
def test():
    logger.info("Vishal: Accessed Test")
    return "Hello!"

def getquotes(mode):
  logger.info("Vishal: In getquotes function")
  rnum = random.randint(0, qTablesize - 1)
  resp = qTable[rnum]['Quote']
  logger.info(qTable[rnum])

  aid = int(qTable[rnum]['AuthorID'])


  logger.info("Vishal: From getquotes() mode:"+mode + " Response:"+resp+" Author ID: "+str(aid))
  author = aDict[aid]
  logger.info("Vishal: Author Json: "+str(author))
  auth = author['AuthorName']
  logger.info("Quote is"+resp+" by "+auth)

  if mode == "initial":
    response = "Hello! Welcome to Berkshire Quotes! Here's a quote from " + auth + ", " + resp + ". Would you like another quote?"
  else:
    response = "Ok, here's another quote from " + auth + ", " + resp + ". Would you like another quote?"
  logger.info(response)
  return response

def getquotesbyAuthor(mode, authID):
    logger.info("Vishal: In getquotesbyAuthor function")
    rnum = 0
    aid = 0
    while True:
        rnum = random.randint(0, qTablesize - 1)
        aid = int(qTable[rnum]['AuthorID'])
        if aid == authID:
            break
    resp = qTable[rnum]['Quote']
    author = aDict[aid]['AuthorName']
    response = "Hello! Welcome to Berkshire Quotes! Here's a quote from " + author + ", " + resp + ". Would you like another quote?"
    return response

def initTable():
    logger.info("Vishal: Now initTable function")
    global qTable, qTablesize, aDict
    aTable = []
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', aws_access_key_id='<INSERT_AWS_ACCESS_KEY_ID_HERE>', aws_secret_access_key = '<INSERT_AWS_SECRET_ACCESS_KEY_HERE>')
    table = dynamodb.Table('Quotes')
    lqtable = table.scan()
    qTable = lqtable['Items']
    qTablesize = lqtable['Count']
    logger.info("Size of the Quotes Table is "+str(qTablesize))

    table = dynamodb.Table('Authors')
    latable = table.scan()
    aTable = latable['Items']

    for item in aTable:
        laid = item['AuthorId']
        logger.info("laid is = "+str(laid))
        aDict[laid] = item
    logger.info(str(aDict))

@assist.action('openskill')
def openskill():
  logger.info("Vishal: Now in openskill")
  try:
    initTable()
    return ask(getquotes("initial"))
  except:
    logger.info("Vishal: An error occured in openskill")
    traceback.print_exc()
    return tell("Sorry, an error occured while accessing our servers. Please try a little later.")

@assist.action('startskill')
def startskill():
  logger.info("Vishal: Now in startskill")
  try:
    initTable()
    return ask(getquotes("initial"))
  except:
    logger.info("Vishal: An error occured in startskill")
    traceback.print_exc()
    return tell("Sorry, an error occured while accessing our servers. Please try a little later.")

@assist.action('startskillwithAuthor',mapping={'author':'author'})
def startskillwithAuthor(author):
  logger.info("Vishal: Now in startskillwithAuthor")
  aid = 1
  try:
    initTable()
    if author == 'warren buffett':
        aid = 1
    else:
        aid = 2
    return ask(getquotesbyAuthor("initial", aid))
  except:
    logger.info("Vishal: An error occured in startskillwithAuthor")
    traceback.print_exc()
    return tell("Sorry, an error occured while accessing our servers. Please try a little later.")

@assist.action('AMAZON.YesIntent')
def yes():
    logger.info("Vishal: Now in AMAZON.YesIntent. Going to get quotes")
    return ask(getquotes("continue"))

@assist.action('AMAZON.NoIntent')
def no():
    logger.info("Vishal: Now in AMAZON.NoIntent. Closing the skill")
    return tell("Thanks for using Berkshire Quotes! Hope to see you soon!")

@assist.action('AMAZON.StopIntent')
def stop():
    logger.info("Vishal: Now in AMAZON.StopIntent. Closing the skill")
    return tell("Thanks for using Berkshire Quotes! Hope to see you soon!")

@assist.action('AMAZON.CancelIntent')
def cancel():
    logger.info("Vishal: Now in AMAZON.CancelIntent. Closing the skill")
    return tell("Thanks for using Berkshire Quotes! Hope to see you soon!")

@assist.action('AMAZON.HelpIntent')
def helpIntent():
    logger.info("Vishal: Now in AMAZON.HelpIntent. Giving help for the skill")
    return ask("This app gives you quotes by Warren Buffett and Charlie Munger. Would you like a quote?")

if __name__ == '__main__':
    app.run()
