# DocScanner
Scan your documents just like CamScanner with added OMR 

### Requirements
You can install Conda for python which resolves all the dependencies for this project
or run 
`pip install requirements.txt`

### Description
Find rectangled-shaped documents in an image and show a clearer and top-down view of them.
Scan sheets and use OMR to score an OMR sheet.

### Execution
After reproducing the repo in your device, to run the code,
Type `python scan.py` for scanning module or `cd omr` followed by `python omr.py` for OMR module.

### Functionalities
1) Sources of detection can be - Image file
2) Apply filter for a clearer image
3) OMR module

### To-do
- [ ] OCR functionality
- [x] OMR functionality
- [ ] Save to PDF option
- [ ] Provide options to change filters

### References
1) https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
2) https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/

Thanks Adrian Rosebrock for inspiring me!

### Sample

#### Scanning
<img src="https://github.com/parthagar/DocScanner/blob/master/images/Capture_Scan.PNG">

#### OMR
<img src="https://github.com/parthagar/DocScanner/blob/master/images/Capture_OMR.PNG">
 
