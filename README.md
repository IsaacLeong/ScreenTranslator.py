# ScreenTranslator.py
## Description:
<p>Application is an experimental project to translate foreign languages on a screen developed in <i>python</i>. Note: the application is currently not optimised to handle images with large amounts of background noise or filter non-sense words<p>
<p>following open-source libraries were used:</p>
<li> PyQt </li>
<li> OpenCV </li>
<li> PyAutoGUI </li>
<li> PyTesseractOCR </li>
<li> GoogleTrans </li>

## Application Structure:
```
1. application gets coordinates and dimensions after being loaded through cmd
2. screenshot with the dimensions is taken
3. individual frame is processed using pytesseract
4. translated text is converted by googletrans 
5. image is displayed on a PyQt Label
6. label is refreshed back to step 2 until user exits (refresh time set to 5 seconds)
```

## Log:
<b>V.01.2 - 28/08/20</b>
<p><i>Added:</i></p>
<li> + Langauge Options Added 1/2</li>
<p><i>Fixes:</i></p>
<li> + Bypass for refresh label function </li>


<b>V.01.1 - 25/08/20</b>
<p><i>Added:</i></p>
<li> + Update button for UI</li>
<p><i>Fixes:</i></p>
<li> None </li>


<b>V.01 - 24/08/20</b>
<p><i>Added:</i></p>
<li> + Base application functionality complete
<p><i>Bugs + Issues:</i></p>
<li> - Application should be more dynamic in getting screen capture
<li> - Non-sense words not filtered
<li> - OCR not optimised for multiple variants (i.e. high-noise, hand-writing, skewed, etc.)
  
## Future Considerations:
<p>Using NLTK to improve translations accuracy
<p>Google Vision to handle OCR
<p>Lanugage detection open reading
<p>Improve the display as an overlay instead of 
<p>Multithread application to run smoother
