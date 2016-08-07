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

from pyBrayns.pybrayns import *

# --------------------------------------------------
# Initialize PyBrayns with brayns url
# --------------------------------------------------
brayns = PyBrayns('http://localhost:5000')

# --------------------------------------------------
# Activate default renderer
# --------------------------------------------------
brayns.set_renderer(RENDERER_DEFAULT)

# --------------------------------------------------
# Activate no shading shader
# --------------------------------------------------
brayns.set_shader(SHADER_DIFFUSE)

# --------------------------------------------------
# set ambient occlusion strength
# --------------------------------------------------
brayns.set_ambient_occlusion(0)

# --------------------------------------------------
# Activate shadows and make them soft
# --------------------------------------------------
brayns.set_shadows(True)
brayns.set_soft_shadows(True)

# --------------------------------------------------
# Define and set camera defined by origin, look-at,
# up vector, aperture and focal length
# --------------------------------------------------
fov_camera = Camera()
fov_camera.set_origin(0,0,-3)
fov_camera.set_look_at(0,0,0)
brayns.set_fov_camera(fov_camera)

# --------------------------------------------------
# Set material 0 to white
# --------------------------------------------------
material = Material()
material.set_diffuse_color(1,1,1)
material.set_specular_color(1,1,1)
material.set_specular_exponent(100)
material.set_opacity(1)
brayns.set_material(0, material)

# --------------------------------------------------
# Set background color
# --------------------------------------------------
brayns.set_background_color(0.1, 0.1, 0.1)

# --------------------------------------------------
# set source image size
# --------------------------------------------------
brayns.set_window_size(512, 512)

# --------------------------------------------------
# Set number of samples per pixel
# --------------------------------------------------
brayns.set_samples_per_pixel(1)

# --------------------------------------------------
# Define transfer function for electrical simulation
# --------------------------------------------------
transfer_function = TransferFunction()

# Define control points for all attributes (R,G,B,A)
red_control_points = [
    [ -92.0915, 0.1 ], [-61.0, 0.1 ],
    [-50.0, 0.8 ], [0.0, 0.0], [49.5497, 1]]
transfer_function.set_control_points(
    ATTRIBUTE_RED, red_control_points)

green_control_points = [
    [ -92.0915, 0.1 ], [-55.0, 0.1 ],
    [-50.0, 0.5 ], [49.5497, 1]]
transfer_function.set_control_points(
    ATTRIBUTE_GREEN, green_control_points)

blue_control_points = [
    [ -92.0915, 0.1 ], [-50.0, 0.1 ],
    [-58.0, 0.0 ], [0.0, 0.1]]
transfer_function.set_control_points(
    ATTRIBUTE_BLUE, blue_control_points)

alpha_control_points = [
    [ -92.0915, 1.0 ], [49.5497, 1]]
transfer_function.set_control_points(
    ATTRIBUTE_ALPHA, alpha_control_points)

# Set transfer function
brayns.set_transfer_function(transfer_function)

# --------------------------------------------------
# Get JPEG image back and save it to example.jpg
# --------------------------------------------------
brayns.set_image_jpeg_size(512, 512)
brayns.set_image_jpeg_quality(100)
image = brayns.get_image_jpeg()
if image is not None:
    image.save('example.jpg')

# --------------------------------------------------
# Get frame buffers (Color and Depth)
# --------------------------------------------------
image = brayns.get_frame_buffer(FRAMEBUFFER_COLOR)
if image is not None:
    image.save('fb_color.tif')
image = brayns.get_frame_buffer(FRAMEBUFFER_DEPTH)
if image is not None:
    image.save('fb_depth.tif')
