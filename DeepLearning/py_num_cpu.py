import numpy as np

def nms_cpu(detects, thres):
    '''@params
            detects: np.ndarray [[xmin,ymin,xmax,ymax, score]]
            thres: IoU threshold(float)
       @return
            keep: keeped detections' index 
    '''
    xmins  = detects[:, 0]
    ymins  = detects[:, 1]
    xmaxs  = detects[:, 2]
    ymaxs  = detects[:, 3]
    scores = detects[:, 4]

    areas = (xmaxs - xmins + 1.) * (ymaxs - ymins + 1.)
    order = scores.argsort()[::-1] 

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        ixmins = np.maximum(xmins[i], xmins[order[1:]])
        iymins = np.maximum(ymins[i], ymins[order[1:]])
        ixmaxs = np.minimum(xmaxs[i], xmaxs[order[1:]])
        iymaxs = np.minimum(ymaxs[i], ymaxs[order[1:]])

        iws = np.maximum(ixmaxs - ixmins + 1., 0.)
        ihs = np.maximum(iymaxs - iymins + 1., 0.)

        inters = iws * ihs
        unions = areas + areas[order[1:]] - inters

        overlaps = inters / unions
        idxes = np.where(overlaps <= thres)[0]
        order = order[idxes + 1] 
    return keep