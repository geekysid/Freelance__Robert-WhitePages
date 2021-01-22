
<p align="center">
    <img src="https://user-images.githubusercontent.com/59141234/93002341-ff261d00-f553-11ea-874d-19ab5cb1068f.png" height="70px" />
</p>
<h4 align="center">
    WhitePages Residential Directory Scraper
</h4>
<p align="center">
    Scraper to fetch details of perople in WhitePages directory
    <br />
    <a href="https://www.upwork.com/ab/f/contracts/25542018">
        Project Contract
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Client - Robert
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Status - Completed
    </a>
</p>

<br />

<!-- Details of Content -->
## Table of contents

 * [Prerequisite](#Prerequisite)
 * [Unpacking](#Unpacking)
 * [Installation Dependencies](#Installation-Dependencies)
 * [Understanding Project File](#Understanding-Project-File)
 * [Running The Script](#Running-The-Script)
 * [Show Your Support](#Show-Your-Support)
 * [Contact Me](#Contact-Me)

<br />

<!-- Prerequisite -->
## Prerequisite
    - Windows
    - Python 3.6 or above 
    - Chrome Webdriver

[Install Python on Windows 10](https://phoenixnap.com/kb/how-to-install-python-3-windows)

[Get Chrome WebDriver according to your Google Chrome Version](https://chromedriver.chromium.org/downloads)

<br />

<!-- Unpacking -->
## Unpacking
 - Unzip the WhitePages_Scrapper.zip in desired location. Let's assume that we unzip the file in location *E:\WhitePages*
 - After this the path of the Project lookes like *E:\WhitePages*
 - The project folder should look something like this:

 ![whitepages](https://user-images.githubusercontent.com/59141234/104126126-ddf9ff80-5380-11eb-808d-e86f30cc4d6b.png)


<!-- Instalation -->
## Installation Dependencies
 - Start terminal and type below command in terminal to point to the project folder:

 ```
 ~$ E:\
 ~$ cd WhitePages
 ```

 - Now we need to download all the dependencies required to run the script. For this we will type below command in terminal:

 ```
 ~$ pip3 install -r requirements.txt
 ```

<br />

<!-- Understanding File -->
## Understanding Project File

#### Requirement.txt ⛔
This file contains all the dependencies that we need to install on our system. You can delete this file but its Ok to keep it there and forget that it exists.

#### Script.py 🚫
This file is the main script that we need to run to get the desired output. **Please never touch this file**.

#### requirements.txt 🚫
This file contains all the inportant modules required to execute the script. **Please never touch this file**.

#### config.json ✍️
This file needs to be edited everytime you run the script and so it needs some explation...

 - **path_to_chromedriver** => Path where the chrome webdriver executeable file is located. Take care of the *Double Black Slash*.

 - **path_to_input_file** => Path where the input csv file is located. Take care of the *Double Black Slash*.
 - **path_to_output_file** =>  Path where the output csv file is to be saved. Take care of the *Double Black Slash*.

#### xyz.csv ✍️
This is the input file. You can place this file anywhere as long as you mention the correct path of this file in config.json. The name of the input file can be anything. This file is only for sample purpose.

#### xyz-output.csv ✍️
This is the output file. This file will be saved to the location mentioned in the config.json. The name of the input file can be anything. This file is only for sample purpose.

<br />

<!-- Running the script -->
## Running The Script
 So before running the script please make sure of two things:

 - You have edited the config file properly.
 - The pointer in terminal is pointing to the project forlder. If not then use below code:

 ```
 ~$ E:\
 ~$ cd Whitepages
 ```

Now we need to enter below code to execute the script.

```
~$ python3 script.py
```

Now just grab yourself a pint of 🍺 and let the script do its task.

<br />

<!-- Asking for Supports -->
## Show Your Support
If you are happy with my work then please give me :star::star::star::star::star: rating and also leave really nice recommendation/feedback on upwork. This will help me a lot in getting more project. A small and happy bonus is always appreciated 🤩. Also kindly rememeber me if you have any such project or any scraping projects. <p />Thank You for giving me opportunity to work on this project.


<br />

<!-- Displaying message about me -->
## Contact Me

**Siddhant Shah** - Please feel free to connect to me in case there is any issue in the script or any changes are required. You can contact on below mentioned connects

> [Website](https://gist.github.com/siddhantshah1986 "My Website")
&emsp;&emsp;
[Mail Me](mailto:siddhant.shah.1986@gmail.com "siddhant.shah.1986@gmail.com")
&emsp;&emsp;
[UpWork](https://www.upwork.com/fl/geekysid "Upwork")
&emsp;&emsp;
[Instagram](https://www.instagram.com/siddhantshah39 "Instagram")
&emsp;&emsp;
[WhatsApp](https://api.whatsapp.com/send?phone=+918584852091 "WhatsApp")
