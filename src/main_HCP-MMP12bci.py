# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
import scipy as sp
import nibabel.freesurfer.io as fsio
from surfproc import view_patch_vtk, patch_color_labels, smooth_patch
from dfsio import writedfs, readdfs
from nibabel.gifti.giftiio import read as gread
import os
from scipy.spatial import cKDTree


p_dir_ref='/home/ajoshi/HCP_data'
ref_dir = os.path.join(p_dir_ref, 'reference')
outbasename = 'BCI-HCP_MMP1'



def interpolate_labels(fromsurf=[], tosurf=[]):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    tosurf.labels = fromsurf.labels[inds]
    return tosurf


def multidim_intersect(arr1, arr2):
    arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    intersected = sp.intersect1d(arr1_view, arr2_view)
    return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

inputfile='/big_disk/ajoshi/data/HCP_MMP1.0_fsaverage/3498446/rh.HCP-MMP1.annot'
fsavesurf='/big_disk/ajoshi/freesurfer/subjects/fsaverage/surf/rh.sphere.reg.avg'
yeomap,_,_=fsio.read_annot(inputfile)
vert,faces=fsaverage_surf=fsio.read_geometry(fsavesurf)
class s:
    pass



s.vertices=vert; s.faces=faces;s.labels=yeomap

class bs:
    pass

class bci:
    pass

''' map to bc sphere'''
bs.vertices, bs.faces = fsio.read_geometry(
    '/big_disk/ajoshi/fs_sub/BCI_DNI_Atlas/surf/rh.sphere.reg')
bs = interpolate_labels(s, bs)
bci.vertices, bci.faces = fsio.read_geometry(
    '/big_disk/ajoshi/fs_sub/BCI_DNI_Atlas/surf/rh.white')
bci.labels = bs.labels
writedfs('BCI_orig_rh.dfs', bci)


bci.vertices, bci.faces = fsio.read_geometry(
    '/big_disk/ajoshi/fs_sub/BCI_DNI_Atlas/surf/rh.inflated')
bci = patch_color_labels(bci)
view_patch_vtk(bci)

writedfs('BCI_pial_rh.dfs.', bci)

bci.vertices, bci.faces = fsio.read_geometry(
    '/big_disk/ajoshi/fs_sub/BCI_DNI_Atlas/surf/rh.white')
writedfs('BCI_white_rh.dfs.', bci)


bci.vertices[:, 0] += 96*0.8
bci.vertices[:, 1] += 192*0.546875
bci.vertices[:, 2] += 192*0.546875
bci_bst = readdfs(
    '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.inner.cortex.dfs')
bci_bst = interpolate_labels(bci, bci_bst)
bci_bst_mid = readdfs(
    '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs')
bci_bst.vertices = bci_bst_mid.vertices

bci_bst = smooth_patch(bci_bst, iterations=3000, relaxation=.5)
bci_bst = patch_color_labels(bci_bst)
writedfs(outbasename + '.right.mid.cortex.dfs', bci_bst)


view_patch_vtk(bci_bst)
