import httplib, urllib2, json, time, urlparse

end = 0
winning = 0
playerKey = "turn-phase-key"

def testGet():
    try:
        url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey
        resp = urllib2.urlopen(url).read()
        parsed = json.loads(resp)
        print json.dumps(parsed, indent=4, sort_keys=True)
        if parsed['your_turn']:
            # detectWinning(parsed)
            print "hi"
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

def testPost(action, amount):
    # bet, raise, call, check, fold
    end = 1
    url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + playerKey +'/action'
    data = None
    if action == "bet" or action == "raise":
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

def detectWinning(resp):
    winning = 1
    for player in resp['players_at_table']:
        if player['stack'] >= resp['stack']:
            winning = 0

def calculateOddsOfWinning():
    print "23%"

def runBot():
    while not end:
        testGet()
        # testPost()
        if not winning:
            time.sleep(1)

runBot()