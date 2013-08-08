Quest
=====

Knowledge Search Engine

## Steps for installing the required software/libraries:
1) Install the latest version of MongoDB from http://www.mongodb.org/downloads

2) Install Beanstalkd from http://kr.github.io/beanstalkd/download.html

3) Start MongoDB by setting up the required database paths.

4) Start Beanstalk daemon.

5) Install Pip for installing Python packages.

6) Install all the required Python libraries by running the following (point to the downloaded requirements.txt):

$ pip install -U -r requirements.txt


## Running the search engine:
1) Go to the web folder and run

$ python root.py

2) Point the browser to http://localhost:8080/

3) In the search text box, type a query and choose one of the suggestions and click the magnifying glass button.

## Running the extractor:
1) Go to the lib folder and run

$ python extractor.py


## Contributors
- Sushant Bhadkamkar
- Prasad Kapde
- Ashwath Pratap Singh

## License

The MIT License (MIT)
Copyright (c) 2013 Sushant Bhadkamkar, Prasad Kapde, Ashwath Pratap Singh

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
