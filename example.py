#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016, Blue Brain Project
#                     Cyrille Favreau <cyrille.favreau@epfl.ch>
#
# This file is part of pyBrayns
# <https://github.com/BlueBrain/PyBrayns>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

import pybrayns

# Initialize pybrayns with brayns url
brayns = pybrayns.PyBrayns('http://localhost:5000')

# Activate no shading shader
brayns.set_shader(brayns.SHADER_DIFFUSE)

# set ambient occlusion strength
brayns.set_ambient_occlusion(0.1)

# Activate soft-shadows
brayns.set_shadows(True)
brayns.set_soft_shadows(True)

# Define and set camera defined by origin, look-at, up vector, aperture and focal length
fov_camera = pybrayns.FovCamera(
    [0, 0, -3], [0, 0, 0], [0, 1, 0], 0, 0)
brayns.set_fov_camera(fov_camera)

# White material
material = pybrayns.Material(
    0, [1, 1, 1], [1, 1, 1], 100, 1, 0, 0, 0)
brayns.set_material(material)

# Set background color
brayns.set_background_color([0.1, 0.1, 0.1])

# set source image size
brayns.set_window_size(512, 512)

# Set number of samples per pixel
brayns.set_samples_per_pixel(64)

# Get JPEG image back and save it to example.jpg
brayns.set_image_jpeg_size(512, 512)
brayns.set_image_jpeg_quality(100)
image = brayns.get_image_jpeg()
if image != None:
    image.save('images/example.jpg')
