# Ph-UI!!!

**NAMES OF COLLABORATORS HERE**
**COLLABORATORS:** [William Reid (NetID: wjr83)](https://github.com/wjr83/Interactive-Lab-Hub/edit/Fall2023/Lab%204/README.md)

For lab this week, we focus both on sensing, to bring in new modes of input into your devices, as well as prototyping the physical look and feel of the device. You will think about the physical form the device needs to perform the sensing as well as present the display or feedback about what was sensed. 

## Part 1 Lab Preparation

### Get the latest content:
As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:


Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the personal access token for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab4 content"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

Option 3: (preferred) use the Github.com interface to update the changes.

### Start brainstorming ideas by reading: 
* [What do prototypes prototype?](https://www.semanticscholar.org/paper/What-do-Prototypes-Prototype-Houde-Hill/30bc6125fab9d9b2d5854223aeea7900a218f149)
* [Paper prototyping](https://www.uxpin.com/studio/blog/paper-prototyping-the-practical-beginners-guide/) is used by UX designers to quickly develop interface ideas and run them by people before any programming occurs. 
* [Cardboard prototypes](https://www.youtube.com/watch?v=k_9Q-KDSb9o) help interactive product designers to work through additional issues, like how big something should be, how it could be carried, where it would sit. 
* [Tips to Cut, Fold, Mold and Papier-Mache Cardboard](https://makezine.com/2016/04/21/working-with-cardboard-tips-cut-fold-mold-papier-mache/) from Make Magazine.
* [Surprisingly complicated forms](https://www.pinterest.com/pin/50032245843343100/) can be built with paper, cardstock or cardboard.  The most advanced and challenging prototypes to prototype with paper are [cardboard mechanisms](https://www.pinterest.com/helgangchin/paper-mechanisms/) which move and change. 
* [Dyson Vacuum Cardboard Prototypes](http://media.dyson.com/downloads/JDF/JDF_Prim_poster05.pdf)
<p align="center"><img src="https://dysonthedesigner.weebly.com/uploads/2/6/3/9/26392736/427342_orig.jpg"  width="200" > </p>

### Gathering materials for this lab:

* Cardboard (start collecting those shipping boxes!)
* Found objects and materials--like bananas and twigs.
* Cutting board
* Cutting tools
* Markers
* New hardware for your kit will be handed out. Update your parts list. 

(We do offer shared cutting board, cutting tools, and markers on the class cart during the lab, so do not worry if you don't have them!)

## Deliverables \& Submission for Lab 4

The deliverables for this lab are, writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do.
* "Acts like": shows how a person would interact with the device.

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, into your lab 4 repository, and link them in your lab 4 readme.md.
* Link your Lab 4 readme.md in your main Interactive-Lab-Hub readme.md. 
* Group members can turn in one repository, but make sure your Hub readme.md links to the shared repository.
* Labs are due on Mondays, make sure to submit your Lab 4 readme.md to Canvas.


## Lab Overview

A) [Capacitive Sensing](#part-a)

B) [OLED screen](#part-b) 

C) [Paper Display](#part-c)

D) [Materiality](#part-d)

E) [Servo Control](#part-e)

F) [Camera Test](#part-f)

G) [Record the interaction](#part-g)

## The Report (Part 1: A-D, Part 2: E-F)

### Part A
### Capacitive Sensing, a.k.a. Human-Twizzler Interaction 

We want to introduce you to the [capacitive sensor](https://learn.adafruit.com/adafruit-mpr121-gator) in your kit. It's one of the most flexible input devices we are able to provide. At boot, it measures the capacitance on each of the 12 contacts. Whenever that capacitance changes, it considers it a user touch. You can attach any conductive material. In your kit, you have copper tape that will work well, but don't limit yourself! In the example below, we use Twizzlers--you should pick your own objects.


<p float="left">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150" />
</p>

Plug in the capacitive sensor board with the QWIIC connector. Connect your Twizzlers with either the copper tape or the alligator clips (the clips work better). Install the latest requirements from your working virtual environment:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ pip install -r requirements.txt
```

<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" width=400>
These Twizzlers are connected to pads 6 and 10. When you run the code and touch a Twizzler, the terminal will print out the following

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python cap_test.py 
Twizzler 10 touched!
Twizzler 6 touched!
```

### Part B
### More sensors

#### Light/Proximity/Gesture sensor (APDS-9960)

We here want you to get to know this awesome sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595). It is capable of sensing proximity, light (also RGB), and gesture! 

<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector and try running the three example scripts individually to see what the sensor is capable of doing!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python proximity_test.py
...
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python gesture_test.py
...
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python color_test.py
...
```

You can go the the [Adafruit GitHub Page](https://github.com/adafruit/Adafruit_CircuitPython_APDS9960) to see more examples for this sensor!

#### Rotary Encoder (optional)

> **_NOTE:_**  Not in the kit yet - skip this.

A rotary encoder is an electro-mechanical device that converts the angular position to analog or digital output signals. The [Adafruit rotary encoder](https://www.adafruit.com/product/4991#technical-details) we ordered for you came with separate breakout board and encoder itself, that is, they will need to be soldered if you have not yet done so! We will be bringing the soldering station to the lab class for you to use, also, you can go to the MakerLAB to do the soldering off-class. Here is some [guidance on soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering/preparation) from Adafruit. When you first solder, get someone who has done it before (ideally in the MakerLAB environment). It is a good idea to review this material beforehand so you know what to look at.

<p float="left">
<img src="https://cdn-shop.adafruit.com/970x728/377-02.jpg" height="200" />
<img src="https://cdn-shop.adafruit.com/970x728/4991-09.jpg" height="200">
</p>

Connect it to your pi with Qwiic connector and try running the example script, it comes with an additional button which might be useful for your design!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python encoder_test.py
```

You can go to the [Adafruit Learn Page](https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython) to learn more about the sensor! The sensor actually comes with an LED (neo pixel): Can you try lighting it up? 

#### Joystick (optional)

A [joystick](https://www.sparkfun.com/products/15168) can be used to sense and report the input of the stick for it pivoting angle or direction. It also comes with a button input!

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/5/8/15168-SparkFun_Qwiic_Joystick-01.jpg" height="200" />
</p>

Connect it to your pi with Qwiic connector and try running the example script to see what it can do!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python joystick_test.py
```

You can go to the [SparkFun GitHub Page](https://github.com/sparkfun/Qwiic_Joystick_Py) to learn more about the sensor!

#### Distance Sensor

Earlier we have asked you to play with the proximity sensor, which is able to sense objects within a short distance. Here, we offer [Sparkfun Proximity Sensor Breakout](https://www.sparkfun.com/products/15177), With the ability to detect objects up to 20cm away.

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/9/2/15177-SparkFun_Proximity_Sensor_Breakout_-_20cm__VCNL4040__Qwiic_-01.jpg" height="200" />
</p>

Connect it to your pi with Qwiic connector and try running the example script to see how it works!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python qwiic_distance.py
```

You can go to the [SparkFun GitHub Page](https://github.com/sparkfun/Qwiic_Proximity_Py) to learn more about the sensor and see other examples!

### Part C
### Physical considerations for sensing

Usually, sensors need to be positioned in specific locations or orientations to make them useful for their application. Now that you've tried a bunch of the sensors, pick one that you would like to use, and an application where you use the output of that sensor for an interaction. For example, you can use a distance sensor to measure someone's height if you position it overhead and get them to stand under it.

**\*\*\*Draw 5 sketches of different ways you might use your sensor, and how the larger device needs to be shaped in order to make the sensor useful.\*\*\***

9 total ideas are described below. Sketches were drawn for 5 of the ideas whose primary sensor was the capacitive sensor.


1.	**Musical painting** (main sensor: Capacitive Touch Sensor) 
>* A canvas will be painted to create an interactive painting experience whereby touching specific parts of the canvas results in sounds being played through the camera’s speaker (these sounds are mapped using the capacitive touch sensor). 

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/50c35851-a878-4b36-814a-a30e1dc6186a)

2.	**A Halloween Display** (main sensor: OLED Screen)
>*  For example, a display of different scary exhibits on the OLED screen such as:
>>* Pet the spider and its legs fly at the user in doing so
>>* A pumpkin that laughs at the user if he/she presses green LED button or scares if the user presses the red LED button
3.	**Garage Band or Guitar Hero type musical game** (main sensor: Capacitive Touch Sensor) 
>* There are four or more colored objects the user has to touch or step on (barefoot for conductivity to work with the capacitive touch sensor). The user is told which items to touch on the OLED screen (the color of object is displayed) and for how long.

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/f9dd17cd-1f0b-476e-b7ad-bf1d27efe098)

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/79f72f06-ee2a-4c22-8ded-8c48b13d1e25)


4.	**Game: Twister Box!** (main sensor: Capacitive Touch Sensor) 
>* Raspberry Pi sits inside a box with conductive stickers (or perhaps the entire side of the box is conductive, each side mapping to some feature or action). The OLED screen tells the user which color to touch (the color of object is displayed) and for how long. The objective of the game is to touch all the colors prompted by the computer in the least amount of time possible. The device will keep a record of high scores. The ID for the high scores can be inputted with the keypad (date of birth), a button to enable speech recognition to convert a name spoken to the name of the player, and an actual keyboard to input the player’s name. 

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/d605edaa-1b5b-4ee4-9988-4dfeb17596f3)

5.	**Game: Color Mixing!** (main sensor: Capacitive Touch Sensor) 
>* A variation of the game above (perhaps a more challenging approach) would be to press the two colors (using the subtractive color model) that when mixed (e.g., such as when mixing paint) make the color displayed on the screen. This would be a fun game to teach young kids the basics of color theory for an introductory art class.
> <p align="center"><img src="https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/2cef0175-3a23-4445-aa98-fb090ffa0d6a"  width="500" > </p>
> <p align="center"><img src="https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/00938d5a-15cc-4ff7-9e00-7283e87d5308"  width="500" > </p>

6.	**A Piano with 12 Keys** (main sensor: Capacitive Touch Sensor) 
>* Have the functionality to record the music generated (using the green or red button to start and stop the recording through the camera’s microphone). The OLED screen can display the notes to play (if practicing a specific song). Note: This would be most feasible for four-chord songs. 

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/cddfda53-8e0a-4d02-822f-9a68f4dcd4ed)

7.	**Game: Crack the Cipher to Unlock the Box!** (main sensor: Capacitive Touch Sensor, green and red LED buttons) 
>* The player must solve a series of puzzles in order to progress to the next level. The puzzles will range from easy to hard, and they will increase in difficulty the higher the level reached. A broad range of skills will be utilized in solving these puzzles, including technology, math, music, science, language, history, current news, etc. The OLED screen will provide the riddle to solve. Hints will be provided (a maximum of 3 hints per level). The inspiration for this game came from the Escape Room team-building game.
8.	**Math Speed Game:** (main sensor: Capacitive Touch Sensor) 
>*  Prompts are shown on the OLED Screen (multiplication, division, square root, exponents, binary numbers that need a decimal conversion, etc.) one at a time and the user needs to provide the answer through a keypad (which could be a lead-drawn keypad or object-inspired keypad using the capacitive touch sensor). 
>* The prompts would be random. This means that a random number (or two random numbers depending on the operation) would be generated and fed through a function to solve and check the answer provided by the player. 
>* The game will display a countdown (2 minutes) on the OLED screen (or miniPiTFT screen).
>* The objective of the game is to solve as many of the mathematical expressions as possible before the countdown reaches zero. 

![image](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/40730086-216b-4156-922c-8e07ffb1a421)


9.	**Hoops on the Pi** (main sensors: Light/Proximity/Gesture sensor and Distance Sensor, coupled with speakers, and green and red LED buttons) 
>*  Use the distance sensor and proximity sensor to detect if an object (ball) has made it through the basket/hoop. 
>>*  This avoids us having to be connected to the ball (e.g., through a conductive string) as would be the case if this were being done with the capacitive touch sensor.
>* Multiplayer game (maximum of two players, unless Khushi and William can combine their sensors on the same bus – then it is a maximum of four players assuming we can differentiate between two identical sensors on the bus).
>
>* **Version A of the Hoops Game:**
>>*  Players take turns shooting at the same basket to play the game H-O-R-S-E. 
>>>*  H-O-R-S-E is a game played by two people on a basketball court. The idea of the game involves matching baskets. The player who makes shots that the opponent does not duplicate wins the game. Example: The second person shooting must duplicate the first-person's shot if it is made. If the second shooter misses, he/she receives the letter "H". If the first person's shot is missed, the second shooter may attempt any shot. If his/her shot is made, the opponent is obligated to duplicate it. Each time a shooter misses a shot that he/she attempted to duplicate, a letter is "awarded". The game continues until one person accumulates 5 letters or H-O-R-S-E.
>>*  The user tells the computer which player is throwing at any given time by pressing the green LED button (i.e., Player #1) or the red LED button (i.e., Player #2).
>>*  This version of the game is not timed. 
>*  **Version B of the Hoops Game:**
>>*  At the beginning of the game, one player will input the duration of their game (for the countdown that will be displayed).
>>*  Two players face each other on opposite sides of a tall, thin box where each of the two sides has its own basket/hoop. Alternatively, each player can face a cardboard wall that has two hoops positioned at the same height but with a horizontal distance between each other. The OLED screen will keep track of the number of points made by each player (or team, if two pairs are shooting into the same basket). 
>>>*  Or four players each face a side of a box, where each box has its own basket/hoop. Note: this is only possible if Khushi and I can combine both our Gesture Sensors and Distance Sensors on the same bus. This game can also be played with teams of two competing for a joint high score.
>>* Points will be displayed to each user player on the OLED screen.
>>*The miniPiTFT screen will display a timer/countdown. The objective of the game is to score as many baskets as possible before the timer runs out. 
>* The camera’s speaker can be used to make a sound every time a basket/hoop is made. 
>>* Note: the basket/hoop would be shaped as a cone (so that it’s easier to make a basket) with an open top and bottom to allow the ping-pong ball to fall through.
>>* Current Idea: The sensor would be positioned flush with the bottom of the conical basket (needs to be tested).
>* The speaker will also indicate which player won.
>*	The game can be played with ping-pong balls (ideally), aluminum foil balls, paper balls, or any other object that fits through the cardboard hoop and won’t damage the structural components.

**\*\*\*What are some things these sketches raise as questions? What do you need to physically prototype to understand how to answer those questions?\*\*\***
* How big should the interactive device be? How portable should the interactive device be?
* Where should the sensors and Raspberry Pi be stored such that these are not visible to the user?
>* How will the Raspberry Pi be powered hidden in this context?
* Where should the screen be positioned?
* Where should the buttons be positioned?
* Is any insulation needed to ensure connections to the capacitive sensor don't touch other connections by mistake?
* How should the circuitry to the capacitive sensor be designed so as to minimize real estate and materials used?
* Which colors should be used for what task?
* How should the information on the small display be designed such that it maximizes readability?
* How fun or amusing will users find these interactive devices? How long will they want to play for?


**\*\*\*Pick one of these designs to prototype.\*\*\***
1.	**Musical painting** was chosen for Part 1 of Lab 4.

### Part D
### Physical considerations for displaying information and housing parts

Here is a Pi with a paper faceplate on it to turn it into a display interface:

<img src="https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2020Fall/images/paper_if.png?raw=true"  width="250"/>


This is fine, but the mounting of the display constrains the display location and orientation a lot. Also, it really only works for applications where people can come and stand over the Pi, or where you can mount the Pi to the wall.

Here is another prototype for a paper display:

<img src="https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2020Fall/images/b_box.png?raw=true"  width="250"/>

Your kit includes these [SparkFun Qwiic OLED screens](https://www.sparkfun.com/products/17153). These use less power than the MiniTFTs you have mounted on the GPIO pins of the Pi, but, more importantly, they can be more flexibly mounted elsewhere on your physical interface. The way you program this display is almost identical to the way you program a  Pi display. Take a look at `oled_test.py` and some more of the [Adafruit examples](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/master/examples).

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/6/1/3/5/17153-SparkFun_Qwiic_OLED_Display__0.91_in__128x32_-01.jpg" height="200" />
</p>


It holds a Pi and usb power supply, and provides a front stage on which to put writing, graphics, LEDs, buttons or displays.

This design can be made by scoring a long strip of corrugated cardboard of width X, with the following measurements:

| Y height of box <br> <sub><sup>- thickness of cardboard</sup></sub> | Z  depth of box <br><sub><sup>- thickness of cardboard</sup></sub> | Y height of box  | Z  depth of box | H height of faceplate <br><sub><sup>* * * * * (don't make this too short) * * * * *</sup></sub>|
| --- | --- | --- | --- | --- | 

Fold the first flap of the strip so that it sits flush against the back of the face plate, and tape, velcro or hot glue it in place. This will make a H x X interface, with a box of Z x X footprint (which you can adapt to the things you want to put in the box) and a height Y in the back. 

Here is an example:

<img src="https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2020Fall/images/horoscope.png?raw=true"  width="250"/>

Think about how you want to present the information about what your sensor is sensing! Design a paper display for your project that communicates the state of the Pi and a sensor. Ideally you should design it so that you can slide the Pi out to work on the circuit or programming, and then slide it back in and reattach a few wires to be back in operation.
 
**\*\*\*Sketch 5 designs for how you would physically position your display and any buttons or knobs needed to interact with it.\*\*\***

**\*\*\*What are some things these sketches raise as questions? What do you need to physically prototype to understand how to anwer those questions?\*\*\***

**\*\*\*Pick one of these display designs to integrate into your prototype.\*\*\***

**\*\*\*Explain the rationale for the design.\*\*\*** (e.g. Does it need to be a certain size or form or need to be able to be seen from a certain distance?)

Build a cardboard prototype of your design.

**\*\*\*Document your rough prototype.\*\*\***


LAB PART 2

### Part 2

Following exploration and reflection from Part 1, complete the "looks like," "works like" and "acts like" prototypes for your design, reiterated below.

### Part E (Optional)
### Servo Control with Joystick
> **_NOTE:_**  Not in the kit yet.

In the class kit, you should be able to find the [Qwiic Servo Controller](https://www.sparkfun.com/products/16773) and [Micro Servo Motor SG51](https://www.adafruit.com/product/2201). The Qwiic Servo Controller will need external power supply to drive, which is included in your kit. Connect the servo controller to the miniPiTFT through qwiic connector and connect the external battery to the 2-Pin JST port (ower port) on the servo controller. Connect your servo to channel 2 on the controller, make sure the brown is connected to GND and orange is connected to PWM.

<img src="Servo_Setup.jpg" width="400"/>

In this exercise, we will be using the nice [ServoKit library](https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython) developed by Adafruit! We will continue to use the `circuitpython` virtual environment we created. Activate the virtual environment and make sure to install the latest required libraries by running:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ pip3 install -r requirements.txt
```

A servo motor is a rotary actuator or linear actuator that allows for precise control of angular or linear position. The position of a servo motor is set by the width of an electrical pulse, that is, we can use PWM (pulse-width modulation) to set and control the servo motor position. You can read [this](https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors/servo-motors) to learn a bit more about how exactly a servo motor works.

Now that you have a basic idea of what a servo motor is, look into the script `servo_test.py` we provide. In line 14, you should see that we have set up the min_pulse and max_pulse corresponding to the servo turning 0 - 180 degrees. Try running the servo example code now and see what happens:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python servo_test.py
```

It is also possible to control the servo using the sensors mentioned in as in part A and part B, and/or from some of the buttons or parts included in your kit, the simplest way might be to chain Qwiic buttons to the other end of the Qwiic OLED. Like this:

<p align="center"> <img src="chaining.png"  width="200" ></p>

You can then call whichever control you like rather than setting a fixed value for the servo. For more information on controlling Qwiic devices, Sparkfun has several python examples, such as [this](https://learn.sparkfun.com/tutorials/qwiic-joystick-hookup-guide/all#python-examples).

We encourage you to try using these controls, **while** paying particular attention to how the interaction changes depending on the position of the controls. For example, if you have your servo rotating a screen (or a piece of cardboard) from one position to another, what changes about the interaction if the control is on the same side of the screen, or the opposite side of the screen? Trying and retrying different configurations generally helps reveal what a design choice changes about the interaction -- _make sure to document what you tried_!

### Part F (Optional)
### Camera
You can use the inputs and outputs from the video camera in the kit. 
We provide another script called camera_test.py to test the USB camera on raspberry pi. 
It uses qt to render a video to the screen, so it is necessary to connect a screen or to connect via VNC to run this script. 

First install some more dependencies into your virtual environment. OpenCV should already be installed on the Pi for the super user. 

```
sudo apt-get install portaudio19-dev python-all-dev
pip install opencv-python pyaudio pygame
```

Once executed the script will render the camera output, press 'q' to stop video and record a sound through the microphone which will be played back by specificing the audio output. 

---
The video is rendered locally on the pi. For wizarding interactions and prototyping it can be necessary to stream the video to another device such as your laptop. A wizard, observing the user and acting as a computer vision algorithm, can then trigger interactions remotley, such as we did in the tinkerbelle lab.

The following resources are good starts on how to stream video: 
* [OpenCV – Stream video to web browser/HTML page](https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)
* [Live video streaming over network with OpenCV and ImageZMQ](https://pyimagesearch.com/2019/04/15/live-video-streaming-over-network-with-opencv-and-imagezmq/)
### Part G
### Record

Document all the prototypes and iterations you have designed and worked on! Again, deliverables for this lab are writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do
* "Acts like": shows how a person would interact with the device

