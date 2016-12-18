# RealismIsRandom
This is my second tool for Maya. It should work in Maya 2015, 2016(not tested) and 2017.
It applys random transformations to the selected objects.

# How to install:
1. Download as .zip.
2. Create RealismIsRandom folder in User/Documents/maya/MAYAVERSION/scripts/ .
3. Extract to that folder.

# How to use:
1. Drag and Drop the RIR_Start.mel file into your open maya scene or copy and paste the code into a shelf button.
2. Select the objects you want to transform randomly.
3. Change some settings, save them as preset if you want to or choose a preset.
4. Hit the Apply Transfom button.
5. As long as you don't change the selection you can undo the transforms with the Reset Transform button.

# Notes:
1. Scale is additive for now.
2. Transformations done with this tool are not undoable with Ctrl+Z you need to use the button.

# TODO:
1. Integrate into maya undo so that it works with Ctrl+Z
2. Rework interface and add a few more handy options.
3. Create a help-popup.
