import pickle5 as pickle
import numpy as np
from OpenGL.GL import *

def transpose_image(im, w, h):
    return np.rot90(im.reshape(h,w), k=1).flatten()
    #return im.reshape(h,w).T.T.flatten()

class SpectralHandler:

    def __init__(self, path):
        self.load(path)


    def load(self, path):

        with open(path, 'rb') as f:
            render_pickle = pickle.load(f)
            self.r_wl_min = render_pickle["wl_min"]
            self.r_wl_max = render_pickle["wl_max"]
            self.r_wl_samples = render_pickle["wl_samp"]
            self.width = render_pickle["width"]
            self.height = render_pickle["height"]
            self.images = render_pickle["data"]

            # self.images = np.array([transpose_image(im, self.width, self.height) for im in self.images])
            # self.images = self.images.transpose()
            print("images:", self.images, sep="\n")
            print("Loaded spectral render of scene {} ({}x{} {} spp). Spectrum range: {}..{} ({} samples).\n".format(render_pickle["scene_name"],self.width,self.height,render_pickle["spp"],self.r_wl_min,self.r_wl_max,self.r_wl_samples))
            # exit(0)
            #im = self.images[0]
            print(len(self.images[0]), self.width, self.height, ":", len(self.images[0])//self.width,len(self.images[0])//self.height)
            # tx_image = cv2.flip(im, 0)
            assert self.r_wl_samples == self.images.shape[0]


    def init(self):
        self.tex_obj = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.tex_obj)
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_R32F, self.width, self.height, self.r_wl_samples, 0, GL_RED, GL_FLOAT, None)
        # glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_RED, self.width, self.height, self.r_wl_samples)
        for i, im in enumerate(self.images): # for each grayscale spectral image
            # convert to byte array:
            #im = transpose_image(im, self.width, self.height)
            #bytearray(im)
            # print(img_data) # GL_UNSIGNED_BYTE
            # im = im.astype(np.float32)

            glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, i, self.width, self.height, 1, GL_RED, GL_FLOAT, im)
        glTexParameterf(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
