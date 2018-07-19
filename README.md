# OSS117 - Open source scrapper for Inteligence ... 
(c'mon, we'll find a better acronym later)

<img src="https://img.static-smb.be/a/view/q75/w720/h480/2090887/e6c6eddf-3a56-4115-90fd-9d18764c912e-gif.gif" alt="looking for intel"/>

OSS117 is a tool to craft intelligence based on opensources data.
It can be used by:
- Red-teams during their recon phase to prepare their engagement (identify VIP, craft username wordlists, etc.)
- Blue-teams to see what information their organization concede to a potential adversary / be aware of their organisation footprint


The project is built around 3 modules types:
- COLLECTORS: which are designed to gather data though multiples sources
- INFERORS: which are designed to find new pieces of data using the data we got
- EVALUATORS: which are designed to evaluate the data we have


Using those modules you can craft the scenarios you want. For instance for a given organization

---- Scenario#1 ----
1. COLLECTORS - Collect all employees (name + job + location) using Linkedin. 
2. INFERORS + EVALUATOR - Derivate their mails using classical templates (fistname.lastname@orgname.tld, etc.)
and email checker API (deliverability, reputation, etc.)
3. EVALUATOR - Check if one mail appears in haveIbeenPwned

---- Scenario#2 ----
1. COLLECTORS - Collect all employees (name + job + location + interest) using Linkedin. 
2. INFERORS - Derivate username/password wordlists using the data collected (name, location, interest, etc.)

and so on...


This is the very first steps for this project, if you have any idea feel free to contact me at tahar.bennacef.farewell@gmail.com
