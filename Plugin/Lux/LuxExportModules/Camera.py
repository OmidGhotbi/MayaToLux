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