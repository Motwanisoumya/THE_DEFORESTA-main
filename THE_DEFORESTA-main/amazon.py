import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def difference(ng1, ng2):
    Gaus = cv.GaussianBlur(ng1, (5, 5), 0) 
    thresh1, bin1 = cv.threshold(Gaus, 0, 255, cv.THRESH_OTSU) 
    Gaus = cv.GaussianBlur(ng2, (5, 5), 0)
    thresh2, bin2 = cv.threshold(Gaus, 0, 255, cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))
    morph1 = cv.morphologyEx(bin1, cv.MORPH_CLOSE, kernel)
    morph2 = cv.morphologyEx(bin2, cv.MORPH_CLOSE, kernel)
    Diff = np.bitwise_xor(morph1, morph2)
    return Diff

def color_diff(img, diff_img):
    img_rgb = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    contours, _ = cv.findContours(diff_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area < 1000:  # Green for contours with area less than 1000
            color = [255, 127, 127]
        elif area < 3500:  # Blue for contours with area between 1000 and 2500
            color = [255, 60, 60]
        else:  # Red for contours with area greater than 2500
            color = [139, 40, 40]
        cv.drawContours(img_rgb, [contour], -1, color, -1)
    return img_rgb       

def load_images_from_folder(folder):
    images = []
    filenames = sorted(os.listdir(folder))  # sort filenames in ascending order
    for filename in filenames:
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            img = cv.imread(img_path, 0)  
            if img is not None:
                images.append(img)
    return images 

def compute_deforestation(folder):
    images = load_images_from_folder(folder)
    diffs = []
    years = []
    percentages = []

    for i in range(len(images) - 1):
        diffs.append(difference(images[i], images[i+1]))
        years.append(f"{i+1}")

    for diff in diffs:
        total_curvature_diff = np.sum(diff) / 255
        percentages.append(float('{0:.2f}'.format(total_curvature_diff / diff.size * 100)))

    return years, percentages, images, diffs

def plot_deforestation(years, percentages, diffs, images):
    plt.figure(figsize=(18, 10))
    for i in range(len(years)):
       
        plt.subplot(3, 5, 2*i+1)
        plt.imshow(images[i], cmap='gray')
        plt.title(f"Actual Image: {years[i]}")
        plt.axis('off')

        
        plt.subplot(3, 5, 2*i+2)
        img_diff = color_diff(images[i], diffs[i])
        plt.imshow(img_diff)
        plt.title(f"Difference: {years[i]}->{int(years[i])+1}")
        plt.axis('off')

    
    plt.subplot(3, 5, 2*len(years)+1)
    plt.imshow(images[-1], cmap='gray')
    plt.title(f"Actual Image: {int(years[-1])+1}")
    plt.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join("./frontend/static/solution", 'deforestation1.png'))

   
    x = [f"{years[i]}-{int(years[i])+1}" for i in range(len(years))]
    y = percentages
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o')
    plt.xlabel('Years')
    plt.ylabel('Percentages')
    plt.title('Rate of Deforestation')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join("./frontend/static/solution", 'deforestation2.png'))








def main():
    folder_path = "./frontend/static/display"
    years, percentages, images, diffs = compute_deforestation(folder_path)
    plot_deforestation(years, percentages, diffs, images)

if __name__ == "__main__":
    main()




