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

class FovCamera(object):

    def __init__(self, origin, lookAt, up, aperture, focal_length):
        self._origin = origin
        self._lookAt = lookAt
        self._up = up
        self._aperture = aperture
        self._focal_length = focal_length

    def serialize(self):
        payload = {
            "origin": {
                "x": self._origin[0],
                "y": self._origin[1],
                "z": self._origin[2]
            },
            "lookAt": {
                "x": self._lookAt[0],
                "y": self._lookAt[1],
                "z": self._lookAt[2]
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
        self._lookAt[0] = obj['lookAt']['x']
        self._lookAt[1] = obj['lookAt']['y']
        self._lookAt[2] = obj['lookAt']['z']
        self._up[0] = obj['up']['x']
        self._up[1] = obj['up']['y']
        self._up[2] = obj['up']['z']
        self._aperture = obj['fovAperture']
        self._focal_length = obj['fovFocalLength']

    def __str__(self):
        return 'Origin: ' + str(self._origin) + \
               ', Target: ' + str(self._lookAt) + \
               ', Up: ' + str(self._up) + \
               ', Aperture: ' + str(self._aperture) + \
               ', Focal length: ' + str(self._focal_length)


class Material(object):
    def __init__(self, index, diffuse_color, specular_color, specular_exponent, \
                 opacity, refraction_index, reflection_index, light_emission):
        self._index = index
        self._diffuse_color = diffuse_color
        self._specular_color = specular_color
        self._specular_exponent = specular_exponent
        self._opacity = opacity
        self._refraction_index = refraction_index
        self._reflection_index = reflection_index
        self._light_emission = light_emission

    def serialize(self):
        payload = {
            "index": self._index,
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
        self._index = obj['index']
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

        self.SHADER_DIFFUSE = 0
        self.SHADER_ELECTRON = 1
        self.SHADER_NOSHADING = 2

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

    def set_background_color(self, background_color):
        value = str(background_color[0]) + ' ' +\
                str(background_color[1]) + ' ' +\
                str(background_color[2])
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
        value = None
        if shader == self.SHADER_DIFFUSE:
            value = 'diffuse'
        elif shader == self.SHADER_ELECTRON:
            value = 'electron'
        elif shader == self.SHADER_NOSHADING:
            value = 'noshading'
        else:
            print('Unknown shader')
        if value != None:
            self.__set_attribute('material', value)

    def set_material(self, material):
        self.__request(self._url_material, 'PUT', material.serialize())

    def get_image_jpeg(self):
        response = self.__request(self._url_image_jpeg, 'GET')
        if response == None:
            return None
        payload = json.loads(response)
        jpeg_image = Image.open(BytesIO(base64.b64decode(payload['data'])))
        return jpeg_image

    def __set_attribute(self, key, value):
        payload = {'key': key, 'value': value}
        self.__request(self._url_attribute, 'PUT', json.dumps(payload))

    def __request(self, url, method, body = None):
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
        except requests.exceptions.ConnectionError as e:
            print('ERROR: Failed to connect to Brayns, did you start it with the '\
                  '--zeroeq-http-server command line option?')
        return response