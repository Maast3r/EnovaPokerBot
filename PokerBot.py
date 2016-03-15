import urllib, urllib2, json

playerKey = "deal-phase-key"

def testGet():
    try:
        resp = urllib2.urlopen('https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey).read()
        parsed = json.loads(resp)
        print json.dumps(parsed, indent=4, sort_keys=True)
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

def testPost(action):
    url_2 = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey +'/' + action
    req = urllib2.Request(url_2)
    rsp = urllib2.urlopen(req)
    content = rsp.read()

    print content

def deal():
    print 'deal'

def flop():
    print 'flop'

def turn():
    print 'turn'

def river():
    print 'river'

def calculateOddsOfWinning():
    print "23%"

testGet()