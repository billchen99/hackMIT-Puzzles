import json
import urllib2

data = {'ids': [12, 3, 4, 5, 6]}

req = urllib2.Request('https://captcha.delorean.codes/u/pkkao/solution')
req.add_header('Content-Type', 'application/json')
req.add_data(
{
    'solutions': [
        {
            'name': 'd38191e31e1c496110836bce98ac191c',
            'solution': 'soln'
        },
    ]
})

response = urllib2.urlopen(req, json.dumps(data))

