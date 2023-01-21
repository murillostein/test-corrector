# UFSC test corrector and report generator
## The challenge
This is a project developed during my experience at [Einstein Floripa](https://einsteinfloripa.com.br/). I had the mission to automatize the correction of the UFSC (Federal University of Santa Catarina) entrance exam, which was initially made by hand, but, with the increase in the total of students, it was impracticable to keep on this way.
So, I developed this code that can correct the tests and generate an [interactive report] on Streamlit platform.

UFSC's entrance exam includes 3 tests.
- A summation-type test, that the score achieved on each question is determined by the rule:
> If CPS > ICS, then: 
$S = \frac{(TP - (TCP - (CPS - ICS))}{TP}$

where:

><p> S - student score<br>
> TP - total alternatives<br>
> TCP - total of correct alternatives<br>
> CPS - total of correct alternatives considered correct  by the student<br>
  > IPS - total of incorrect alternatives considered correct by the student</p>
- A writing test where the student writes an essay;
- A discursive test, where the student answers discursive questions.

## The solution
It utilizes the Pandas' package to do all the data manipulation processes.
Then, the manipulated data is input into the Streamlit app to visualize with Plotly charts.
- `corrector`: main file to correct the tests
- `app_main`: main page to deploy the app on streamlit.share

## Author

- [Murillo Stein](https://www.linkedin.com/in/murillo-stein/)