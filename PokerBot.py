import httplib, urllib2, json, time, urlparse

end = 0
winning = 0
getKey = "turn-phase-key"
postKey = 'river-phase-key'

values = {'1': 1, '2': 2, '3': 3,
          '4': 4, '5': 5, '6': 6,'7': 7, '8': 8,
          '9': 9,'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def testGet():
    try:
        url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + getKey
        resp = urllib2.urlopen(url).read()
        parsed = json.loads(resp)
        print json.dumps(parsed, indent=4, sort_keys=True)
        if not parsed['lost_at']:
            if parsed['your_turn']:
                # detectWinning(parsed)
                calculateOddsOfWinning(parsed)
        else:
            end=1
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

def testPost(action, amount):
    # bet, raise, call, check, fold
    end = 1
    url = 'https://enova-no-limit-code-em.herokuapp.com/sandbox/players/' + postKey +'/action'
    data = None
    if action == "bet" or action == "raise":
        data = "action_name=" + action + "&amount=" + amount

    else:
        data = "action_name=" + action

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

def calculateOddsOfWinning(resp):
   if resp['betting_phase' == 'deal']:
        deal(resp)
   else:
        flop(resp)

def deal(resp):
    card1 = values[resp['hand'][0][0]]
    card2 = values[resp['hand'][1][0]]
    suit1 = resp['hand'][0][1]
    suit2 = resp['hand'][1][1]

    if card1 > card2:
        if suit1 == suit2:
            playOn(resp, 0)
        else:
            if card1 < 4:
                testPost('fold', 0)
            else:
                playOn(resp, 0)
    elif card2 > card1:
        if suit1 == suit2:
            playOn(resp, 0)
        else:
            if card2 < 4:
                testPost('fold', 0)
            else:
                playOn(resp, 0)
    else:
        playOn(resp, int(resp['current_bet']/10))

def playOn(resp, amount):
    if amount > 0:
        testPost('raise', str(amount))
        if resp['call_amount']:
            testPost('call', 0)
        else:
            testPost('raise', str(0))

def runBot():
    while not end:
        testGet()
        # testPost()
        if not winning:
            time.sleep(1)
            break
        break

runBot()