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
