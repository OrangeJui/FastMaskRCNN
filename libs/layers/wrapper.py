# --------------------------------------------------------
# Mask RCNN
# Written by CharlesShang@github
# --------------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from . import anchor
from . import roi
from . import mask
from . import sample
from . import assign
from libs.boxes.anchor import anchors_plane

def anchor_encoder(gt_boxes, all_anchors, height, width, stride, indexs, scope='AnchorEncoder'):
  
  with tf.name_scope(scope) as sc:
    labels, bbox_targets, bbox_inside_weights, indexs = \
      tf.py_func(anchor.encode,
                 [gt_boxes, all_anchors, height, width, stride, indexs],
                 [tf.int32, tf.float32, tf.float32, tf.int32])

    labels = tf.convert_to_tensor(tf.cast(labels, tf.int32), name='labels')
    indexs = tf.convert_to_tensor(tf.cast(indexs, tf.int32), name='labels')
    bbox_targets = tf.convert_to_tensor(bbox_targets, name='bbox_targets')
    bbox_inside_weights = tf.convert_to_tensor(bbox_inside_weights, name='bbox_inside_weights')


    labels = tf.reshape(labels, (1, height, width, -1))
    indexs = tf.reshape(indexs, (1, height, width, -1))
    bbox_targets = tf.reshape(bbox_targets, (1, height, width, -1))
    bbox_inside_weights = tf.reshape(bbox_inside_weights, (1, height, width, -1))

  
    return labels, bbox_targets, bbox_inside_weights, indexs


def anchor_decoder(boxes, scores, all_anchors, ih, iw, scope='AnchorDecoder'):
  
  with tf.name_scope(scope) as sc:
    final_boxes, classes, scores, indexs = \
      tf.py_func(anchor.decode,
                 [boxes, scores, all_anchors, ih, iw],
                 [tf.float32, tf.int32, tf.float32, tf.int32])

    indexs = tf.convert_to_tensor(tf.cast(indexs, tf.int32), name='classes')
    final_boxes = tf.convert_to_tensor(final_boxes, name='boxes')
    classes = tf.convert_to_tensor(tf.cast(classes, tf.int32), name='classes')
    scores = tf.convert_to_tensor(scores, name='scores')

    indexs = tf.reshape(indexs, (-1, ))
    final_boxes = tf.reshape(final_boxes, (-1, 4))
    classes = tf.reshape(classes, (-1, ))
    scores = tf.reshape(scores, (-1, ))
  
    return final_boxes, classes, scores, indexs


def roi_encoder(gt_boxes, rois, num_classes, indexs, scope='ROIEncoder'):
  
  with tf.name_scope(scope) as sc:
    labels, bbox_targets, bbox_inside_weights, max_overlaps, indexs = \
      tf.py_func(roi.encode,
                [gt_boxes, rois, num_classes, indexs],
                [tf.int32, tf.float32, tf.float32, tf.float32, tf.int32]
                )
    labels = tf.convert_to_tensor(tf.cast(labels, tf.int32), name='labels')
    indexs = tf.convert_to_tensor(tf.cast(indexs, tf.int32), name='indexs')
    bbox_targets = tf.convert_to_tensor(bbox_targets, name='bbox_targets')
    bbox_inside_weights = tf.convert_to_tensor(bbox_inside_weights, name='bbox_inside_weights')

    labels = tf.reshape(labels, (-1, ))
    indexs = tf.reshape(indexs, (-1, ))
    bbox_targets = tf.reshape(bbox_targets, (-1, num_classes * 4))
    bbox_inside_weights = tf.reshape(bbox_inside_weights, (-1, num_classes * 4))
    max_overlaps = tf.reshape(max_overlaps,(-1, ))
  
    return labels, bbox_targets, bbox_inside_weights, max_overlaps, indexs


def roi_decoder(boxes, scores, rois, ih, iw, scope='ROIDecoder'):
  
  with tf.name_scope(scope) as sc:
    final_boxes, classes, scores = \
      tf.py_func(roi.decode,
                 [boxes, scores, rois, ih, iw],
                 [tf.float32, tf.int32, tf.float32])
    final_boxes = tf.convert_to_tensor(final_boxes, name='boxes')
    classes = tf.convert_to_tensor(tf.cast(classes, tf.int32), name='classes')
    scores = tf.convert_to_tensor(scores, name='scores')
    final_boxes = tf.reshape(final_boxes, (-1, 4))
    
    return final_boxes, classes, scores

# def mask_encoder_(gt_masks, gt_boxes, rois, num_classes, mask_height, mask_width, indexs, scope='MaskEncoder'):
  
#   with tf.name_scope(scope) as sc:
#     labels, mask_targets, mask_inside_weights, mask_rois, indexs = \
#       tf.py_func(mask.encode_,
#                  [gt_masks, gt_boxes, rois, num_classes, mask_height, mask_width, indexs],
#                  [tf.int32, tf.float32, tf.float32, tf.float32, tf.int32])

#     labels = tf.convert_to_tensor(tf.cast(labels, tf.int32), name='classes')
#     indexs = tf.convert_to_tensor(tf.cast(indexs, tf.int32), name='classes')
#     mask_targets = tf.convert_to_tensor(mask_targets, name='mask_targets')
#     mask_inside_weights = tf.convert_to_tensor(mask_inside_weights, name='mask_inside_weights')

#     labels = tf.reshape(labels, (-1,))
#     indexs = tf.reshape(indexs, (-1,))
#     mask_targets = tf.reshape(mask_targets, (-1, mask_height, mask_width, num_classes))
#     mask_inside_weights = tf.reshape(mask_inside_weights, (-1, mask_height, mask_width, num_classes))
#     mask_rois = tf.reshape(mask_rois,(-1, 4))
  
#   return labels, mask_targets, mask_inside_weights, mask_rois, indexs

def mask_encoder(gt_masks, gt_boxes, rois, num_classes, mask_height, mask_width, indexs, scope='MaskEncoder'):
  
  with tf.name_scope(scope) as sc:
    labels, mask_targets, mask_inside_weights, mask_rois, indexs = \
      tf.py_func(mask.encode,
                 [gt_masks, gt_boxes, rois, num_classes, mask_height, mask_width, indexs],
                 [tf.int32, tf.float32, tf.float32, tf.float32, tf.int32])

    labels = tf.convert_to_tensor(tf.cast(labels, tf.int32), name='classes')
    indexs = tf.convert_to_tensor(tf.cast(indexs, tf.int32), name='classes')
    mask_targets = tf.convert_to_tensor(mask_targets, name='mask_targets')
    mask_inside_weights = tf.convert_to_tensor(mask_inside_weights, name='mask_inside_weights')
    mask_rois = tf.convert_to_tensor(mask_rois, name='mask_rois')

    labels = tf.reshape(labels, (-1,))
    indexs = tf.reshape(indexs, (-1,))
    mask_targets = tf.reshape(mask_targets, (-1, mask_height, mask_width, num_classes))
    mask_inside_weights = tf.reshape(mask_inside_weights, (-1, mask_height, mask_width, num_classes))
    mask_rois = tf.reshape(mask_rois,(-1, 4))
  
    return labels, mask_targets, mask_inside_weights, mask_rois, indexs

def mask_decoder(mask_targets, rois, classes, ih, iw, scope='MaskDecoder'):
  
  with tf.name_scope(scope) as sc:
    Mask = \
      tf.py_func(mask.decode,
                 [mask_targets, rois, classes, ih, iw,],
                 [tf.float32])
    Mask = tf.convert_to_tensor(Mask, name='MaskImage')
    Mask = tf.reshape(Mask, (ih, iw))
  
    return Mask


def sample_wrapper(boxes, scores, indexs, is_training=True, only_positive=True, scope='SampleBoxes'):
  
  with tf.name_scope(scope) as sc:
    boxes, scores, batch_inds, indexs = \
      tf.py_func(sample.sample_rpn_outputs,
                 [boxes, scores, indexs, is_training, only_positive],
                 [tf.float32, tf.float32, tf.int32, tf.int32])
    boxes = tf.convert_to_tensor(boxes, name='Boxes')
    scores = tf.convert_to_tensor(scores, name='Scores')
    batch_inds = tf.convert_to_tensor(batch_inds, name='BatchInds')
    indexs = tf.convert_to_tensor(indexs, name='Indexs')

    boxes = tf.reshape(boxes, (-1, 4))
    batch_inds = tf.reshape(batch_inds, [-1])
    indexs = tf.reshape(indexs, [-1])
  
    return boxes, scores, batch_inds, indexs

def sample_with_gt_wrapper(boxes, scores, gt_boxes, indexs, is_training=True, only_positive=True, scope='SampleBoxesWithGT'):
  
  with tf.name_scope(scope) as sc:
    boxes, scores, batch_inds, indexs, mask_boxes, mask_scores, mask_batch_inds, mask_indexs = \
      tf.py_func(sample.sample_rpn_outputs_wrt_gt_boxes,
                 [boxes, scores, gt_boxes, indexs, is_training, only_positive],
                 [tf.float32, tf.float32, tf.int32, tf.int32, tf.float32, tf.float32, tf.int32, tf.int32])
    boxes = tf.convert_to_tensor(boxes, name='Boxes')
    scores = tf.convert_to_tensor(scores, name='Scores')
    batch_inds = tf.convert_to_tensor(batch_inds, name='BatchInds')
    indexs = tf.convert_to_tensor(indexs, name='Indexs')
    
    mask_boxes = tf.convert_to_tensor(mask_boxes, name='MaskBoxes')
    mask_scores = tf.convert_to_tensor(mask_scores, name='MaskScores')
    mask_batch_inds = tf.convert_to_tensor(mask_batch_inds, name='MaskBatchInds')
    mask_indexs = tf.convert_to_tensor(mask_indexs, name='Indexs')
  
    return boxes, scores, batch_inds, indexs, mask_boxes, mask_scores, mask_batch_inds, mask_indexs

def gen_all_anchors(height, width, stride, scales, scope='GenAnchors'):
  
  with tf.name_scope(scope) as sc:
    all_anchors = \
      tf.py_func(anchors_plane,
                 [height, width, stride, scales],
                 [tf.float64]
                 )
    all_anchors = tf.convert_to_tensor(tf.cast(all_anchors, tf.float32), name='AllAnchors')
    all_anchors = tf.reshape(all_anchors, (height, width, -1))
    
    return all_anchors

def assign_boxes(gt_boxes, tensors, layers, scope='AssignGTBoxes'):

    with tf.name_scope(scope) as sc:
        min_k = layers[0]
        max_k = layers[-1]
        assigned_layers = \
            tf.py_func(assign.assign_boxes, 
                     [ gt_boxes, min_k, max_k ],
                     tf.int32)
        assigned_layers = tf.reshape(assigned_layers, [-1])

        assigned_tensors = []
        for t in tensors:
            split_tensors = []
            for l in layers:
                tf.cast(l, tf.int32)
                inds = tf.where(tf.equal(assigned_layers, l))
                inds = tf.reshape(inds, [-1])
                split_tensors.append(tf.gather(t, inds))
            assigned_tensors.append(split_tensors)

        return assigned_tensors + [assigned_layers]

def sample_rcnn_outputs_wrapper(final_boxes, classes, cls2_prob, indexs, scope='instInference'):
    with tf.name_scope(scope) as sc:
        inst_boxes, inst_classes, inst_prob, batch_inds, inst_indexs = \
            tf.py_func(sample.sample_rcnn_outputs,
                       [final_boxes, classes, cls2_prob, indexs],
                       [tf.float32, tf.int32, tf.float32, tf.int32, tf.int32])

        inst_boxes = tf.convert_to_tensor(inst_boxes, name='instBoxes')
        inst_classes = tf.convert_to_tensor(inst_classes, name='instClasses')
        inst_prob = tf.convert_to_tensor(inst_prob, name='instProb')
        batch_inds = tf.convert_to_tensor(batch_inds, name='BatchInds')
        inst_indexs = tf.convert_to_tensor(inst_indexs, name='inst_indexs')

        return [inst_boxes] + [inst_classes] + [inst_prob] + [batch_inds] + [inst_indexs]