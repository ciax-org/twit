# Twit - Python script using tweepy to set notifications for all Twitter friends

## Problem

You follow `friends` like crazy on Twitter and accept suggestions of many other `friends` to follow.

Then you realize after following 1,000+ `friends` you never see their tweets; as the default is no `notifications`.  

## Solution

This utility script allows you to set `notifications` for all of them to --yes (-y) or --no (-n).

## Usage

Typical usage to allow all `notifications` from all `friends`;

```bash
python main.py --id YourTwitterScreenName --yes
```

or

```bash
python main.py -i YourTwitterScreenName -y
```

## Dependencies

tweepy - Version used 4.10.1 (others may work, this was just the latest)

## TODO

It is a good starting point for Twitter automation and allows for command like options and a config file.  

Its features could be expanded to achieve many other tasks.

A search (by profile keywords, screen_name etc.) and accept / deny `notifications` from only some or one `friend`.
