# Observant Systems

**COLLABORATORS:**  [Annetta Zheng (NetID: jz2272)](https://github.com/annetta-zheng/Interactive-Lab-Hub/tree/Fall2023/Lab%205),  [William Ried (NetID: wjr83)](https://github.com/wjr83/Interactive-Lab-Hub/tree/Fall2023/Lab%205)


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/-/Lab%202/prep.md#using-vnc-to-see-your-pi-desktop).
2.  Install the dependencies as described in the [prep document](prep.md). 
3.  Read about [OpenCV](https://opencv.org/about/),[Pytorch](https://pytorch.org/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### Pytorch for object recognition

For this first demo, you will be using PyTorch and running a MobileNet v2 classification model in real time (30 fps+) on the CPU. We will be following steps adapted from [this tutorial](https://pytorch.org/tutorials/intermediate/realtime_rpi.html).

![torch](Readme_files/pyt.gif)


To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md).

Make sure your webcam is connected.

You can check the installation by running:

```
python -c "import torch; print(torch.__version__)"
```

If everything is ok, you should be able to start doing object recognition. For this default example, we use [MobileNet_v2](https://arxiv.org/abs/1801.04381). This model is able to perform object recognition for 1000 object classes (check [classes.json](classes.json) to see which ones.

Start detection by running  

```
python infer.py
```

The first 2 inferences will be slower. Now, you can try placing several objects in front of the camera.

Read the `infer.py` script, and get familiar with the code. You can change the video resolution and frames per second (fps). You can also easily use the weights of other pre-trained models. You can see examples of other models [here](https://pytorch.org/tutorials/intermediate/realtime_rpi.html#model-choices). 


### Machine Vision With Other Tools
The following sections describe tools ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)).

#### MediaPipe

A recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Media pipe](Readme_files/mp.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(venv-ml) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(venv-ml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py`. 

Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) is very useful for prototyping with the capabilities of machine learning. We are using [a python package](https://github.com/MeqdadDev/teachable-machine-lite) with tensorflow lite to simplify the deployment process.

![Tachable Machines Pi](Readme_files/tml_pi.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)


```
(venv-tml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tml_example.py
```


Next train your own model. Visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. The raspberry pi 4 is capable to run not just the low resource models. Second, use the webcam on your computer to train a model. *Note: It might be advisable to use the pi webcam in a similar setting you want to deploy it to improve performance.*  For each class try to have over 150 samples, and consider adding a background or default class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate. Finally export your model as a 'Tensorflow lite' model. You will find an '.tflite' file and a 'labels.txt' file. Upload these to your pi (through one of the many ways such as [scp](https://www.raspberrypi.com/documentation/computers/remote-access.html#using-secure-copy), sftp, [vnc](https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#transferring-files-to-and-from-your-raspberry-pi-0-6), or a connected visual studio code remote explorer).
![Teachable Machines Browser](Readme_files/tml_browser.gif)
![Tensorflow Lite Download](Readme_files/tml_download-model.png)

Include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.

#### (Optional) Legacy audio and computer vision observation approaches
In an earlier version of this class students experimented with observing through audio cues. Find the material here:
[Audio_optional/audio.md](Audio_optional/audio.md). 
Teachable machines provides an audio classifier too. If you want to use audio classification this is our suggested method. 

In an earlier version of this class students experimented with foundational computer vision techniques such as face and flow detection. Techniques like these can be sufficient, more performant, and allow non discrete classification. Find the material here:
[CV_optional/cv.md](CV_optional/cv.md).

### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.
* This can be as simple as the boat detector showen in a previous lecture from Nikolas Matelaro.
* Try out different interaction outputs and inputs.

  **I think I want to use the HandPose model for ASL (American Sign Language) hand poses. The model can classify gestures to allow deaf or hard-of-hearing individuals to use ASL with individuals who are not proficient in ASL. Interaction would be first prototyped to work on systems such as Zoom or Google Meet (i.e., video calls).**


**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***


Model Integration: Implement the HandPose model into video call platforms like Zoom or Google Meet, allowing real-time hand gesture recognition during video conversations.

Gesture Classification: Experiment with the model's ability to accurately classify various ASL hand gestures. Ensure it covers a comprehensive set of ASL signs for effective communication.

User-Friendly Interface: Design an intuitive user interface that seamlessly integrates with video call platforms, providing users with easy access to hand gesture recognition features. Consider a minimalistic overlay to avoid distractions.

Compatibility Testing: Conduct extensive testing to ensure the HandPose model works seamlessly across different devices, operating systems, and browsers commonly used for video calls.

User Training: Develop a user-friendly guide or tutorial to educate users on how to use and make the most of the ASL hand gesture recognition feature. Consider incorporating interactive elements for a more engaging learning experience.

Accessibility Features: Explore additional accessibility features, such as visual cues or subtitles, to enhance communication between deaf or hard-of-hearing users and those not proficient in ASL.

Privacy and Security: Implement robust privacy measures to safeguard user data and ensure secure communication. Address any potential concerns related to the storage and processing of video call content.

User Feedback and Iteration: Gather feedback from users, especially from the deaf or hard-of-hearing community, to continuously improve the model's accuracy and the overall user experience. Use an iterative development approach based on user input.

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do? 
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
1. How bad would they be impacted by a miss classification?
1. How could change your interactive system to address this?
1. Are there optimizations you can try to do on your sense-making algorithm.


When does it what it is supposed to do? 
The model performs effectively when presented with clear and well-defined hand gestures commonly used in ASL.

When does it fail?
Failures may occur in low-light conditions, reducing the model's ability to accurately detect and classify hand poses.
Occlusion of hands or rapid, complex gestures may lead to misclassifications or failures.

When it fails, why does it fail?
Lack of lighting impacts the model's ability to identify subtle hand movements and poses.
Occlusion disrupts the visibility of certain parts of the hand, leading to incomplete data for classification.
   
Based on the behavior you have seen, what other scenarios could cause problems?
Variability in hand sizes and shapes may pose challenges, as the model may not generalize well across diverse user demographics.
Background clutter or busy environments may introduce noise, affecting the model's accuracy.



### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

- **What can you use ASL HandPose for?**
  - ASL HandPose can be used for real-time recognition and interpretation of American Sign Language (ASL) hand gestures during video calls.
  - Facilitates communication for deaf or hard-of-hearing individuals, allowing them to express themselves using ASL with those who may not be proficient in the language.

- **What is a good environment for ASL HandPose?**
  - Ideal for video call platforms like Zoom or Google Meet.
  - Works well in well-lit environments to ensure accurate hand gesture recognition.
  - Suited for situations where clear communication through ASL gestures is preferred or necessary.

- **What is a bad environment for ASL HandPose?**
  - Poorly lit environments may hinder accurate hand gesture recognition.
  - Environments with significant visual clutter or distractions may impact the model's ability to interpret gestures accurately.
  - Limited bandwidth or connectivity issues in the network may affect real-time performance.

- **When will ASL HandPose break?**
  - It may break in situations where there is low internet bandwidth, causing delays or interruptions in real-time hand gesture recognition.
  - In scenarios where the user's hands are not clearly visible or are obstructed, the model may struggle to accurately interpret gestures.

- **When it breaks, how will ASL HandPose break?**
  - Breakage may result in misinterpretation or non-recognition of hand gestures, leading to communication gaps.
  - Delays in processing, particularly in low-bandwidth conditions, may cause a lag in the real-time recognition of ASL gestures.

- **What are other properties/behaviors of ASL HandPose?**
  - **Adaptability:** The model should be adaptable to different devices, operating systems, and video call platforms.
  - **Learning Capability:** The ability to improve accuracy over time through machine learning and user feedback.
  - **Privacy Measures:** Implementation of privacy features to ensure secure handling of user data.

- **How does ASL HandPose feel?**
  - **Empowering:** Provides a sense of empowerment to individuals who rely on ASL for communication.
  - **Inclusive:** Fosters inclusivity by bridging communication gaps between those proficient in ASL and those who are not.
  - **Tech-Savvy:** Feels innovative and modern by incorporating cutting-edge technology to enhance communication accessibility.

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***


**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

* I chose to use the Teachable Machines model. 

**Ideas brainstormed for interaction:**

1. ASL (American Sign Language) gesture classification to allow deaf or hard-of-hearing individuals to use ASL with individuals who are not proficient in ASL. Interaction would be first prototyped to work on systems such as Zoom or Google Meet (i.e., video calls).
2. Alert users when a parking spot opens on his/her street. Rationale: street parking in Manhattan is in extremely high demand. The alert could help a user find street parking closer to his/her apartment.
3. System to Recognize Recyclable Objects. 

**The final choice is to implement idea #3: System to Recognize Recyclable Objects**

Making this choice and implementing a system to recognize recyclable objects from non-recyclable objects is motivated by several factors:

> * Environmental Conservation: Effective waste separation and recycling play a crucial role in reducing the environmental impact of waste disposal. It helps conserve resources, reduce energy consumption, and lower greenhouse gas emissions.
> * Waste Reduction: Proper recycling minimizes the volume of waste sent to landfills or incinerators, leading to a reduction in the need for landfill space and decreased pollution from incineration.
> * Consumer Education: Confusion among individuals about the correct sorting of waste is a common issue. This system can serve as an educational tool, clarifying recycling guidelines and encouraging responsible disposal practices.
> * Convenience: Many consumers find it challenging to decipher complex instructions or symbols on bins. A machine learning solution simplifies the process by instantly classifying waste items through images, making it more user-friendly.

**Description of the System:**

The proposed system integrates a camera into trash and recycling bins, providing guidance on which bin to use before disposal. Here's how it will look, feel, and operate: 

#### Look and Feel
- We designed the smart recycling system to be a "trash-eating monster" for awareness-raising for adults and education for kids.
- The smart recycling system itself will feel like a normal trash can, with the exception that the item will not be dropped into a hole but rather placed on a flat surface for a quick classification scan before the user drops the item into the corresponding bin.
  
> - How the smart recycling bin/trashcan looks like:

![main](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/3bf5e727-950b-45b9-8366-4438e0c25807)

> - The setup looks like this:

> ![setup_0](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/d2b87369-ce23-4ff8-8900-40bfc21aace8)
> 
> ![setup_1](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/2c1d5a78-ca52-44c5-81f1-94f89862c0a3)


#### Operate
- The system identifies an object and classifies it as one of the 5 recycled materials (including cardboard, glass, plastic, paper, and metal) or otherwise as trash.

> How it operates:
> 1. Users approach the integrated camera system with their waste items and receive real-time guidance on which bin their waste item belongs to before disposal.
> 2. Then, the smart recycling system successfully identifies the object shown as 1 of the 5 recycled materials the model was trained on (cardboard, glass, plastic, paper, and metal) or as trash.
> > * NOTE: The model was also trained on a background image such that it wouldn't classify an object nor move the servo motor if the background was shown, but as will be seen later, the background training needs to be refined as it sometimes confuses the background with cardboard. 
> 4. After that, the trash can lid will spin to the corresponding trash segment where the user should dispose of the object.
> 5. The user tosses the item he/she no longer needs and leaves.

> Sample recognition for metal: ![rec_sample_metal](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/1889602c-1c89-46ce-862c-1db8aaf5cf63)
> 
> Sample recognition for trash: ![rec_sample_trash](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/e076bb97-54b0-4892-8e29-87481d28ff9d)
>
> Successful Video Demo: (https://drive.google.com/file/d/1avhTgtqcQr5u4EQSTJDn--qpWvSgFQ5v/view?usp=share_link) **Our system successfully identifies and classifies the item into 1 of the 5 recycled materials (including cardboard, glass, plastic, paper, metal) or otherwise as trash.**



**User Interface:**
> A camera is integrated into the trashcan and recycling bin system, making it a seamless part of the waste disposal process in various settings, including businesses, cafes, and outdoor spaces.

> Users approach the integrated camera system with their waste items and receive real-time guidance on which bin their waste item belongs to before disposal.


### Part C
### Test the interaction prototype

## 1. Test for Model #2
Sample Tests Screenshots of System that Recognizes Recyclable Objects (Model #2) in action:
![IMG_4062](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/9032bc7f-e3c9-4f62-bbaa-6cf6d8a511fc)
![IMG_4061](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/bb37b888-9d66-418e-99b0-6472d74871bb)
![IMG_4060](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/6a3b12bc-2208-4383-a02a-3eb88539eb1c)
![IMG_4059](https://github.com/wjr83/Interactive-Lab-Hub/assets/143034234/eb50df40-0e3d-49b4-a0f2-85bd4bd84990)

**Sample Video Interaction / Test:** https://drive.google.com/file/d/1u-p_H_ba_3ORCzK4hywkZke2gTsULy2J/view?usp=sharing


## 2. Tests for Model #3
Sample Tests Videos of System that Recognizes Recyclable Objects (Model #3) in action:

1. Fail test because of the trash can material
(https://drive.google.com/drive/u/2/folders/1qCKEubHjXd1xtYYphaeVq0LjEabTZmkg)

https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/58a06b58-612c-473c-afcc-378bf88f8e21


2. Fail test because of the setup of the servo
   (https://drive.google.com/file/d/1Ys0qppKyxyMv89Qit53MTH5-sW39A0VH/view?usp=share_link) 

https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/6bb87330-8fdd-4634-a26f-1d6f9d7c8555


3. Successful Demo:
Sample recognition for metal: ![rec_sample_metal](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/1889602c-1c89-46ce-862c-1db8aaf5cf63)

Sample recognition for trash: ![rec_sample_trash](https://github.com/annetta-zheng/Interactive-Lab-Hub/assets/67286396/e076bb97-54b0-4892-8e29-87481d28ff9d)

Our system successfully identifies and classifies an object into one of the 5 recycled materials (including cardboard, glass, plastic, paper, and metal) or as trash.

Video Link to Demo: https://drive.google.com/file/d/1avhTgtqcQr5u4EQSTJDn--qpWvSgFQ5v/view?usp=share_link



Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it do what it is supposed to do?
> * The system accurately identifies waste items. The next step in the design of this system would be to guide the user to the correct disposal bin, streamlining the waste sorting process. Thus, users receive clear guidance on which bin to use before disposing of their waste.
1. When does it fail?
> * In cases of poor lighting or obstructed views, it is challenging for the camera to capture clear images of the waste items.
> * When tested on some objects it hasn't seen or different sides of objects it has seen but was not tested on.
> * It also struggles when identifying items with similar appearances that belong in different bins, such as clear plastics and glass, which look alike.
> * In situations where users deposit waste items very quickly, the system may occasionally struggle to keep up, leading to slight delays in providing guidance.
1. When it fails, why does it fail?
> * Poor lighting conditions can affect image quality, leading to misclassifications or a failure to identify the waste item correctly.
> * Obstructed views or partially obscured items may make it difficult for the camera to capture and classify the waste.
> * Similar-looking items may pose a challenge because the system may not have fine-grained classification capabilities to distinguish between them or not enough training data to yield a robust trash vs. recyclables classification model.
> * Rapid user turnover can overwhelm the system's processing capacity, causing it to miss some waste items or provide guidance after the item has been deposited.
1. Based on the behavior you have seen, what other scenarios could cause problems?
> * Language barriers: If the system relies on verbal or text-based instructions to guide users, individuals who do not understand the language used might face difficulties.
> * Age and accessibility issues: Users with visual or hearing impairments might face challenges if the system relies heavily on visual or audio cues without considering accessibility features.
> * Rapid user turnover: In busy public spaces, multiple users deposit waste items in quick succession. The system should be capable of handling high user volumes efficiently without causing bottlenecks or errors.
> * Maintenance issues: The camera and machine learning model require regular maintenance to ensure proper functioning. Neglecting maintenance can lead to performance issues over time.

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
> * Users may not always be fully aware of the uncertainties in the system. They might assume that the system's classifications are always accurate, especially if it doesn't provide clear feedback about its confidence level. 
2. How bad would they be impacted by a miss classification?
> * The impact of misclassification on users can vary. In some cases, misclassifying an item as recyclable when it's not could lead to contamination of recycling streams and added processing costs. Misclassifying an item as non-recyclable when it's recyclable might lead to missed recycling opportunities. For compostable materials, misclassification could affect organic waste diversion rates.
3. How could change your interactive system to address this?
> * To address these concerns, the interactive system could:
> > * Implement a confidence level indicator: The system could provide a confidence score along with its classification. This way, users are aware of how certain or uncertain the system is about its decision.
> > * Offer clear instructions: If an item is challenging to classify, the system could provide guidance to the user, such as suggesting a specific bin but indicating that the user should double-check.
> > * Collect user feedback: Allow users to report misclassifications or provide feedback, which can be used to improve the system's accuracy over time.
4. Are there optimizations you can try to do on your sense-making algorithm?
> * Continuous learning: Implement a self-learning algorithm that can adapt to new objects and user behaviors over time.
> * Real-time model updates: Ensure that the machine learning model is regularly updated with new data to stay current with evolving waste items.
> * Transfer Learning: Utilize transfer learning techniques where the model is initially trained on a broad dataset of waste items and then fine-tuned with specific data from the local environment. This can help the system adapt to local variations in waste categorization.
> * Semantic Segmentation: Employ more advanced computer vision techniques like semantic segmentation to precisely identify regions within an image that correspond to different waste materials. This level of granularity can improve classification accuracy.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

> **Video Link:** https://drive.google.com/file/d/1u-p_H_ba_3ORCzK4hywkZke2gTsULy2J/view?usp=sharing

1. What can you use the recyclable material identification system for?

> * The recyclable material identification system can be used for efficiently identifying and sorting recyclable materials, compostables, and landfill-bound waste, simplifying the waste disposal process.
> * It can serve as an educational tool, raising awareness about responsible waste management and encouraging proper recycling practices.
> * The system can contribute to environmental conservation by promoting recycling, reducing waste, and minimizing landfill usage.

What is a good environment for the recyclable material identification system?

> * The recyclable material identification system thrives in environments with well-lit and clear waste disposal areas, where the camera can capture high-quality images of waste items.
> * It performs well in settings with users who are receptive to using technology for waste sorting and are open to real-time guidance.
> * Collaborative environments where users can provide feedback to enhance the recyclable material identification system's accuracy are ideal.

What is a bad environment for the recyclable material identification system?

> * The recyclable material identification system may not perform well in dimly lit or obstructed areas, as these conditions can hinder the camera's image capture and classification accuracy.
> * Environments with resistance to technology adoption or where users prefer traditional waste sorting methods may not be suitable for the system.
> * Locations with a lack of maintenance or a history of neglecting system upkeep can be problematic for the recyclable material identification system's long-term reliability.

When will the recyclable material identification system break?

> * The recyclable material identification system is susceptible to malfunction or breakdown when exposed to extreme environmental conditions, such as extreme heat, heavy rain, or physical damage.
> * Regular wear and tear, including camera lens contamination and sensor degradation, can contribute to breakdown over time.
> * If the machine learning model used in the recyclable material identification system becomes outdated and no longer receives updates or refinements, it may become less effective.
> * In the event of loss of power or, if solar-powered, weather (rain or snow) preventing optimal charge of the system causing the system to turn off.

When it breaks, how will the recyclable material identification system break?

> * The recyclable material identification system may break by experiencing sensor or camera malfunctions, causing it to fail in accurately identifying waste items.
> * Software breakdowns or system crashes may lead to an inability to provide real-time guidance to users.
> * The system could break gradually, with a decline in accuracy, rather than an abrupt failure, depending on the nature of the issue.

Other properties/behaviors of the recyclable material identification system:

> * The recyclable material identification system continuously learns and improves from user interactions and feedback.
> * It can provide real-time feedback to users, including guidance on which bin to use and potential disposal instructions.
> * The system promotes responsible waste management and environmental sustainability, aligning with the United Nations Sustainable Development Goal 12.

How does the recyclable material identification system feel?

> * The recyclable material identification system offers a user-friendly and efficient waste sorting experience, reducing the complexity of recycling and waste disposal.
> * It can make users feel empowered to contribute to environmental conservation and engage in responsible waste practices.
> * Users might feel confident in using the system, knowing it simplifies their role in sorting waste materials correctly.


Our system successfully identifies and classifies an object as one of the 5 recycled materials (cardboard, glass, plastic, paper, and metal) or otherwise as trash.

> * Successful Demo (Video Link): https://drive.google.com/file/d/1avhTgtqcQr5u4EQSTJDn--qpWvSgFQ5v/view?usp=share_link

**\*\*\*Future Work: Reflection Ideas for Improving on Performance, Design, and Interaction.\*\*\***
> * Increase training dataset. In particular, we need to keep the following in mind as we acquire more data:
> > * Types of objects
> > * Orientation and deformation of objects
> > * Lighting conditions
> > * Add a category for compost
> > * Add a category for toxic waste (e.g., such as batteries)
> > * Could the sound an object makes when squished be used to train a Machine Learning model that exceeds the performance of a computer vision-focused Machine Learning model?
> > * Need to investigate: Are there any sensors that may help identify the structural component of objects (e.g., spectroscopy) that are feasible in this scenario?  
> * The type of trash / recyclable objects will vary drastically depending on the location of the system. We may need to add location-specific data for training for the smart recycling system (e.g., add feedback loop with new sample data collected --> label new data --> retrain classification model with location-specific data --> aggregate new data from all location-specific acquisitions into the model --> release automatic update of the model in the physical smart recycling system). 
> * Simplify Interaction and Design:
> > *  It would be ideal if the user would simply place the object on a flat surface, where the camera would determine the type of object, and once that is confirmed, the servo will spin the trash can lid until the object sits above the bin it corresponds to (e.g., metal). At this point, the item would fall into the bin it corresponds to (perhaps another servo motor would be required to let go of the object through the hole, but not necessarily.
> * Improve the recognition of the background so that the system displays only the count of all types of objects recycled or trashed but does not show a prediction for the background.
> * Add a feature to count the number of items of each type recycled (e.g., using a distance sensor or proximity sensor in a similar fashion as we used in [Lab 4](https://github.com/wjr83/Interactive-Lab-Hub/edit/Fall2023/Lab%204/README.md).
> > * Display these counts to the user by category type in hopes of promoting the mindset: reduce, reuse, recycle.
