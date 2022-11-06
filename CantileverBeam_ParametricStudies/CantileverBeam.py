# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

execfile("Parameters_for_CantileverBeam.py")

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 

Mdb()

# Create Part 
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=400.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(0.0, 0.0), 
    point2=(L, T))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=W, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((209000.0, 0.3), 
    ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)

# Assembly
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])

# Step
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

# Boundary Conditions
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.0, T/2.0, W/2.0), )), name='Set-1')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=SET, u2=SET, 
    u3=SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    L/2.0, T, W/2.0), )))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, field='', magnitude=q, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])

# Mesh
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=2.0)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT),), regions=(
    mdb.models['Model-1'].parts['Part-1'].cells, ))

# Create a Point Set for Postprocessing
mdb.models['Model-1'].rootAssembly.Set(name='Set-Point', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((L, T, W), )))

mdb.models['Model-1'].rootAssembly.regenerate()

# Job
jobName ='CantileverBeam'

###############################################
###  Create new directionary for FE files
###############################################
DirName = jobName + '_q_' + "%g"%q
curr_dir = os.getcwd()
if not os.path.exists(curr_dir + '\\FEModelFiles'):
    os.mkdir(curr_dir + '\\FEModelFiles')
if not os.path.exists(curr_dir + '\\FEModelFiles\\' + DirName):
    os.mkdir(curr_dir + '\\FEModelFiles\\' + DirName)
os.chdir(curr_dir + '\\FEModelFiles\\' + DirName)

#
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()


##############################################################
## Report Displacement and Reaction Force
## https://anning003.com/extract-reaction-force/
##############################################################


stepName = 'Step-1'
outputSetName = 'Set-Point'

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

odb = openOdb(path = jobName+'.odb')

timeFrame = odb.steps[stepName].frames[1]
Disp = timeFrame.fieldOutputs['U']
readNode = odb.rootAssembly.nodeSets[outputSetName.upper()]
readNodeDisp = Disp.getSubset(region=readNode)
readNodeDispValues = readNodeDisp.values

Displacement = readNodeDispValues[0].data[1] # 0-X Direction; 1-Y Direction; 2-Z Direction

outfile = open(jobName + '.csv', 'w')
outfile.write('Pressure [MPa]' + ',' + 'Displacement [mm]' + '\n')
outfile.write("%g"%q + ',' + "%g"%Displacement)
outfile.close()