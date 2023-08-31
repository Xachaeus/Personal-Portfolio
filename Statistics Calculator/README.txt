This project was a program with useful statistics functions built into it for
the statistics class I taught in my senior year of high school. At my high
school, everyone was required to have a chromebook, so I compiled the project
into a debian package that could be installed natively onto a chromebook.
Unfortunately, due to significant damage to the hard drive that the source code 
was stored on,the only remnant of the project is the compiled debian binary 
package, which can only be installed on compatable machines. Due to the
large size of the package (about 125MB), the binary package cannot be uploaded
to Github, but can be downloaded from Google Drive here: 
https://drive.google.com/file/d/10cgSt3hTeiXLBCnUqJjDzuh_9hanO9f2/view?usp=sharing

The software utilizes linear, quadratic, and exponential regression software
from the numpy, scipy, matplotlib, and sklearn libraries. The software allows
users to either choose a specific regression model and enter the data, or just
enter the data and find the model with the lowest correlation coefficient.
Whichever option the user chooses, the software will provide both the exact
function which was yielded by the regression algorithm, and a graph which
illustrates both the input data and the regressed function, as well as
providing the correlation coefficient. The graph that the software produces
can be resized and exported to an image format, for ease of use in an education
environment.
