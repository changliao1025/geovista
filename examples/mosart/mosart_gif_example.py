import os
import glob
import imageio

def create_gif(filenames, output_gif, duration=0.5):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    
    # Create the GIF
    imageio.mimsave(output_gif, images, duration=duration, loop=0)

if __name__ == "__main__":
    # List of filenames of images to include in the GIF

    #sFolder_png = r'Z:\04model\e3sm\amazon\analysis\e3sm20240102002\flooded_fraction\png'
    sFolder_png = r'Z:\04model\e3sm\amazon\analysis\e3sm20240102002\main_channel_water_depth_liq\png'
    file_extension = '.png'

    # Use glob to get all files with the specified extension
    aFilename = glob.glob(os.path.join(sFolder_png, f'*{file_extension}'))
    aFilename = sorted(aFilename)
    print(aFilename)
    # Output GIF filename
    output_gif = r"C:\workspace\python\geovista\data\mosart\amazon\main_channel_water_depth_liq.gif"
    
    # Duration (in seconds) for each frame
    duration = 0.5
    
    # Call the function to create the GIF
    create_gif(aFilename, output_gif, duration=duration)
