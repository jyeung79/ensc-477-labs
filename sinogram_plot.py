import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftshift, ifft
from scipy import ndimage

def add_noise(sinogram, mean, std_dev, reduce_dose):
	# Function to simulate adding noise and reducing dose_level
	# reduce_dose is the factor of reduction of the image
	# Returns a sinogram [n x m]

	reduced_sino = sinogram/reduce_dose
	noisy_image = reduced_sino + np.random.normal(mean, std_dev, reduced_sino.shape)

	return noisy_image

def filtered_sino(sinogram, param_a):
	# Function to remove high frequency noise from the sinogram
	# returns a sinogram [n x m]

	# a - parameter that modulates roll off at high frequencies
	a = param_a
	filt_sino = np.zeros((sinogram.shape[0], sinogram.shape[1]))

	# Filter in time domain for windowed ramp filter in fourier doman
	# as refered to Waqas Akram
	# sin filter
	step_size = 2*np.pi/sinogram.shape[0]
	w = np.arange(-np.pi, np.pi, step_size)
	ramp_filter = abs(2/a*np.sin(a*w/2))
	# sinc filter
	sinc_filter = np.sin(a*w/2)/(a*w/2) 
	filter_proj = ramp_filter*sinc_filter**2

	# windowed ramp filter in fourier domain
	fourier_filt = fftshift(filter_proj)
	for i in range(sinogram.shape[1]):
		fourier_sino = fft(sinogram[:,i])
		temp_sino = fourier_sino * fourier_filt
		filt_sino[:,i] = np.real(ifft(temp_sino))

	return filt_sino

def back_proj(sinogram, theta):
	# Function to produce a backprojection image from the sinogram given at the angle theta
	# Returns an matrix [n x n]
	theta_rad = theta*np.pi/180 #np.cos/sin only accepts rads
	length = sinogram.shape[0] # number of projections	
	back_proj_image = np.zeros((length, length))
	_plot_shift = length/2

	# Why does the x or y coordinates have to be centered?
	# Can't they just start from [0, n] instead of [-n/2, n/2] where n = # of projections
	# The image is centered at [0, 0] instead of [n/2, n/2]
	x = np.arange(length)-_plot_shift
	y = np.arange(length)-_plot_shift
	# plots a grid of coordinates (xx,yy)
	xx, yy = np.meshgrid(x, y)

	l_rot = xx*np.cos(theta_rad)+yy*np.sin(theta_rad)
	l_rot = np.round(l_rot+_plot_shift).astype('int')

	# only accepts 
	x0, y0 = np.where((l_rot >= 0) & (l_rot <= (length-1)))
	
	# acquires the projection of the theta
	temp_sino = sinogram[:,theta]

	back_proj_image[x0, y0] = temp_sino[l_rot[x0, y0]]

	return back_proj_image

def recon_back_proj(sinogram, num_rotations):
	# Reconstructs the original image from all the backprojection images 
	# Returns an matrix [n x n]
	length = sinogram.shape[0]
	recon_matrix = np.zeros((length, length))

	if num_rotations > sinogram.shape[1]:
		num_angles = sinogram.shape[1]
	else:
		num_angles = num_rotations

	for theta in range(num_angles):
		proj_image = back_proj(sinogram, theta)
		recon_matrix += proj_image

	print(recon_matrix)
	plt.imshow(recon_matrix, cmap='gray', aspect='auto', origin = 'lower')
	plt.title('Reconstructed image')
	plt.xlabel('Coordinates: x ')
	plt.ylabel('Coordinates: y ')
	plt.show()
	return recon_matrix

# ----- main ------
sino_90_1 = np.loadtxt("90_1.txt", dtype='f', delimiter = '\t')
sino_90_5 = np.loadtxt("90_5.txt", dtype='f', delimiter = '\t')
sino_180_5 = np.loadtxt("180_5.txt", dtype='f', delimiter = '\t')
sino_360_1 = np.loadtxt("360_1.txt", dtype='f', delimiter = '\t')
sino_360_5 = np.loadtxt("360_5.txt", dtype='f', delimiter = '\t')

#recon_back_proj(sino_360_1, 180)

sino_1 = plt.imread("sino1.bmp")
sino_1_noise1 = add_noise(sino_1, 0, 1, 1)
sino_1_filtered_1 = filtered_sino(sino_1_noise1, 1)

plt.imshow(sino_1_filtered_1, cmap='gray', origin = 'lower')
plt.title('sino1 with added noise')
plt.xlabel('Number of Projections')
plt.ylabel('Angle of Rotation')
plt.show()

sino_1_noise2 = add_noise(sino_1, 0, 2, 2)
sino_1_filtered_2 = filtered_sino(sino_1_noise1, 1)

plt.imshow(sino_1_filtered_2, cmap='gray', origin = 'lower')
plt.title('sino1 with added noise')
plt.xlabel('Number of Projections')
plt.ylabel('Angle of Rotation')
plt.show()

sino_1_noise3 = add_noise(sino_1, 0, 5, 2)
sino_1_filtered_3 = filtered_sino(sino_1_noise1, 1)

plt.imshow(sino_1_filtered_3, cmap='gray', origin = 'lower')
plt.title('sino1 with added noise')
plt.xlabel('Number of Projections')
plt.ylabel('Angle of Rotation')
plt.show()

recon_back_proj(sino_1_filtered_1, 180)
recon_back_proj(sino_1_filtered_2, 180)
recon_back_proj(sino_1_filtered_3, 180)


'''
#print(sino_90_1)
#print(sino_90_5)
#print(sino_180_5)
#print(sino_360_1)
#print(sino_360_5)


# Transpose the dataset so that degrees is the y-axis and intensity? is the x-axis
plt.imshow(sino_360_5.T, cmap='gray', aspect='auto', origin = 'lower')
plt.title('sino 3600deg of 5deg step')
plt.xlabel('Number of Projections')
plt.ylabel('Rotation Step of 5deg step size')
plt.show()


#back_proj(sino_360_5, 72, 1)
#back_proj(sino_90_1, 15, 1)
#back_proj(sino_180_5, 18, 1)
#back_proj(sino_360_1, 57, 1)
#recon_back_proj(sino_360_1, 360)
'''
'''
filt_sino_1 = filtered_sino(sino_360_1, 0.1)
filt_sino_2 = filtered_sino(sino_360_1, 1.0)
filt_sino_3 = filtered_sino(sino_360_1, 10.0)

plt.imshow(filt_sino_1.T, cmap='gray', aspect='auto', origin = 'lower')
plt.show()
plt.imshow(filt_sino_2.T, cmap='gray', aspect='auto', origin = 'lower')
plt.show()
plt.imshow(filt_sino_3.T, cmap='gray', aspect='auto', origin = 'lower')
plt.show()
recon_back_proj(filt_sino_1, 360)
recon_back_proj(filt_sino_2, 360)
recon_back_proj(filt_sino_3, 360)
'''