import httplib, urllib2, json, time, urlparse

playerKey = "turn-phase-key"

def testGet():
    time.sleep(1)
    try:
        url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey
        resp = urllib2.urlopen(url).read()
        parsed = json.loads(resp)
        print json.dumps(parsed, indent=4, sort_keys=True)
        if parsed['your_turn']:
            print "my turn"
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

def testPost(action, amount):
    url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey +'/action'
    data = None
    if action == "bet" or action == "raise":
        # data = "{'action_name': " + action + ", 'amount': " + amount + "}"
        data = "action_name=" + action + "&amount=" + amount
    else:
        data = "action_name" + action

    urlparts = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(urlparts.netloc, urlparts.port or 80)
    conn.request("POST", urlparts.path, data)
    resp = conn.getresponse()
    body = resp.read()
    parsed = json.loads(body)
    print json.dumps(parsed, indent=4, sort_keys=True)

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

testPost('bet', '10')