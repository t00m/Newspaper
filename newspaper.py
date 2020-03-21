import feedparser

# ~ sources = open('rss.txt', 'r').readlines()
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
    print(rss)
    channel, entries = get_rss_data(rss)
    # ~ header = get_chanel_info(channel)
    fieldset = set()
    for field in channel:
        fieldset.add(field)
        # ~ print(type(channel[field]))
        if isinstance(channel[field], str):
            print ("\t%s -> %s" % (field, channel[field]))
        elif isinstance(channel[field], feedparser.FeedParserDict):
            print ("\t%s" % field)
            for key in channel[field]:
                print ("\t\t%s => %s" % (key, channel[field][key]))
    print("")
    fieldsets.append(fieldset)

common_fields = set.intersection(*fieldsets)
print(common_fields)
# ~ for fieldset in fieldsets:
    # ~ print(fieldset)


    # ~ print (f['feed']['title'])
    # ~ print (f['feed']['link'])
    # ~ print (f['feed']['language'])
    # ~ print (f['feed']['rights'])
    # ~ print (f['feed']['author'])
    # ~ print (f['feed']['published'])
    # ~ print (f['feed']['updated'])
    # ~ print (f['feed']['tags'])

    # ~ for entry in f['entries']:
        # ~ for node in entry:
            # ~ print("\t%s: %s" % (node, entry[node]))

    # ~ for node in f['feed']:
        # ~ print("\t%s: %s" % (node, f['feed'][node]))
    # ~ fname = "%s.txt" % sname.lower()
    # ~ print(fname)
    # ~ with open(fname, 'w') as feed:
        # ~ feed.write(str(f))