               
### The "CoreBuilder" script
### Authors: Kevin Manalo, Richard Cerge, Dylon Wegner
### Version: alpha 1, call it beta after full overlay support
### Origination Date: Sept 10, 2010

from __future__ import print_function
import os
import sys
from operator import mul

### AUXILARY FUNCTIONS ###

#here we attempt to classify the type of overlay
def overlayID(olList):
  noo = int(abs(int(olList[0][0])))
  #determine if we have a repeated lattice
  latflag = []
  if int(olList[0][0]) < 0:
    for x in range(noo):
      latflag.append('yes')
  else:
    for x in range(noo):
      if int(olList[1][x]) < 0:
        latflag.append('yes')
      else:
        latflag.append('no')

# We will define overlay shape ID and names for this source code
#   Shape                        ShapeID             penshxp spec.          source code name
#-------------------------------------------------------------------------------------------
# rectangle                         1              -x,+x,-y,+y,(-z,+z)               rect
# cylinder(along z)                 2              -x,+x,-y,+y,(-z,+z)               cylz
# quarter cylinder             21,22,23,24         -x,+x,-y,+y,(-z,+z)               qcyl
# cylinder(along y)                 25             -x,+x,-z,+z                       cyly
# cylinder(along x)                 26             -y,+y,-z,+z                       cylx
# arbitrary triangle                3              Ax,Ay,Bx,By,Cx,Cy,(-z,+z)         arbtri
# prismatic right triangle     31,32,33,34         -x,+x,-y,+y,(-z,+z)               pritri
# sphere                            4              Ox,Oy,Oz,r,(-z,+z)                sphr
# sector                            51             Ox,Oy,Ax,Ay,Bx,By,(-z,+z)         sect

  olID = []
  for x in range(noo):
    if abs(int(olList[1][x])) == 1:
      olID.append('rect')
    elif abs(int(olList[1][x])) == 2:
      olID.append('cylz')
    elif abs(int(olList[1][x])) == 21:
      olID.append('qcyl')
    elif abs(int(olList[1][x])) == 22:
      olID.append('qcyl')
    elif abs(int(olList[1][x])) == 23:
      olID.append('qcyl')
    elif abs(int(olList[1][x])) == 24:
      olID.append('qcyl')
    elif abs(int(olList[1][x])) == 25:
      olID.append('cyly')
    elif abs(int(olList[1][x])) == 26:
      olID.append('cylx')
    elif abs(int(olList[1][x])) == 3:
      olID.append('arbtri')
    elif abs(int(olList[1][x])) == 31:
      olID.append('pritri')
    elif abs(int(olList[1][x])) == 32:
      olID.append('pritri')
    elif abs(int(olList[1][x])) == 33:
      olID.append('pritri')
    elif abs(int(olList[1][x])) == 34:
      olID.append('pritri')
    elif abs(int(olList[1][x])) == 4:
      olID.append('sphr')
    elif abs(int(olList[1][x])) == 51:
      olID.append('sect')
    else:
      olID.append('unidentified shape ID')

  return latflag,olID
  
  

  

# flatten a 2-d list to a 1-d list
def flatten(iterable):
  for elem in iterable:
    if hasattr(elem, '__iter__'):
      for sub in flatten(elem): yield sub
    else:
      yield elem

def dot_product(a, b):
  return sum(map(mul, a, b))

def dot_dot_product(a, b, c):
  tmp=map(mul, a, b)
  return sum(map(mul, tmp, c))

# function to strip commas and 'slashes'
# slash '/' in 1st column is comment in PENMSHXP
# function filters the comments out!!!
def parseSlash(file):
  lst=[]
  for line in file:

    if "cm overlay" in line:
      lst.append("overlay begin")
    elif "/" in line[0]:
      pass
    else:
      line=line.replace(","," ")
      line=line.split()      
      lst.append(line)

  return lst

# pList inputs are files - penmsh.inp data
def processPData(pList):

  # curly bracket is dictionary
  pData={}

  # for a file in the pList
  for f in pList:

    # typeName is a substring of f
    if '/' in f:
      typeName = f[0:f.find('/')]
    else:
      typeName = f

    with open(f,'r') as file:
      data=parseSlash(file)

    # key-value pair is formed
    # the value is a rather large blob of data
    pData[typeName]=data
      
  return pData

# zList inputs are files - prbname#.inp data where # is a z-level
def processZData(zList,maxZLevel):

  zData={}
  
  for f in zList:
    # now, we handle the z-level component
    for iLevel in range(1,int(maxZLevel)+1):
      if '/' in f:
        typeName = f[0:f.find('/')]
      else:
        typeName = f

      with open(f,'r') as file:
        data=parseSlash(file)

      data.append("overlay begin")  ##KEVEN..WHY IS THIS HERE AND WHAT DOES IT DO.....

      zData[typeName,iLevel]=data

  return zData

### CREATE A SIMPLE CLASS ###

class zDataProcessor:
  ''' calculates data scoped within zData '''

  def __init__(self, zData):
      self.zData = zData

  ### METHOD NCX ###
  def ncx(self,key):
    ncx, ncy, maxfinz = self.zData[key][0]
    ncx = int(ncx)
    return ncx

  ### METHOD NCY ###
  def ncy(self,key):
    ncx, ncy, maxfinz = self.zData[key][0]
    ncy = int(ncy)
    return ncy

  ### METHOD THREADCM ###
  def thread(self,key,cmNumber):
    ncx, ncy, maxfinz = self.zData[key][0]

    nc = int(ncx)*int(ncy)
    ncx = int(ncx)
    ncy = int(ncy)

    cmn = int(cmNumber)

    # grab #xfm & #yfm & #zfm
    
    pickRow = (cmn-1)//ncy + 1
    pickCol = cmn % ncy or ncy    

    ### XFM : Number of X-fine Meshes ###
    
    numXFM = None
    for jy in range(1,ncy+1):
      row = self.zData[key][jy]
      vals = [ int(val) for val in row ]
      for ix in range(1,ncx+1):
        val = vals[ix-1]
        if (ix == pickCol and jy == pickRow):
          numXFM = val

    if (numXFM is None):
      print( "no value found for numXFM!" )
      sys.exit(1)
      
    lastRow = jy

    ### YFM : Number of Y-fine Meshes ###
    
    numYFM = None
    for jy in range(lastRow+1,lastRow+ncy+1):
      row = self.zData[key][jy]
      vals = [ int(val) for val in row ]
      for ix in range(1,ncx+1):
        val = vals[ix-1]
        if (ix == pickCol and (jy-lastRow) == pickRow):
          numYFM = val   
    
    if (numYFM is None):
      print( "no value found for numYFM!" )
      sys.exit(1)
      
    lastRow = jy

    ### ZFM : Number of Z-fine Meshes ###
    
    numZFM = None
    for jy in range(lastRow+1,lastRow+ncy+1):
      row = self.zData[key][jy]
      vals = [ int(val) for val in row ]
      for ix in range(1,ncx+1):
        val = vals[ix-1]
        if (ix == pickCol and (jy-lastRow) == pickRow):
          numZFM = val   

    if (numZFM is None):
      print( "no value found for numZFM!" )
      sys.exit(1)

    lastRow = jy

    
    ### Determine delta-X ###

    dx = None
    lineNumber = lastRow + 1
    row = self.zData[key][lineNumber]
    vals = [ float(val) for val in row ]
    for ix in range(1,ncx+1):
      if(ix == pickCol):
        dx = vals[ix] - vals[ix-1]
      
        
    if (dx is None):
      print( "no value found for dx!" )
      sys.exit(1)
    
    ### Determine delta-Y ###

    dy = None
    lineNumber += 1
    row = self.zData[key][lineNumber]
    vals = [ float(val) for val in row ]
    for jy in range(1,ncy+1):
      if(jy == pickRow):
        dy = vals[jy] - vals[jy-1]

    if (dy is None):
      print( "no value found for dx!" )
      sys.exit(1)


    ### CM-Type ###

    lastRow = lineNumber
    cmType = None
    ctr = 0
    for jy in range(lastRow+1,lastRow+ncy+1):
      row = self.zData[key][jy]
      vals = [ int(val) for val in row ]
      for ix in range(1,ncx+1):
        val = vals[ix-1]
        # if negative count associated overlay
        if (val < 0):
          ctr += 1
        if (ix == pickCol and (jy-lastRow) == pickRow):
          cmType = val
          overlayNum = ctr

    overlayTot = ctr
    
    if (cmType is None):
      print( "no value found for cmType!" )
      sys.exit(1)

    ### matPerCM ###

    lastRow = jy
    matPerCM = None
    for jy in range(lastRow+1,lastRow+ncy+1):
      row = self.zData[key][jy]
      vals = [ int(val) for val in row ]
      for ix in range(1,ncx+1):
        val = vals[ix-1]
        if (ix == pickCol and (jy-lastRow) == pickRow):
          matPerCM = val  

    if (matPerCM is None):
      print( "no value found for matPerCM!" )
      sys.exit(1)

    ### Base Material ###

    lastRow = jy
    baseMatl = None
    
    for idx in range(lastRow+1,lastRow+ncx*ncy+1):
      val = int(self.zData[key][idx][0])
      if( (idx-lastRow) == cmNumber ):
        baseMatl = val
      
    xCMidx = pickCol
    yCMidx = pickRow

    ### CM Overlay ###

    lastRow = idx

    #DBG print(self.zData[key][lastRow+1])
    ctr = 1
    
    lineNumber = lastRow + 1

    line = ""

    overlayList = []
    for ctr in range(1,overlayTot+1):
      
      while "overlay begin" not in line:
        lineNumber = lineNumber + 1
        line = self.zData[key][lineNumber]
        
        if( ctr == overlayNum and "overlay begin" not in line ):         
          overlayList.append( self.zData[key][lineNumber] )
      line = ""
    
    #DBG print(overlayList)
    
    #DBG print(numXFM,numYFM,numZFM,xCMidx,yCMidx,dx,dy,cmType,matPerCM,baseMatl)      
    return numXFM,numYFM,numZFM,xCMidx,yCMidx,dx,dy,cmType,matPerCM,baseMatl,overlayList 
  def calcFMinKey(self,key):

    #ncx, ncy, maxfinz = zDataKey[0]

    
    ncx, ncy, maxfinz = self.zData[key][0]
    ncx = int(ncx)
    ncy = int(ncy)
    ncz = abs(int(maxfinz))



    xfm=[]
    for i in range(1,1+ncx):
      #intList=[int(val) for val in zDataKey[i]]
      intList=[int(val) for val in self.zData[key][i]]
      xfm.append(intList)

    yfm=[]
    for i in range(1+ncx,1+2*ncx):
      #intList=[int(val) for val in zDataKey[i]]
      intList=[int(val) for val in self.zData[key][i]]
      yfm.append(intList)

    if(int(maxfinz)<0):
      zfm=[]
      for i in range(1+2*ncx,1+3*ncx):
        #intList=[int(val) for val in zDataKey[i]]
        intList=[int(val) for val in self.zData[key][i]]
        zfm.append(intList)

    #xfm=[int(item) for item in xfm]
    xfm=list(flatten(xfm))
    yfm=list(flatten(yfm))
    zfm=list(flatten(zfm))
      
    print(xfm,"\n")
    print(yfm,"\n")
    print(zfm,"\n")


### END OF CLASS DEFINITION ###
    
def processEachType(typeData,maxZLevel):  #type data is name of folder, foldername/penmsh.inp, and nickname
  if len(typeData[0])==3:                 #maxZLevel is an integer
    nList = {}
    #print("Processing folder(s): ", [item[0] for item in typeData])
    nList=[item[0] for item in typeData]
    pList=[item[0]+"/penmsh.inp" for item in typeData]
    pData=processPData(pList)

    for i in range(1,int(maxZLevel)+1):
      zList=[item[0]+"/"+item[0]+str(i)+".inp" for item in typeData]  
      zData=processZData(zList,i)
      
    return pData, zData, nList

### MAIN PROGRAM BEGIN
  
if os.path.isfile("corebuild.inp"):
  print("Processing corebuild.inp file")
else:
  print("No corebuild.inp file exists, exiting")
  sys.exit(1)
  
data=[]
with open("corebuild.inp",'r') as file:
  data=parseSlash(file)

  #input("Press <ENTER> to continue")
            
# collect typeData, break off from data
typeData=[]
for item in data:
  if len(item) == 2:
    typeData.append(item)
  else:
    del data[0:len(typeData)]
    break

# if './' in typename, convert to text
typeData=[ [item[0].replace('./',''),item[0].replace('./','')+'/penmsh.inp',item[1]] \
           for item in typeData]

# typeData now has length 3 if problem is inside a folder

# break off final output name
masterName=data.pop().pop()   #final foldername

# convert data to mapData, this is the new global core map
mapData=data
del data

# form typeDict (dictionary)

typeDict = {}      # key is nickname....value is foldername
if len(typeData[0])==3:
  for item in typeData:
    typeDict[item[2]] = item[0] 
if len(typeData[0])==2:
  for item in typeData:
    typeDict[item[1]] = item[0]

keys=typeDict.keys()   #shows the nicknames

keys=list(keys)    #puts the nicknames in a list  

# break max z-level off from mapData
maxZLevel=mapData.pop(0).pop()

#print('mapData', mapData)
nList= {} # Holds the type names for ascertaining data from pData
zList= [] # Holds the values for Z-Levels in each type
pData, zData, nList = processEachType(typeData,maxZLevel)

# Number of Z levels as well as type location for pData
for x in nList:
 # print('in', pData[x][0][0])
 # print(pData[x][1][0], ' z-levels')
  zList.append(int(pData[x][1][0]))


# This is the definition of z based off the class 'zDataProcessor'

z=zDataProcessor(zData)  #instantiate an object to the class 


# For each map z-level

mapZlevel = mapData.pop(0)
mapZlevel = int(mapZlevel[0])

# obtain mapXspan and mapYspan lists
mapXspan = mapData[0]


### SECTION for mapXspan and mapYspan needed to calculate global bdy data !!!

# mapXspan and mapYspan are just the first row & column resp.
#print('mapXspan', mapXspan)

mapYspan = []
for item in mapData:
  if len(item) == 1:
    break
  else:
    mapYspan.append(item[0])



# calculate globalXspan and associated globalXlist - the x boundary list

globalXlist = [0.]
globalCtr = 0
planeNCX = 0
gridNCXlist = []
gridDXlist = []
for key in mapXspan:

  # calculate ncx; ncy

  ncx=z.ncx((typeDict[key],1))
  ncy=z.ncy((typeDict[key],1))
  xyGrid = ncx*ncy

  dxSpan = 0.
  dySpan = 0.
  
  for i in range(1,xyGrid+1):

    ### collect a heavy amt of data with the thread method 'threading CM' information from the zData
    numXFM,numYFM,numZFM,xCMidx,yCMidx,dx,dy,cmType,matPerCM,baseMatl,overlayList = z.thread((typeDict[key],1),i)
    if yCMidx == 1:
      dxSpan += dx
      globalCtr += 1
      globalXlist.append(globalXlist[globalCtr-1]+dx)
    if xCMidx == 1:
      dySpan += dy

  if(len(gridNCXlist)>=1):
    gridNCXlist.append(ncx+int(gridNCXlist[-1]))
    gridDXlist.append(dxSpan+float(gridDXlist[-1]))
  else:
    gridNCXlist.append(ncx)
    gridDXlist.append(dxSpan)
    
  planeNCX += ncx
#print(globalXlist)  # this is all of the changes in x for each cm along the entire global x-axis grid
gridNCXlist.insert(0,0)
gridNCXlist.pop()
gridDXlist.insert(0,0)
gridDXlist.pop()
#print(gridNCXlist) # this list contains the list "element" number in globalXlist that correspond to x distance that starts a new tile
#print(gridDXlist)  # this list contains the starting x position for each new tile
#input('press <ENTER> to continue')

# calculate globalYspan and associated globalYlist - the y boundary list

globalYlist = [0.]
globalCtr = 0
planeNCY = 0
gridNCYlist = []
gridDYlist = []

for key in mapYspan:

  # calculate ncx; ncy
  ncx=z.ncx((typeDict[key],1))####################
  ncy=z.ncy((typeDict[key],1))####################
  xyGrid = ncx*ncy

  dxSpan = 0.
  dySpan = 0.

  for i in range(1,xyGrid+1):
    numXFM,numYFM,numZFM,xCMidx,yCMidx,dx,dy,cmType,matPerCM,baseMatl,overlayList = z.thread((typeDict[key],1),i)################################
    if yCMidx == 1:
      dxSpan += dx
    if xCMidx == 1:
      dySpan += dy
      globalCtr += 1
      globalYlist.append(globalXlist[globalCtr-1]+dy)
  
  if(len(gridNCYlist)>=1):
    gridNCYlist.append(ncy+int(gridNCYlist[-1]))
    gridDYlist.append(dySpan+float(gridDYlist[-1]))
  else:
    gridNCYlist.append(ncy)
    gridDYlist.append(dySpan)
    
  planeNCY += ncy

gridNCYlist.insert(0,0)
gridNCYlist.pop()
gridDYlist.insert(0,0)
gridDYlist.pop()

### These arrays are the respective x and y shifts for new map positions
### The first elements of the arrays should be zero !!!

addNCX=gridNCXlist # better names
addNCY=gridNCYlist
addDX=gridDXlist # better names
addDY=gridDYlist

# The above lists are important for boundary and coarse mesh dimension information

### SECTION - BUILD THE FINAL FILE 'prbname.inp'
# Recall the old PENMSHXP had prbname#.inp, now we turn a new format 'all-in-one'

f = masterName
if '/' in f:
  f=f.replace('./','')
#print(f)
f = f + '/prbname.inp'

with open(f,'w') as penmshinp:

  ### DEFINE DIMENSIONS
  print("/All-zlev-in-one input file : prbname.inp", file=penmshinp)
  print("/ncx, ncy", file=penmshinp)

  print(planeNCX, planeNCY, sep=',', file=penmshinp)

  print("/ cm bounds along x-axis (in seq ...x)", file=penmshinp)

  ### DEFINE X BOUNDARIES 
  for val in globalXlist:
    print(val, end=' ', file=penmshinp)
  print(end='\n', file=penmshinp)
  
  print("/ cm bounds along y-axis (in seq ...x)", file=penmshinp)

  ### DEFINE Y BOUNDARIES
  for val in globalYlist:
    print(val, end=' ', file=penmshinp)
  print(end='\n', file=penmshinp)

  print("/CM cards", file=penmshinp)

  ### THE MASTER ALGORITHM (ASSUMING CYLINDRICAL LATTICES)
  #print(mapData)
  #input()
  zlevel = int(0)
  for zlevel in range(1,zList[0]+1):
    icy = -1
    overlayChanged = False
    for x in range(len(mapData)):

      icy+=1
      if( len(mapData[x]) <= 1 ):
        break
      levelXspan = mapData[x]
      icx = -1
      for key in levelXspan:
        icx+=1
        ncx=z.ncx((typeDict[key],zlevel))################
        ncy=z.ncy((typeDict[key],zlevel))################
        xyGrid = ncx * ncy
        for i in range(1,xyGrid+1):
          overlayList=[]
          numXFM,numYFM,numZFM,xCMidx,yCMidx,dx,dy,cmType,matPerCM,baseMatl,overlayList = z.thread((typeDict[key], zlevel),i)##############

          # This is new........................
          latflag,olID = overlayID(overlayList)

          
          print('cm=', xCMidx+addNCX[icx], yCMidx+addNCY[icy], zlevel, file=penmshinp) ##########################
          print(-1*baseMatl, '          / mat num', file=penmshinp)
          print(numXFM,numYFM,numZFM, '  / fine mesh numbers (#xfm, #yfm, #zfm)', sep=' ', file=penmshinp)
          print("/overlay", file=penmshinp)

          # Here we have our dx,dy,dz adjustments 
       
      
          ctr = 0
          olctr = 0
          latflagISon = False
          for item in overlayList:          
            ctr+=1
            colctr = 0
            if olctr >= len(olID):                  # This is a fix to a logic issue.....maybe a better way? Dylon..look at me
              olctr = 0
            oltype = olID[olctr]
            for subitem in item:
              if ctr <= 3:
                print(subitem, end=" ", file=penmshinp)
                overlayChanged = False
              else:
                colctr +=1
                if latflagISon:
                  print(subitem, end=" ", file=penmshinp)
                  overlayChanged = False
                else:
                  if(oltype=='rect' or oltype=='cylz' or oltype=='qcyl' or oltype=='pritri'):                 #first set of overlays
                    if(colctr <= 2):
                      print("{:10.5f}".format(float(subitem)+float(addDX[icx])), end=" ", file=penmshinp)
                    elif(colctr > 2 and colctr <=4):
                      print("{:10.5f}".format(float(subitem)+float(addDY[icy])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr > 4):
                       #print stuf for z direction....
                      overlayChanged = True                 
                    
                  elif(oltype=='cyly'):                                                                        #second set of overlays
                    if(colctr <= 2):
                      print("{:10.5f}".format(float(subitem)+float(addDX[icx])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr > 2):
                      #print stuff in z direcion...
                      overlayChanged = True
                                         
                  elif(oltype=='cylx'):                                                                         #third set of overlays
                    if(colctr <= 2):
                      print("{:10.5f}".format(float(subitem)+float(addDY[icy])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr > 2):
                      #print stuff in z direcion...
                      overlayChanged = True

                  elif(oltype=='arbtri' or oltype=='sect'):                                                     #fourth set of overlays
                    if(colctr%2!=0 and colctr < 7):
                      print("{:10.5f}".format(float(subitem)+float(addDX[icx])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr%2==0 and colctr < 7):
                      print("{:10.5f}".format(float(subitem)+float(addDY[icy])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr > 6):
                      #print stuff for z direction
                      overlayChanged = True
                      
                  elif(oltype=='sphr'):                                                                         #and lastly...the lonely sphere...
                    if(colctr == 1):
                      print("{:10.5f}".format(float(subitem)+float(addDX[icx])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr == 2):
                      print("{:10.5f}".format(float(subitem)+float(addDY[icy])), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr == 3):
                      #print stuff in z
                      overlayChanged = True
                    elif(colctr == 4): #the radius shouldnt be adjusted
                      print("{:10.5f}".format(float(subitem)), end=" ", file=penmshinp)
                      overlayChanged = True
                    elif(colctr > 4):
                      #print stuff in z direction
                      overlayChanged = True
                      

                  
            if latflagISon:           
              latflagISon = False
              
            if overlayChanged:          
              print(end=" / This overlay row was changed \n", file=penmshinp)
              if(latflag[olctr] == 'yes' and overlayChanged):
                latflagISon = True
              olctr += 1
              overlayChanged = False
            else:
              print(end="\n", file=penmshinp)
                    
                
                    
                
























          
          
