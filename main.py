import numpy as np
import imageio.v2 as imageio  # Explicit use of imageio.v2
import cv2
import scipy.ndimage


def convert_to_grayscale(rgb_image):
    """
    Converts an RGB image to grayscale.
    """
    return np.dot(rgb_image[..., :3], [0.299, 0.587, 0.114])


def apply_dodge(front_layer, back_layer):
    """
    Applies the 'dodge' effect to create a pencil sketch effect.
    """
    result = front_layer * 255 / (255 - back_layer)
    result[result > 255] = 255
    result[back_layer == 255] = 255
    return result.astype('uint8')


def pencil_sketch(image_path, output_path, blur_sigma=10):
    """
    Generates a pencil sketch effect from an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to the output image.
        blur_sigma (float): Sigma for the Gaussian blur (defines the blur level).
    """
    # Load the image
    original_image = imageio.imread(image_path)

    # Convert to grayscale
    grayscale_image = convert_to_grayscale(original_image)

    # Invert the colors
    inverted_image = 255 - grayscale_image

    # Apply Gaussian blur
    blurred_image = scipy.ndimage.gaussian_filter(inverted_image, sigma=blur_sigma)

    # Apply the dodge effect
    final_image = apply_dodge(blurred_image, grayscale_image)

    # Save the resulting image
    cv2.imwrite(output_path, final_image)
    print(f"The image has been saved to '{output_path}'.")


# Example usage
if __name__ == "__main__":
    input_image = "test.jpeg"
    output_image = "test_coloring.png"
    pencil_sketch(input_image, output_image)