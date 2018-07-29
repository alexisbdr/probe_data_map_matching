#! /usr/bin/env python
import csv
import numpy as np
import matplotlib.pyplot as plt
import probe
import link
import link_dist
from shapely.geometry import LineString as line, Point as point
import math
import matched_point
import pickle
import write_data
import sys
from numpy.polynomial import Polynomial

x=[]
y=[]
#
# x1=[]
# y1=[]

probe_data=[]
link_data=[]
matched_data=[]



def read_probe():
  #reading Probe Data
    print 'reading probe points ...'
    with open('Partition6467ProbePoints.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i=0
        for row in spamreader:
            probe_obj=probe.Probe(row)
            probe_data.append(probe_obj)
            # x.append(probe_obj.longitude)
            # y.append(probe_obj.latitude)

            # print 'No=',i,'latitude=',probe_obj.latitude,'longitude=', probe_obj.longitude
            i=i+1
            if i>100:
                break
            # print '\n'

    # plt.scatter(x,y)
    # plt.show()



def read_link():
    #reading Link Data
  print 'reading link data ...'
  with open('Partition6467LinkData.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      i=0
      for row in spamreader:
          # print 'row_length=',row[16]
          link_obj=link.Link(row)


          # for shape_point in link_obj.shape_points:
          #     x.append(shape_point.longitude)
          #     y.append(shape_point.latitude)
          #     print 'No=',i,'latitude=', shape_point.latitude, 'longitude=', shape_point.longitude

         #For displaying nodes only
          # x.append(link_obj.reference_node.longitude)
          # y.append(link_obj.reference_node.latitude)
          # print 'No=', i, 'latitude=', link_obj.reference_node.latitude, 'longitude=', link_obj.reference_node.longitude
          #
          # x.append(link_obj.non_reference_node.longitude)
          # y.append(link_obj.non_reference_node.latitude)
          # print 'No=', i, 'latitude=', link_obj.non_reference_node.latitude, 'longitude=', link_obj.non_reference_node.longitude

          i=i+1
          # print type(link_obj.reference_node.latitude)
          link_data.append(link_obj)


def distance(p_x, p_y, line_points):
  # l = line([(1, 1), (-1,1)])
  link_line = line(line_points)
  p = point(p_x,p_y)
  return p.distance(link_line)


def search_link(num, precision = 0.001):
  '''
  arguments
   num: The probe_data point in the probe_data array.
   precision: size of the filter box, 2nd decimal places corresponds to around 1 Km
  This function takes in one probe point and does the following:
   1. Taking one link at a time, it filters out the links whose shape points are not within a specified range
   2. For the selected ink, it buils a linear approximation, considering all shape points and calculates the
   minimum distance of the probe point from the link.
   3. The link ID and the distance from that link is stored in respective arrays.
  Call this function recusrsively to evaluate multiple probe points.
  '''
  dist=[]
  link_id = []
  for item in link_data:
    flag = 0
    line_points=[]
    links=[]
    for pt in item.shape_points:
      if abs(pt.latitude - probe_data[num].latitude) < precision and abs(pt.longitude - probe_data[num].longitude) < precision:
        flag = 1
      else:
        continue
    if flag!=0:
      link_id.append(item.linkPVID)
      links.append(item)
      for pt in item.shape_points:
        line_points.append((pt.latitude,pt.longitude))
      dist.append(distance(probe_data[num].latitude, probe_data[num].longitude, line_points))
    else:
      continue
  out = sorted(zip(link_id,dist), key=lambda x:x[1])
  probe_data[num].update_link_info(out)
  return out

def calculate_heading_diff(point, link):
    min=10000
    # plot_point_n_links(point, [link])

    heading=point.heading*1
    for angle in link.angles:
        diff= abs(angle-int(point.heading))
        if diff <min:
            min=diff
    return min

# plots a point with the given set of links for comparison
def plot_point_n_links(pnt,links):
    for link in links:
        lon = []
        lat = []
        for shapepoint in link.shape_points:

            lon.append(shapepoint.longitude)
            lat.append(shapepoint.latitude)
        plt.plot(lon, lat, 'ro-')
    plt.plot(pnt.longitude, pnt.latitude, 'ro-', color='blue')
    # plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    # plt.show()

def plot_point_n_links_highlight(pnt,links,minlink):

    for link in links:
        lon = []
        lat = []
        for shapepoint in link.shape_points:

            lon.append(shapepoint.longitude)
            lat.append(shapepoint.latitude)
        plt.plot(lon, lat, 'ro-')
    lon = []
    lat = []
    for shapepoint in minlink.shape_points:

        lon.append(shapepoint.longitude)
        lat.append(shapepoint.latitude)
    plt.plot(lon, lat, 'ro-',color='green')
    plt.plot(pnt.longitude, pnt.latitude, 'ro-', color='blue')
    
def distance_calc(node1,node2):
    x1=node1.longitude
    x2=node2.longitude
    y1 = node1.latitude
    y2 = node2.latitude
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def slope_cal(link_obj,matched_array):
  '''
  argument:
    link_obj : The link object
  '''
  x =[]
  y =[]
  z= []
  dist = []
  for item in matched_array:
    if item.linkPVID == link_obj.linkPVID:
      x.append(item.latitude)
      y.append(item.longitude)
      z.append(item.altitude)
      dist.append(item.distFromRef)

  y2 = link_obj.reference_node.longitude
  x2 = link_obj.reference_node.latitude
  '''
  x1,y1 = np.array(x), np.array(y)
  p = Polynomial.fit(x1, y1, 4)
  x1,y1  = p.linspace()
  # calculating slope at ref node
  # searching for the point closest to ref node and getting its index in array x
  # ind =  a.index(min(a, key=lambda x:abs(math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))))
  dist  = math.sqrt((x1[0]-x2)**2+(y1[0]-y2)**2)
  for i,a,b in enumerate(zip(x1,y1)):
    new_dist  = math.sqrt((a-x2)**2+(b-y2)**2)
    if new_dist < dist:
      dist = new_dist
      ind = i
    else:
      pass
  #  now i is the index of the closest point to reference node
  slope_ref = (z[i+1] - x[i])
  '''
  # searching for the point closest to ref node and getting its index in array x
  # for a,b in zip(x,y):
  #   i=a-x2
  #   dist.append(math.sqrt((a-x2)**2+(b-y2)**2))
  out = sorted(zip(x,y,z,dist), key=lambda x:x[3])
  slope_ref=0
  if len(out)>1:
      # x_cl, y_cl, z_cl, dist_cl = out[0]
      lat1=float(out[-1][0])
      lon1= float(out[-1][1])
      lat2=float(out[0][0])
      lon2=float(out[0][1])
      distance=distance_meters(lat1, lon1, lat2, lon2)
      # slope_ref = (float(out[-1][2]) - float(out[0][2]))/(math.sqrt((float(out[-1][0]) - float(out[0][0]))**2+(float(out[-1][1])-float(out[0][1]))**2))
      slope_ref = (float(out[-1][2]) - float(out[0][2]))/distance

  return slope_ref# def main():
#   read_probe()
#
#
#
#   read_link()
#
#   print 'The number of links is ' ,len(link_data)
#   probe_data_length=len(probe_data)
#   for i, probe in enumerate(probe_data):
#       print i,'/',len(probe_data)
#       # input_point=probe_data[probe_index]
#       # print input_point.latitude, input_point.longitude
#
#       out = search_link(i)
#
#       print len(out)
#
#       links_plot=[]
#
#       min=100000
#       min_linkId=0
#       min_link=link_data[0]
#       for link_id,dist in out:
#
#         link=next((x for x in link_data if x.linkPVID == link_id), None)
#         links_plot.append(link)
#         heading_diff=calculate_heading_diff(input_point,link)
#         dscore=dist*100000
#         hscore=heading_diff/10
#         score=dscore+hscore
#
#         # print 'Score=',score
#         if score<min:
#             min=score
#             min_linkId=link_id
#             min_link=link
#         # plot_point_n_links(input_point, [link])
#       dfromref=distance_calc(min_link.reference_node,input_point)
#       match_obj = matched_point.Matched_point(input_point,min_linkId,'F',dfromref,dist)
#       matched_data.append(match_obj)
#
#       # for link_id, dist in out:
#       #     if link_id==min_linkId:
#       #         link = next((x for x in link_data if x.linkPVID == link_id), None)
#       #         dfromref=distance_calc(link.reference_node,input_point)
#       #         match_obj = matched_point.Matched_point(input_point,link_id,'F',dfromref,dist)
#       #         matched_data.append(match_obj)
#
#
      # plot_point_n_links(input_point,links_plot)
#
#   fileObject = open('matched_points', 'wb')
#   pickle.dump(matched_data, fileObject)
#
#   print 'Matched points length=',len(matched_data)
#   print 'Probe points length=', len(probe_data)

#distance calculation using Haversine formula
def distance_meters(lat1, lon1, lat2, lon2):
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * 3.14 / 180 - lat1 * 3.14 / 180
    dLon = lon2 * 3.14 / 180 - lon1 * 3.14 / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) +math.cos(lat1 * 3.14 / 180) * math.cos(lat2 * 3.14 / 180) *math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    d = R * c;
    return d * 1000# meters


def main():
  read_probe()
  read_link()

#Readdata directly from dump
  # fileObject = open('probe_data', 'rb')
  # probe_data = pickle.load(fileObject)
  #
  # fileObject = open('link_data', 'rb')
  # link_data = pickle.load(fileObject)

  print 'The number of links is ' ,len(link_data)
  probe_data_length=len(probe_data)
  min_link=link_data[0]
  for probe_index in range(probe_data_length):
      print probe_index,'/',probe_data_length
      input_point=probe_data[probe_index]
      # print input_point.latitude, input_point.longitude

      out = search_link(probe_index)

      print len(out)

      links_plot=[]

      min=100000
      min_linkId=0

      for link_id,dist in out:
        link=next((x for x in link_data if x.linkPVID == link_id), None)
        links_plot.append(link)
        heading_diff=calculate_heading_diff(input_point,link)
        dscore=dist*100000
        hscore=heading_diff/10
        score=dscore+hscore

        # print 'Score=',score
        if score<min:
            min=score
            min_linkId=link_id
            min_link=link
        # plot_point_n_links(input_point, [link])
      dfromref=distance_calc(min_link.reference_node,input_point)
      match_obj = matched_point.Matched_point(input_point,min_linkId,'F',dfromref,dist)
      matched_data.append(match_obj)

      # for link_id, dist in out:
      #     if link_id==min_linkId:
      #         link = next((x for x in link_data if x.linkPVID == link_id), None)
      #         dfromref=distance_calc(link.reference_node,input_point)
      #         match_obj = matched_point.Matched_point(input_point,link_id,'F',dfromref,dist)
      #         matched_data.append(match_obj)


  plot_point_n_links_highlight(input_point,links_plot,min_link)

  sys.exit()
  fileObject = open('matched_points', 'wb')
  pickle.dump(matched_data, fileObject)

  print 'Matched points length=',len(matched_data)
  print 'Probe points length=', len(probe_data)

  # data = write_data.read_dump()
  # write_data.write_csv(data)


def calculate_slopes():
    read_link()
    fileObject = open('matched_points', 'rb')
    matched_array=pickle.load(fileObject)
    for link in link_data:
        slope=slope_cal(link,matched_array)
        link.calculated_slope=slope

def write_slope_csv():
    with open('Partition6467Slope_ComparisonPoints.csv','wb') as out:
        writer = csv.writer(out, delimiter=',',quotechar='|')
        # sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink
        for link in link_data:
            row = link.linkPVID,link.slopeInfo,link.calculated_slope
            writer.writerow(row)
    print "File written !"

if __name__=="__main__":
  main()
  calculate_slopes()
  write_slope_csv()
