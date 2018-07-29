#!/usr/bin/env python
import csv
import probe
import link
import pickle
import sys


def read_dump():
    with open('matched_points','rb') as f:
        x = pickle.load(f)
    return x

def write_csv(data):
    with open('Partition6467MatchedPoints.csv','wb') as out:
        writer = csv.writer(out, delimiter=',',quotechar='|')
        # sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink
        for num,line in enumerate(data):
            row = line.sampleID,line.dateTime,line.sourceCode,line.latitude,line.longitude,line.altitude,line.speed,line.heading,line.linkPVID,line.direction,line.distFromRef,line.distFromLink
            writer.writerow(row)
    print "File written !"

def main():
    data = read_dump()
    write_csv(data)


if __name__=="__main__":
  main()
