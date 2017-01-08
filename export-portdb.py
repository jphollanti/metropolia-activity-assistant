"""
Exports port db from portsdb.com and cleans the data to suite our needs.
"""

from __future__ import division
import urllib2, json
from time import sleep

def to_degrees(degrees, minutes, indicator):
    """
    Degrees = (+/-) Degrees + minutes/60 + seconds/3600
    We don't have seconds.
    """
    d = degrees + minutes/60
    if indicator == 'S' or indicator == 'W':
        return -d
    return d


outfile = "ports.json"
url = "http://www.portsdb.com/api/ports/"
#url = "http://www.portsdb.com/api/ports/?page=580"
sleep_between_queries = 1
ports = []
discard_keys = ('alternative_name', 'country_url', 'daylight_saving_time', 'id', 'latitude_decimal', 'longitude_decimal'
                , 'status', 'timezone', 'unlocode', 'url', 'full_port_name', 'country'
                , 'latitude_degrees', 'latitude_minutes', 'latitude_indicator'
                , 'longitude_degrees', 'longitude_minutes', 'longitude_indicator')
while(url):
    print "fetching ports from",url
    request = urllib2.Request(url)
    request.add_header("Authorization", "Token <INSERT_TOKEN>")
    response = urllib2.urlopen(request);
    data = json.loads(response.read())
    for datum in data['results']:
        if datum['latitude_degrees'] and datum['latitude_minutes'] and datum['latitude_indicator'] and datum['longitude_degrees'] and datum['longitude_minutes'] and datum['longitude_indicator']:
            datum['lat'] = to_degrees(datum['latitude_degrees'], datum['latitude_minutes'], datum['latitude_indicator'])
            datum['lng'] = to_degrees(datum['longitude_degrees'], datum['longitude_minutes'], datum['longitude_indicator'])
        for key in discard_keys:
            datum.pop(key, None)
    ports = ports + data['results']

    url = data['next'];
    sleep(sleep_between_queries)

with open(outfile, mode='w') as f:
    json.dump(ports, f)
