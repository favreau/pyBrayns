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

import requests
import json
from PIL import Image
from io import BytesIO
import base64

ATTRIBUTE_RED = 'red'
ATTRIBUTE_GREEN = 'green'
ATTRIBUTE_BLUE = 'blue'
ATTRIBUTE_ALPHA = 'alpha'
ATTRIBUTE_LIGHT_EMISSION = 'emission'

SHADER_DIFFUSE = 'diffuse'
SHADER_ELECTRON = 'electron'
SHADER_NOSHADING = 'noshading'

FRAMEBUFFER_COLOR = 0
FRAMEBUFFER_DEPTH = 1

RENDERER_DEFAULT = 'exobj'
RENDERER_PROXIMITY_DETECTION = 'proximityrenderer'
RENDERER_SIMULATION = 'simulationrenderer'


class Camera(object):

    def __init__(self):
        self._origin = [0,0,-1]
        self._look_at = [0,0,0]
        self._up = [0,1,0]
        self._aperture = 0
        self._focal_length = 0

    def set_origin(self, x, y, z):
        self._origin = [x,y,z]

    def set_look_at(self, x, y, z):
        self._look_at = [x,y,z]

    def set_up(self, x, y, z):
        self._up = [x,y,z]

    def set_aperture(self, aperture):
        self._aperture = aperture

    def set_focal_length(self, focal_length):
        self._focal_length = focal_length

    def serialize(self):
        payload = {
            "origin": {
                "x": self._origin[0],
                "y": self._origin[1],
                "z": self._origin[2]
            },
            "lookAt": {
                "x": self._look_at[0],
                "y": self._look_at[1],
                "z": self._look_at[2]
            },
            "up": {
                "x": self._up[0],
                "y": self._up[1],
                "z": self._up[2]
            },
            "fovAperture": self._aperture,
            "fovFocalLength": self._focal_length
        }
        return json.dumps(payload)

    def deserialize(self, content):
        obj = json.loads(content)
        self._origin[0] = obj['origin']['x']
        self._origin[1] = obj['origin']['y']
        self._origin[2] = obj['origin']['z']
        self._look_at[0] = obj['lookAt']['x']
        self._look_at[1] = obj['lookAt']['y']
        self._look_at[2] = obj['lookAt']['z']
        self._up[0] = obj['up']['x']
        self._up[1] = obj['up']['y']
        self._up[2] = obj['up']['z']
        self._aperture = obj['fovAperture']
        self._focal_length = obj['fovFocalLength']

    def __str__(self):
        return 'Origin: ' + str(self._origin) + \
               ', Target: ' + str(self._look_at) + \
               ', Up: ' + str(self._up) + \
               ', Aperture: ' + str(self._aperture) + \
               ', Focal length: ' + str(self._focal_length)


class Material(object):

    def __init__(self):
        self._diffuse_color = None
        self._specular_color = None
        self._specular_exponent = None
        self._opacity = None
        self._refraction_index = None
        self._reflection_index = None
        self._light_emission = None

    def set_diffuse_color(self, r, g, b):
        self._diffuse_color = [r,g,b]

    def set_specular_color(self, r, g, b):
        self._specular_color = [r,g,b]

    def set_specular_exponent(self, exponent):
        self._specular_exponent = exponent

    def set_opacity(self, opacity):
        self._opacity = opacity

    def set_refraction_index(self, refraction_index):
        self._refraction_index = refraction_index

    def set_reflection_index(self, reflection_index):
        self._reflection_index = reflection_index

    def set_light_emission(self, light_emission):
        self._light_emission = light_emission

    def serialize(self, index):
        payload = {
            "index": index,
            "diffuseColor" :
            {
                "r" : self._diffuse_color[0],
                "g" : self._diffuse_color[1],
                "b" : self._diffuse_color[2]
            },
            "lightEmission" : self._light_emission,
            "opacity" : self._opacity,
            "reflectionIndex" : self._reflection_index,
            "refractionIndex" : self._refraction_index,
            "specularColor" :
            {
                "r" : self._specular_color[0],
                "g" : self._specular_color[1],
                "b" : self._specular_color[2]
            },
            "specularExponent" : self._specular_exponent
        }
        return json.dumps(payload)

    def deserialize(self, content):
        obj = json.loads(content)
        self._diffuse_color[0] = obj['diffuseColor']['r']
        self._diffuse_color[1] = obj['diffuseColor']['g']
        self._diffuse_color[2] = obj['diffuseColor']['b']
        self._specular_color[0] = obj['specularColor']['r']
        self._specular_color[1] = obj['specularColor']['g']
        self._specular_color[2] = obj['specularColor']['b']
        self._specular_exponent = obj['specularExponent']
        self._opacity = obj['opacity']
        self._refraction_index = obj['refractionIndex']
        self._reflection_index = obj['reflectionIndex']
        self._light_emission = obj['lightEmission']

    def __str__(self):
        return 'Diffuse color: ' + str(self._diffuse_color) + \
               ', Specular color: ' + str(self._specular_color) + \
               ', Specular exponent: ' + str(self._specular_exponent) + \
               ', Opacity: ' + str(self._opacity) + \
               ', Refraction index: ' + str(self._refraction_index) + \
               ', Reflection index: ' + str(self._reflection_index) + \
               ', Light emission: ' + str(self._light_emission)


class TransferFunction(object):

    def __init__(self):
        self._control_points = dict()
        self._control_points[ATTRIBUTE_RED] = []
        self._control_points[ATTRIBUTE_GREEN] = []
        self._control_points[ATTRIBUTE_BLUE] = []
        self._control_points[ATTRIBUTE_ALPHA] = []

    def get_attributes(self):
        attributes = []
        for attribute in self._control_points:
            attributes.append(attribute)
        return attributes

    def get_control_points(self, attribute):
        return self._control_points[attribute]

    def set_control_points(self, attribute, control_points):
        self._control_points[attribute].clear()
        for control_point in control_points:
            self._control_points[attribute].append( control_point )

    def serialize(self):
        for attribute in self.get_attributes():
            payload = '{"attribute": "' + attribute + '", "points": ['
            count = 0
            for point in self._control_points[attribute]:
                if count != 0:
                    payload = payload + ','
                payload = payload + '{"x":' + str(point[0]) + ',"y":' + str(point[1]) + '}'
                count += 1
            payload = payload + ']}'
        return payload


class PyBrayns(object):

    def __init__(self, url):
        """
        Setup brayns context
        """
        self._url = url
        self._url_attribute = self._url + '/zerobuf/render/attribute'
        self._url_fov_camera = self._url + '/zerobuf/render/fovcamera'
        self._url_color_map = self._url + '/zerobuf/render/colormap'
        self._url_image_jpeg = self._url + '/lexis/render/imagejpeg'
        self._url_material = self._url + '/zerobuf/render/material'
        self._url_transfer_function = self._url + '/zerobuf/render/transferFunction1D'
        self._url_frame_buffers = self._url + '/zerobuf/render/framebuffers'

    def set_fov_camera(self, fov_camera):
        self.__request(self._url_fov_camera, 'PUT', fov_camera.serialize())

    def get_fov_camera(self, fov_camera):
        r = requests.get(self._url_fov_camera)
        fov_camera.deserialize(str(r.text))

    def set_ambient_occlusion(self, strengh):
        self.__set_attribute('ambient-occlusion', strengh)

    def set_image_jpeg_quality(self, quality):
        self.__set_attribute('jpeg-compression', quality)

    def set_samples_per_pixel(self, spp):
        self.__set_attribute('spp', spp)

    def set_background_color(self, r, g, b):
        value = str(r) + ' ' + str(g) + ' ' + str(b)
        self.__set_attribute('background-color', value)

    def set_window_size(self, width, height):
        self.__set_attribute('window-size', str(width) + ' ' + str(height))

    def set_image_jpeg_size(self, width, height):
        self.__set_attribute('jpeg-size', str(width) + ' ' + str(height))

    def set_shadows(self, enabled):
        self.__set_attribute('shadows', int(enabled))

    def set_soft_shadows(self, enabled):
        self.__set_attribute('soft-shadows', int(enabled))

    def set_epsilon(self, epsilon):
        self.__set_attribute('epsilon', str(epsilon))

    def set_timestamp(self, timestamp):
        self.__set_attribute('timestamp', str(timestamp))

    def set_shader(self, shader):
        self.__set_attribute('material', shader)

    def set_renderer(self, renderer):
        self.__set_attribute('renderer', renderer)

    def set_material(self, index, material):
        self.__request(self._url_material, 'PUT', material.serialize(index))

    def get_image_jpeg(self):
        response = self.__request(self._url_image_jpeg, 'GET')
        if response is None:
            return None
        payload = json.loads(response)
        jpeg_image = Image.open(BytesIO(base64.b64decode(payload['data'])))
        return jpeg_image

    def get_frame_buffer(self, frame_type):
        response = self.__request(self._url_frame_buffers, 'GET')
        if response is None:
            return None
        payload = json.loads(response)
        size = [payload['width'], payload['height']]
        if frame_type == FRAMEBUFFER_COLOR:
            return Image.frombytes('RGBA', size, base64.b64decode(payload['diffuse']))
        elif frame_type == FRAMEBUFFER_DEPTH:
            return Image.frombytes('I;16', size, base64.b64decode(payload['depth']))
        return None

    def set_transfer_function(self, transfer_function):
        self.__request(self._url_transfer_function, 'PUT', transfer_function.serialize())

    def __set_attribute(self, key, value):
        payload = {'key': key, 'value': value}
        self.__request(self._url_attribute, 'PUT', json.dumps(payload))

    @staticmethod
    def __request(url, method, body=None):
        response = None
        request = None
        try:
            if method == 'PUT':
                if body == '':
                    request = requests.put(url)
                else:
                    request = requests.put(url, data=body)
            elif method == 'GET':
                request = requests.get(url)
                response = str(request.text)
            request.close()
        except requests.exceptions.ConnectionError:
            print('ERROR: Failed to connect to Brayns, did you start it with the '\
                  '--zeroeq-http-server command line option?')
        return response
