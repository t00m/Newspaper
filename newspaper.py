import os
import sys
import feedparser
from concurrent.futures import ThreadPoolExecutor as Executor

feeds = {}

def get_rss_data(rss):
    try:
        f = feedparser.parse(rss)
        return rss, f['feed'], f['entries']
    except:
        print("Error while getting data from: %s" % rss)
        return None

def get_chanel_info(channel):
    header = {}
    for field in channel:
        # Only strings
        # ~ if isinstance(channel[field], str):
            # ~ header[field] = channel[field]
        # All fields:
        header[field] = channel[field]
    return header

def get_field_value(entry, field):
    try:
        return entry[field]
    except:
        return ''

def process_feeds(sources):
    fieldsets = []
    with Executor(max_workers=5) as exe:
        jobs = []
        for rss in sources:
            if rss.startswith('#'):
                continue

            job = exe.submit(get_rss_data, rss)
            print("Querying feed: %s" % rss)
            # ~ job.add_done_callback(job_done)
            jobs.append(job)


        for job in jobs:
            rss, channel, entries = job.result()
            print ("Receiving data from: %s" % channel['title'])

            # Process feed
            feeds[rss] = {}
            fieldset = set()

            ## Process feed header
            feeds[rss]['header']={}
            for field in channel:
                fieldset.add(field)
                if isinstance(channel[field], str):
                    feeds[rss]['header'][field] = channel[field]
                elif isinstance(channel[field], feedparser.FeedParserDict):
                    for key in channel[field]:
                        pass # ~ print ("\t\t%s => %s" % (key, channel[field][key]))
            fieldsets.append(fieldset)

            ## Process feed entries
            feeds[rss]['entries']={}
            for entry in entries:
                eid = entry['id']
                feeds[rss]['entries'][eid] = {}
                feeds[rss]['entries'][eid]['title'] = get_field_value(entry, 'title')
                adate = get_field_value(entry, 'published')
                if len(adate) == 0:
                    adate = get_field_value(entry, 'date')
                feeds[rss]['entries'][eid]['published'] = adate

                feeds[rss]['entries'][eid]['link'] = get_field_value(entry, 'link')
                # ~ for field in entry:
                    # ~ print ("\tField: %s" % field)

    # ~ common_fields = set.intersection(*fieldsets)
    # ~ print ("Common fields for all RSS feeds: ")
    # ~ print(common_fields)
    # ~ {'links', 'subtitle', 'title', 'title_detail', 'subtitle_detail', 'link'}
    for rss in feeds:
        print ("%s (%s)" % (feeds[rss]['header']['title'], feeds[rss]['header']['link']))
        for eid in feeds[rss]['entries']:
            title = feeds[rss]['entries'][eid]['title']
            published = feeds[rss]['entries'][eid]['published']
            link = feeds[rss]['entries'][eid]['link']
            print ("\t* %s (%s) via %s" % (title, published, link))
        # ~ print ("\t%s" % feeds[rss]['header']['subtitle'])
        # ~ print ("\t%s" % feeds[rss]['header']['link'])
        # ~ print ("")

if __name__ == '__main__':
    try:
        rss_file = sys.argv[1]
        if os.path.exists(rss_file):
            sources = open(rss_file, 'r').read().splitlines()
            process_feeds(sources)
        else:
            print ("RSS file path doesn't exist. Exit.")
    except IndexError as error:
        print("RSS file path not provided. Exit.")
