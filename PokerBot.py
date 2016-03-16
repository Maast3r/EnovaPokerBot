import httplib, urllib2, json, time, urlparse

end = 0
winning = 0
getKey = "d8dfad17-957d-48c2-a746-a9dde10b1874"
postKey = 'd8dfad17-957d-48c2-a746-a9dde10b1874'

values = {'1': 1, '2': 2, '3': 3,
          '4': 4, '5': 5, '6': 6,'7': 7, '8': 8,
          '9': 9,'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def testGet():
    try:
        url = 'https://enova-no-limit-code-em.herokuapp.com/api/players/' + getKey
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
    print '--------------------------------------------------'
    # bet, raise, call, check, fold
    url = 'https://enova-no-limit-code-em.herokuapp.com/api/players/' + postKey +'/action'
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
   if resp['betting_phase'] == 'deal':
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
        playOn(resp, int(resp['current_bet'])/10)

def flop(resp):
    if int(resp['call_amount']) > 200:
        testPost('fold', 0)
    else:
        card1 = values[resp['hand'][0][0]]
        card2 = values[resp['hand'][1][0]]
        suit1 = resp['hand'][0][1]
        suit2 = resp['hand'][1][1]

        communityCard1 = values[resp['community_cards'][0][0]]
        communitysuit1 = resp['community_cards'][0][1]
        communityCard2 = values[resp['community_cards'][1][0]]
        communitysuit2 = resp['community_cards'][1][1]
        communityCard3 = values[resp['community_cards'][2][0]]
        communitysuit3 = resp['community_cards'][2][1]
        # communityCard4 = values[resp['community_cards'][3][0]]
        # communitysuit4 = resp['community_cards'][3][1]
        # communityCard5 = values[resp['community_cards'][4][0]]
        #communitysuit5 = resp['community_cards'][4][1]
        if card1 == communityCard1 or card1 == card2 or card1 == communityCard2 or card1 == communityCard3 or card2 == communityCard1 or card2 == communityCard2 or card2 == communityCard3:
            testPost('call', 0)
        else:
            testPost('fold', 0)


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
        if not winning:
            time.sleep(1)

runBot()