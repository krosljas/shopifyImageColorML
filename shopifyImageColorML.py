import sys
from sklearn.cluster import KMeans
from collections import Counter
import numpy
import cv2
import shopify

API_KEY = 'ddf972d21428a9fee5506bd48b12652b'
PASSWORD = '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'
API_VERSION = '2020-01'
shop_url = "https://%s:%s@jason-kroslowitz.myshopify.com/admin/api/%s" % (API_KEY, PASSWORD, API_VERSION)
shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()


url = sys.argv[1]


#Helper function to convert raw RGB data from opencv to hexadecimal
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex
    
    
#Read in an image from an internet URL 
#Kind of hacky taking advantage of VideoCapture object
#May be inefficient but beats downloading images
def captureImageFromURL(url, readFlag=cv2.IMREAD_COLOR):
    cap = cv2.VideoCapture(url)
    if( cap.isOpened() ) :
        res,img = cap.read()
        cv2.waitKey()
        print("Success")
        return img

#Current attempt at getting what the ML algorithm 
#Determines to be the most frequent color in an image
#Out of all the present colors in the image
#Based on return values 'ordered_colors'
def getMainColor(counts):
    counts = list(counts)
    max_val = counts[0]
    max_idx = 0
    for i in range( 1, len(counts) ):
        if counts[i] > max_val:
            max_val = counts[i]
            max_idx = i
    return max_idx
    
def processImage(img, k=6):

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_img_rgb = cv2.resize(img_rgb, (64, 64), interpolation=cv2.INTER_AREA)
    img_list = resized_img_rgb.reshape((resized_img_rgb.shape[0] * resized_img_rgb.shape[1], 3))
    
    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(img_list)
    
    label_counts = Counter(labels)
    total_count = sum(label_counts.values())
    
    center_colors = list(clt.cluster_centers_)
    ordered_colors = [center_colors[i]/255 for i in label_counts.keys()]
    color_labels = [rgb2hex(ordered_colors[i]*255) for i in label_counts.keys()]
    
    color_idx = getMainColor(label_counts.values())
    #print(label_counts.values())
    #print(color_labels)
    #print(ordered_colors)
    print(color_labels[color_idx])
    sys.stdout.flush()
    return color_labels[color_idx]
    

img = captureImageFromURL(url)
color_label = processImage(img)
product = shopify.Product.find(5305581600812)
product.add_metafield(shopify.Metafield({
    'key': 'swatch_hex_value',
    'value': color_label,
    'value_type': 'string',
    'namespace': 'swatch_data'
    }))
