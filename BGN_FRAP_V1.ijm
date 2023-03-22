//PARAMETERS:
Dialog.create("Image correction, parameters:");
Dialog.addNumber("Rolling Ball Radius:",60);
Dialog.addNumber("Median filter Radius (spot radius):",5);
Dialog.addNumber("Number of frames for I0:",15);
Dialog.show();
//	- rolling ball radius
r=Dialog.getNumber();
//	- radius for the median filtering
rm=Dialog.getNumber();
//  - N
N=Dialog.getNumber();
// 	- image name
original_image_name=getTitle();
run("Set Scale...", "distance=0 known=0 unit=pixel");
if ( matches( original_image_name , ".*.stk" ) ) {
	tif_image_name=replace( original_image_name , ".stk" , ".tif" );
} else {
	tif_image_name = original_image_name ;
}
//	- image directory
dir=getDirectory("image");

//duplicate the original image and run the local
//background subtraction
run("Duplicate...", "duplicate");
//local background subtraction
run("Subtract Background...", "rolling="+r+" stack");
//get its name
image_name=getTitle();

//Compute the selection
//duplicate the image and run a median filter to 
//smoothen the selection.
//That is important for speed purposes.
run("Duplicate...", "title=median_filtered_image.tif duplicate");
run("Median...", "radius="+rm+" stack");
//compute the mask
//setOption("BlackBackground", true);
run("Duplicate...", "title=mask.tif duplicate range=1-2");
run("Convert to Mask", "method=Li background=Dark calculate black");
//create the selection for corr_bleach
run("Create Selection");
//Measure the values in the selection
selectWindow("median_filtered_image.tif");
run("Restore Selection");
run("Measure Stack...");

//normalize the raw image
selectWindow(image_name);
for(l=0; l<N; l++) {
	I0+=getResult("Mean",l);
}
I0 = I0 / N ;
print( I0 );
for(l=0; l<nSlices; l++) {
	I=getResult("Mean",l);
	scale_factor=I0/I;
	setSlice(l+1);
	run("Multiply...", "value=" + scale_factor + " slice");
}

//save it
normalized_output_name=replace(tif_image_name,".tif","_FRAPN.tif");
saveAs("Tiff", dir+normalized_output_name);
//clean up

//select the normalized image
selectWindow(normalized_output_name);
//remove the cytoplasmatic background
imageCalculator("Subtract create stack", normalized_output_name,"median_filtered_image.tif");
//save it

md_output_name=replace(tif_image_name,".tif","_FRAPN_MD.tif");
saveAs("Tiff", dir+md_output_name);

//clean up
selectWindow(normalized_output_name);
close();

selectWindow("median_filtered_image.tif");
close();

selectWindow(original_image_name);
close();
