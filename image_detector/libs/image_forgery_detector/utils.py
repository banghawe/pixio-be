import numpy as np


def mirror_pad_image(image, pad_row, pad_col):
    """
    Fungsi untuk menambah array/pad pada tepi citra
    Penambahan pad menggunakan mirroring
    """
    row = np.size(image, 0)
    col = np.size(image, 1)

    paddedYX = np.zeros((row + 2 * pad_row, col + 2 * pad_col))

    for i in range(pad_row, row + pad_row):
        for j in range(pad_col, col + pad_col):
            paddedYX[i, j] = image[i - pad_row, j - pad_col]

    # Mirror X

    padded_img = np.copy(paddedYX)

    for i in range(pad_row):
        for j in range(np.size(paddedYX, 1)):
            padded_img[i, j] = padded_img[2 * pad_row - i, j]
            padded_img[np.size(paddedYX, 0) - i - 1, j] = padded_img[np.size(paddedYX, 0) - 2 * pad_row + i - 1, j]

    # Mirror Y

    for j in range(pad_col):
        for i in range(np.size(paddedYX, 0)):
            padded_img[i, j] = padded_img[i, 2 * pad_col - j]
            padded_img[i, np.size(paddedYX, 1) - j - 1] = padded_img[i, np.size(paddedYX, 1) - 2 * pad_col + j - 1]

    return padded_img


def sum_fiter_horz(image, filter_size):
    """
    Fungsi untuk menjumlah secara horizontal, antar kolom
    """
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row, img_col - 2 * offset))

    for i in range(img_row):
        sum = 0
        for jj in range(2 * offset + 1):
            sum = sum + image[i, jj]

        filtered_img[i, 0] = sum
        for j in range(offset + 1, img_col - filter_size + offset):
            sum = sum - image[i, j - offset - 1]
            sum = sum + image[i, j + offset]
            filtered_img[i, j - offset] = sum

    return filtered_img


def median_fiter_vert(image, filter_size):
    """
    Fungsi untuk mencari median secara vertical antar row
    """
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row - 2 * offset, img_col))

    for j in range(img_col):
        for i in range(img_row - 2 * offset):
            counter = 0
            temp = np.zeros((filter_size - 1))

            for k in range(i, i + filter_size - 1):
                temp[counter] = image[k, j]
                counter += 1

            temp = np.sort(temp)
            filtered_img[i, j] = temp[offset + 1]

    return filtered_img


def median_filter_8step_vert(image, filter_size):
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row - 2 * offset, img_col))

    for i in range(offset, img_row - offset):
        for j in range(img_col):
            temp = np.zeros((5))
            counter = 0

            for k in range(-16, 16, 8):
                temp[counter] = image[i + k, j]
                counter = counter + 1

            temp = np.sort(temp)
            filtered_img[i - offset, j] = temp[3]

    return filtered_img


def sum_fiter_vert(image, filter_size):
    """
    Fungsi untuk menjumlah secara vertikal antar row
    """
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row - 2 * offset, img_col))

    for j in range(img_col):
        sum = 0
        for ii in range(2 * offset + 1):
            sum = sum + image[ii, j]

        filtered_img[0, j] = sum
        for i in range(offset + 1, img_row - filter_size + offset):
            sum = sum - image[i - offset - 1, j]
            sum = sum + image[i + offset, j]
            filtered_img[i - offset, j] = sum

    return filtered_img


def median_fiter_horz(image, filter_size):
    """
    Fungsi untuk mencari median secara vertikal antar row
    """
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row, img_col - 2 * offset))

    for j in range(img_row):
        for i in range(img_col - 2 * offset):
            counter = 0
            temp = np.zeros((filter_size))
            for k in range(i, i + filter_size):
                temp[counter] = image[j, k]
                counter = counter + 1

            temp = np.sort(temp)
            filtered_img[j, i] = temp[offset + 1]

    return filtered_img


def median_filter_8step_horz(image, filter_size):
    offset = filter_size // 2
    img_row = np.size(image, 0)
    img_col = np.size(image, 1)
    filtered_img = np.zeros((img_row, img_col - 2 * offset))

    for ii in range(img_row):
        for jj in range(offset, img_col - offset):
            temp = np.zeros((5))
            counter = 0
            for kk in range(-16, 16, 8):
                temp[counter] = image[ii, jj + kk]
                counter = counter + 1

            temp = np.sort(temp)
            filtered_img[ii, jj - offset] = temp[3]

    return filtered_img


def block_check(blok):
    row_sum = np.zeros((6))
    col_sum = np.zeros((6))
    row_edge = np.zeros((2))
    col_edge = np.zeros((2))

    for i in range(1, 7):
        for j in range(1, 7):
            row_sum[i - 1] = row_sum[i - 1] + blok[i, j]
            col_sum[j - 1] = col_sum[j - 1] + blok[j, i]

        row_edge[0] = row_edge[0] + blok[i, 0]
        row_edge[1] = row_edge[1] + blok[i, 7]

    for j in range(1, 7):
        col_edge[0] = col_edge[0] + blok[0, j]
        col_edge[1] = col_edge[1] + blok[7, j]

    max1 = np.amax(row_sum)
    max2 = np.amax(col_sum)
    min1 = np.amin(row_edge)
    min2 = np.amin(col_edge)

    return int(max1 + max2 - min1 - min2)


def block_process(img):
    """
    Fungsi untuk memproses BAG
    """
    img_row = np.size(img, 0)
    img_col = np.size(img, 1)
    outArray = np.zeros((int(img_row / 8) - 1, int(img_col / 8) - 1))

    block = np.zeros((8, 8))
    for i in range(0, img_row - 8, 8):
        for j in range(0, img_col - 8, 8):
            for ii in range(i, i + 8):
                for jj in range(j, j + 8):
                    block[ii - i, jj - j] = img[ii, jj]

            outArray[int(i / 8) - 1, int(j / 8) - 1] = block_check(block)

    return outArray
