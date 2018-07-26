# OSS117 - Open source scrapper for Inteligence ... 
(c'mon, we'll find a better acronym later)

<img src="https://img.static-smb.be/a/view/q75/w720/h480/2090887/e6c6eddf-3a56-4115-90fd-9d18764c912e-gif.gif" alt="looking for intel"/>

OSS117 is a tool designed to craft intelligence based on open sources data.
It can be used by:
- Red-teams during their recon phase to prepare their engagement (identify VIP, craft username wordlists, etc.)
- Blue-teams to get a picture of your organisation footprint / What intell we concede to a potential adversary


The project is built around 3 modules types:
- COLLECTORS: which gathers data though multiples sources
- INFERORS: which finds new pieces of data using the data we got
- EVALUATORS: which evaluates the data we have

Using those modules you can craft the scenarios you want. For instance for a given organization

1. COLLECTORS - Collect all employees (name + job + location) using Linkedin. 
2. INFERORS + EVALUATOR - Derivate their mails using classical templates (fistname.lastname@orgname.tld, etc.)
and email checker API (deliverability, reputation, etc.)
3. EVALUATOR - Check if one mail appears in haveIbeenPwned

---- Scenario#2 ----
1. COLLECTORS - Collect all employees information using Linkedin (name + job + location + interest). 
2. INFERORS - Derivate username/password wordlists using the data collected (name, location, interest, etc.)

---- Scenario#3 ----
1. COLLECTORS - Collect employees name, interest
2. INFEREROS - Try to identificate employee's account using checkusernames / namechk, etc.


and so on...


Here's a <a href="https://www.youtube.com/watch?v=elhEocatrdM"> basic POC </a> I've made. 
Notice that the scrap speed is configurable but is deliberately slow to avoid to be busted by Google and Linkedin 



These are the very first steps for this project, if you have any idea of modules, scenarios, feel free to contact me at tahar.bennacef.farewell@gmail.com
