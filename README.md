# shopifyImageColorML
Attempts to pull the most dominant color from a product/variant image in shopify via API calls and a sklearn ML algorithm. The python algorithm outputs its best attempt at gathering the most dominant color, and makes another API call to shopify, tagging the image with a metafield containing a hex color. 
