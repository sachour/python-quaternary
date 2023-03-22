# python-quaternary
Rudimentary library for quaternary diagram plotting in python based on Matplotlib.
Can be installed by pip at https://pypi.org/project/python-quaternary/.
Please see example files for an example case of how to use it.
<div style="text-align:center">
<img src="/readme_images/ex1.png" width="800" height="600"/>
</div>
## Installation
###pip
```bash
pip install python-quaternary
```
## Useage
Please see examples in the examples folder fore detailed examples.
First you need to import it with
```python
from quaternary import quaternary
```
Then, you need to create a matplotlib figure and create the quaternary object
```python
fig = plt.figure()
quat = quaternary(fig)
```
After that, you can set the grid and labels on each corner
```python
quat.set_grid()
quat.set_label1('C$_1$')
quat.set_label2('C$_4$')
quat.set_label3('C$_{10}$')
quat.set_label4('CO$_2$',pad=0.05)
```

Some day I may write actual documentation for this library depending on if anyone finds it useful...

## Citation
If you want to cite it, open the file CITATION.md.
