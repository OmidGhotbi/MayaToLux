#******************************************************************************
#* Copyright (c) 2015-2022 Luxrender.                                         *
#* All rights reserved.                                                       *
#*                                                                            *
#* DESCRIPTION: Contains the Dll Entry stuff                                  *
#* AUTHOR: Omid Ghotbi (TAO) omid.ghotbi@gmail.com                            *
#* Based on a translation by Doug Hammond that is base on the c++ luxmaya     *
#* exporter, in turn based on maya-pbrt by Mark Colbert (luxCoreRenderer 1.x) *
#*                                                                            *
#*   This file is part of LuxRender.                                          *
#*                                                                            *
#* Licensed under the Apache License, Version 2.0 (the "License");            *
#* you may not use this file except in compliance with the License.           *
#* You may obtain a copy of the License at                                    *
#*                                                                            *
#*     http://www.apache.org/licenses/LICENSE-2.0                             *
#*                                                                            *
#* Unless required by applicable law or agreed to in writing, software        *
#* distributed under the License is distributed on an "AS IS" BASIS,          *
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   *
#* See the License for the specific language governing permissions and        *
#* limitations under the License.                                             *
#******************************************************************************

import math
from maya import OpenMaya
from maya import cmds

from ExportModule import ExportModule

class Camera(ExportModule):
    """
    Camera ExportModule. Responsible for detecting the type of the given
    camera and exporting a suitable lux camera with appropriate parameters.
    """
    
    DOF_CONST = 0 # this should be (1000 * (scene scale factor)), I think. :S
    
        def __init__(self, dagPath, width, height):
        """
        Constructor. Initialises local dagPath, camera function set and some
        vars needed for camera parameter calculation.
        """
        
        self.dagPath = dagPath
        self.camera = OpenMaya.MFnCamera(self.dagPath)
        
        self.outWidth  = width
        self.outHeight = height
        
        self.scale = 1.0
        
        self.sceneScale = self.getSceneScaleFactor()
        self.DOF_CONST = 1000 # * self.sceneScale
    #end def __init__
    
    def getOutput(self):
        """
        The actual camera export process starts here. First we insert the lux
        LookAt and then the appropriate camera.
        """

        if self.camera.isOrtho():
            self.InsertOrtho()
        else:
            ptype = cmds.getAttr( 'lux_settings.camera_persptype', asString = True )
            self.addToOutput ( '#Camera' )
            if ptype == 'Perspective':
                self.InsertPerspective()
            elif ptype == 'Environment':
                self.InsertEnvironment()
            else:
                self.InsertRealistic()
                
        self.InsertLookat()
    
    #end def getOutput
    
    def InsertCommon(self):
        """
        Insert parameters common to all camera types into the lux scene file.
        """
        
        # should really use focusDistance but that's not auto set to the camera's aim point ??!
        #self.addToOutput ( '\t"float focaldistance" [%f]' % (self.camera.centerOfInterest()*self.sceneScale) )
        
        
        if cmds.getAttr( 'lux_settings.camera_infinite_focus' ) == 0:
            focal_length = self.camera.focalLength() / self.DOF_CONST
            lens_radius = focal_length / ( 2 * self.camera.fStop() )
        else:
            lens_radius = 0.0 
        
        #self.addToOutput ( '\t"float lensradius" [%f]' % lens_radius )
    
        shiftX = self.camera.filmTranslateH() # these are a fraction of the image height/width
        shiftY = self.camera.filmTranslateV()
        
        # Film aspect ratio is > 1 for landscape formats, ie 16/9 > 1
        ratio = float(self.outWidth) / float(self.outHeight)
        invRatio = 1/ratio
        
        if ratio > 1.0:
            screenwindow = [ ( (2 * shiftX) - 1 ) * self.scale,
                             ( (2 * shiftX) + 1 ) * self.scale,
                             ( (2 * shiftY) - invRatio ) * self.scale,
                             ( (2 * shiftY) + invRatio ) * self.scale
                           ]
        else:
            screenwindow = [ ( (2 * shiftX) - ratio ) * self.scale,
                             ( (2 * shiftX) + ratio ) * self.scale,
                             ( (2 * shiftY) - 1 ) * self.scale,
                             ( (2 * shiftY) + 1 ) * self.scale
                           ]
        
        self.addToOutput( '\tscene.camera.screenwindow = %f %f %f %f' % (screenwindow[0], screenwindow[1], screenwindow[2], screenwindow[3]) )
        #self.addToOutput( '\t"float frameaspectratio" [%f]' % ratio )
        
        #self.addToOutput( '\t"float hither" [%f]' % (self.camera.nearClippingPlane()*self.sceneScale) )
        #self.addToOutput( '\t"float yon" [%f]' % (self.camera.farClippingPlane()*self.sceneScale) )
        self.addToOutput( '\tscene.camera.shutteropen = %f' % 0.0 )
        
        exposure_time = cmds.getAttr( 'lux_settings.camera_exposuretime' )
        self.addToOutput( '\tscene.camera.shutterclose = %f' % exposure_time )
    
    #end def InsertCommon
    
    def InsertLookat(self):
        """
        Here we grab the camera's position, point and up vectors and output them
        as a lux LookAt.
        """
        
        try:
            eye = self.camera.eyePoint(OpenMaya.MSpace.kWorld)
        except:
            OpenMaya.MGlobal.displayError( "Failed to get camera.eyePoint\n" )
            raise
        
        try:
            up = self.camera.upDirection(OpenMaya.MSpace.kWorld)
        except:
            OpenMaya.MGlobal.displayError( "Failed to get camera.upDirection\n" )
            raise