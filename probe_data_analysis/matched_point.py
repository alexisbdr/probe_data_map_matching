import link_dist
import probe

class Matched_point():
    sampleID=0
    dateTime=""
    sourceCode=0
    latitude=0.0
    longitude=0.0
    altitude=0
    speed=0
    heading=0
    linkPVID=0
    direction=''
    distFromRef=0
    distFromLink=0

    def __init__(self,probe,lID,dirxn,dfromref,dfromlink):
        self.sampleID=probe.sampleID
        self.dateTime=probe.dateTime
        self.sourceCode=probe.sourceCode
        self.latitude=probe.latitude
        self.longitude=probe.longitude
        self.altitude=probe.altitude
        self.speed=probe.speed
        self.heading=probe.heading
        self.linkPVID=lID
        self.direction=dirxn
        self.distFromRef=dfromref
        self.distFromLink=dfromlink


