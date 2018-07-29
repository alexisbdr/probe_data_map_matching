#!/usr/bin/env python
import csv
import probe
import link
import sys
from six.moves import cPickle as pickle

probe_data=[]
link_data=[]

def read_probe(num = 10000):
  #reading Probe Data
  print 'Reading probe points ...', num
  with open('Partition6467ProbePoints.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for i, row in enumerate(spamreader):
          probe_obj=probe.Probe(row)
          probe_data.append(probe_obj)
          if i > num:
            break

def read_link():
    #reading Link Data
  print 'Reading link data ...'
  with open('Partition6467LinkData.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for i, row in enumerate(spamreader):
          link_obj=link.Link(row)
          link_data.append(link_obj)


def main():
  if len(sys.argv) < 2:
    print 'Number of probe points not given, using 10,000 points'
    read_probe()
  else:
    num = int(sys.argv[1])
    read_probe(num)
  read_link()

  print "Writing Probe file"
  probeObject = open('probe_data', 'wb')
  pickle.dump(probe_data, probeObject)
  probeObject.close()
  print "Writing Link file"
  linkObject = open('link_data', 'wb')
  pickle.dump(link_data, linkObject)
  linkObject.close()
  print "All done"


if __name__=="__main__":
  main()
