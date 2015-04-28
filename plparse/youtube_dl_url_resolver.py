#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import youtube_dl
import  argparse
import sys

def silent_output(message, skip_eol=False, check_quiet=False):
    pass

def get_urls(url, check, debug):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    if not debug:
        ydl.to_stdout = silent_output
        ydl.to_stderr = silent_output

    if check:
        result = False
        ies = ydl._ies
        for ie in ies:
            if ie.IE_NAME == "generic":
                continue
            if debug:
                print "checking ", ie.IE_NAME
            if ie.suitable(url) and ie.working():
                if debug:
                    print ie.IE_NAME, "is suitable and is working"
                result = True
                break

        if result:
            sys.stdout.write("TRUE")
        else:
            sys.stdout.write("FALSE")
        return

    try:
        with ydl:
            result = ydl.extract_info(
                url,
                download=False # We just want to extract the info
            )
    except Exception as e:
        if debug:
            print e.message
        sys.stdout.write("TOTEM_PL_PARSER_RESULT_ERROR")
        exit(1)

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    sys.stdout.write(u''.join(("title=", video["title"])).encode('utf-8') + "\n")
    sys.stdout.write(u''.join(("id=", video["id"])).encode('utf-8') + "\n")
    sys.stdout.write(u''.join(("moreinfo=", video["webpage_url"])).encode('utf-8') + "\n")
    sys.stdout.write(u''.join(("url=", video["url"])).encode('utf-8') + "\n")
    sys.stdout.write(u''.join(("image-url=", video["thumbnail"])).encode('utf-8') + "\n")
    sys.stdout.write(u''.join(("duration=", str(float(video["duration"]) * 1000.0))).encode('utf-8') + "\n")

if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--url",
                            action="store", dest="url",
                            default="",
                            help="Url to scan or check")
    arg_parser.add_argument("-c", "--check",
                            action="store_true",
                            help="only check if the url can be scanned")
    arg_parser.add_argument("-d", "--debug",
                            action="store_true",
                            help="enable debug")

    args = arg_parser.parse_args()

    if not args.url:
        print "please specify a url to scan or check"
        exit (1)

    get_urls (args.url, args.check, args.debug)
