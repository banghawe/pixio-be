from skimage.color import rgb2ycbcr
from skimage.segmentation import slic
from scipy.ndimage.filters import median_filter

from .utils import *


class BlockArtifactGrid:
    def __init__(self, image):
        self.image = image
        self.result_percentage = 0
        self.result_image = []
        self.segments = 70
        self.sigma = 5
        self.color = 'cr'
        self.min_lbl = 0.7
        self.differ_treshold = 50
        self.accum_col = 33
        self.median_filter_size = 3
        self.progress = 0

    def __horizontal_extraction(self, chosen_img_layer):
        padded_img_horz = mirror_pad_image(chosen_img_layer, 0, self.accum_col // 2)

        M, N = padded_img_horz.shape

        differ_horz = np.zeros((M, N))
        for i in range(1, M - 1):
            for j in range(N):
                differ_horz[i, j] = 2 * padded_img_horz[i, j] - padded_img_horz[i - 1, j] - padded_img_horz[i + 1, j]

        differ_horz: np.ndarray = np.absolute(differ_horz)
        differ_horz: np.ndarray = median_filter(differ_horz, size=self.median_filter_size)

        for i in range(1, M - 1):
            for j in range(N):
                if differ_horz[i, j] > self.differ_treshold:
                    differ_horz[i, j] = self.differ_treshold

        for j in range(N):
            differ_horz[0, j] = differ_horz[1, j]
            differ_horz[M - 1, j] = differ_horz[M - 2, j]

        summed_horz = sum_fiter_horz(differ_horz, self.accum_col)
        summed_horz_pad = mirror_pad_image(summed_horz, self.accum_col // 2, 0)
        med_vert = median_fiter_vert(summed_horz_pad, self.accum_col)

        edge_horz = summed_horz - med_vert
        edge_horz_pad = mirror_pad_image(edge_horz, self.accum_col // 2, 0)
        med_8step_vert = median_filter_8step_vert(edge_horz_pad, self.accum_col)

        return med_8step_vert

    def __vertical_extraction(self, chosen_img_layer):
        padded_img_vert = mirror_pad_image(chosen_img_layer, self.accum_col // 2, 0)

        M, N = padded_img_vert.shape

        differ_vert = np.zeros((M, N))
        for i in range(M):
            for j in range(1, N - 1):
                differ_vert[i, j] = 2 * padded_img_vert[i, j] - padded_img_vert[i, j + 1] - padded_img_vert[i, j - 1]

        differ_vert: np.ndarray = np.absolute(differ_vert)
        differ_vert = median_filter(differ_vert, size=self.median_filter_size)

        for i in range(M):
            for j in range(1, N - 1):
                if differ_vert[i, j] > self.differ_treshold:
                    differ_vert[i, j] = self.differ_treshold

        for i in range(M):
            differ_vert[i, 0] = differ_vert[i, 1]
            differ_vert[i, N - 1] = differ_vert[i, N - 2]

        summed_vert = sum_fiter_vert(differ_vert, self.accum_col)
        summed_vert_pad = mirror_pad_image(summed_vert, 0, self.accum_col // 2)
        med_horz = median_fiter_horz(summed_vert_pad, self.accum_col)

        edge_vert = summed_vert - med_horz
        edge_vert_pad = mirror_pad_image(edge_vert, 0, self.accum_col // 2)
        med_8step_horz = median_filter_8step_horz(edge_vert_pad, self.accum_col)

        return med_8step_horz

    def detect(self, progress_action=None):
        ycbcr_img = rgb2ycbcr(self.image)

        segmented_img = slic(self.image, n_segments=self.segments, sigma=self.sigma)
        self.progress += 5
        progress_action and progress_action(self.progress)

        if self.color == 'y':
            chosen_img_layer = ycbcr_img[:, :, 0]
        elif self.color == 'cb':
            chosen_img_layer = ycbcr_img[:, :, 1]
        else:
            chosen_img_layer = ycbcr_img[:, :, 2]

        # Horizontal
        extracted_horz_img = self.__horizontal_extraction(chosen_img_layer)
        self.progress += 30
        progress_action and progress_action(self.progress)

        # Vertical
        extracted_vert_img = self.__vertical_extraction(chosen_img_layer)
        self.progress += 30
        progress_action and progress_action(self.progress)

        # BAG
        bag = extracted_vert_img + extracted_horz_img

        block = block_process(bag)
        self.progress += 15
        progress_action and progress_action(self.progress)

        normal_block = np.zeros((block.shape))

        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i, j] > np.mean(block):
                    normal_block[i, j] = 1

        label_map = np.zeros((np.size(chosen_img_layer, 0), np.size(chosen_img_layer, 1)))

        for i in range(len(normal_block)):
            for j in range(len(normal_block[i])):
                for ii in range(8):
                    for jj in range(8):
                        label_map[ii + (i * 8), jj + (j * 8)] = normal_block[i, j]
        self.progress += 10
        progress_action and progress_action(self.progress)

        for (i, seg_val) in enumerate(np.unique(segmented_img)):
            mean_segment = np.mean(label_map[segmented_img == seg_val])
            if mean_segment < self.min_lbl:
                label_map[segmented_img == seg_val] = 0
            else:
                label_map[segmented_img == seg_val] = 1
        self.progress += 10
        progress_action and progress_action(self.progress)

        self.result_image = label_map
