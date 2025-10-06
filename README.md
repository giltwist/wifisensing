**Statement of the Problem:**

It is exceedingly helpful in many applications to have some sense of what is going on in the immediate surroundings of a smart device. For example, beginning a wake-up procedure that takes several seconds as a user is approaching the device rather than waiting for the user to press a button. Advanced methods such as computer vision are expensive both in hardware and computationally. Dedicated hardware, such as ultrasonic or infrared rangefinders are more economical, but may ultimately be inviable due to size, cost, or complexity restraints. Any internet-enabled smart device is likely to have wifi already included in the hardware, thus utilizing this hardware in novel ways to solve this core problem may be prudent.

**The tech in a nutshell:**

Human bodies absorb a variety of electromagnetic frequencies very well. If a person walks between a wifi router and a smart device, their body will cast a “shadow” that may be measurable in the Received Signal Strength Indicator (often in db) at a magnitude several times the ambient variation of the signal.

**About this Repo**

At this point, my explorations are still strongly tied to the specific hardware on which they run, so these folders contains the snippets of the code that would potentially be reusable by others.  For example, nobody else is going to have the little RGB smart lamp I made for a class, but they might very well have a Raspberry Pi 3B+.  So, the actual meaningful wifi sensing code for that hardware gets a folder, but I've stripped out a lot of the connected code for, say, controlling the color of the lamp.

**More Reading**

* Schäfer, J., Barrsiwal, B. R., Kokhkharova, M., Adil, H., & Liebehenschel, J. (2021). Human Activity Recognition Using CSI Information with Nexmon. _Applied Sciences_, _11_(19), 8860. _<https://doi.org/10.3390/app11198860>_

* Yang, J., Chen, X., Zou, H., Lu, C. X., Wang, D., Sun, S., & Xie, L. (2023). SenseFi: A library and benchmark on deep-learning-empowered wifi human sensing. _Patterns_, _4_(3), 100703. _<https://doi.org/10.1016/j.patter.2023.100703>_


