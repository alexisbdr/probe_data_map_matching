#! /usr/bin/env python
import csv
import numpy as np
import matplotlib.pyplot as plt

x=[]
y=[]

x1=[]
y1=[]

def probe():
  with open('../Partition6467ProbePoints.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for row in spamreader:
        if(row[0] == '3496'):
          x.append(row[3])
          y.append(row[4])
        # print 'latitude=',row[3]
        # print 'latitude=',Decimal(row[3])
        # break
          # print float(row[3])
  print x[-1], y[-1]
  plt.scatter(x, y)
  plt.show()
  

def link():
  with open('../probe_data_map_matching/Partition6467LinkData.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for row in spamreader:
          a = row[14].split("|")
          i = a[0].split("/")
          # x.append(i[0])
          # y.append(i[1])
          j = a[-1].split('/')

          x.append(j[0])
          y.append(j[1])
          print "ref ",i," nref", j, d
  plt.scatter(x,y)
  plt.show()



def main():
  probe()
  # link()


if __name__=="__main__":
  main()
