import feedparser

feeds = {}
sources = open('rss.txt', 'r').read().splitlines()

def get_rss_data(rss):
    try:
        f = feedparser.parse(rss)
        return f['feed'], f['entries']
    except:
        print("Error while getting data from: %s" % rss)
        return None

def get_chanel_info(channel):
    header = {}
    for field in channel:
        # Only strings
        # ~ if type(channel[field]) == str:
            # ~ header[field] = channel[field]

        # All fields:
        header[field] = channel[field]
    return header

fieldsets = []
for rss in sources:
    # ~ print(rss)
    if rss.startswith('#'):
        continue
    feeds[rss] = {}
    channel, entries = get_rss_data(rss)
    fieldset = set()
    feeds[rss]['header']={}
    for field in channel:
        fieldset.add(field)
        if isinstance(channel[field], str):
            feeds[rss]['header'][field] = channel[field]
            # ~ print ("\t%s -> %s" % (field, channel[field]))
        elif isinstance(channel[field], feedparser.FeedParserDict):
            # ~ print ("\t%s" % field)
            for key in channel[field]:
                pass
                # ~ print ("\t\t%s => %s" % (key, channel[field][key]))
    # ~ print("")
    fieldsets.append(fieldset)

# ~ common_fields = set.intersection(*fieldsets)
# ~ print ("Common fields for all RSS feeds: ")
# ~ print(common_fields)
# ~ {'links', 'subtitle', 'title', 'title_detail', 'subtitle_detail', 'link'}
for rss in feeds:
    print (feeds[rss]['header']['title'])
    # ~ print ("\t%s" % feeds[rss]['header']['title_detail'])
    print ("\t%s" % feeds[rss]['header']['subtitle'])
    # ~ print ("\t%s" % feeds[rss]['header']['subtitle_detail'])
    print ("\t%s" % feeds[rss]['header']['link'])
    print ("")
