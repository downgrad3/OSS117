# OSS117 - Open source scrapper for Intelligence ... 
(c'mon, we'll find a better acronym later)

<img src="https://img.static-smb.be/a/view/q75/w720/h480/2090887/e6c6eddf-3a56-4115-90fd-9d18764c912e-gif.gif" alt="looking for intel"/>

OSS117 is a tool designed to craft intelligence based on open sources data.
It can be used by:
- Red-teams during their recon phase to prepare their engagement (identify VIP, craft username wordlists, gather people interest for SE scenarios, etc.)
- Blue-teams to have a picture about their organisation fingerprint in the wild (ie: information avalaible for a potential adversary)

The project is built around 3 modules types:
- COLLECTORS: which gathers data though multiples sources
- INFERORS: which finds new pieces of data using the data we got
- EVALUATORS: which evaluates the data we have

Using those modules you can craft the scenarios you want. For instance for a given organization
1. COLLECTORS - Collect all employees (name + job + location) using Linkedin. 
2. INFERORS + EVALUATOR - Derivate their mails using classical templates (fistname.lastname@orgname.tld, etc.)
and email checker API (deliverability, reputation, etc.)
3. EVALUATOR - Check if one mail appears in haveIbeenPwned


1. COLLECTORS - Collect all employees (name + job + location + interest) using Linkedin. 
2. INFERORS - Derivate username/password wordlists using the data collected

and so on...


Here's a <a href="https://www.youtube.com/watch?v=elhEocatrdM"> basic POC </a> I've made. 
Notice that the scrap speed is configurable but is deliberately slow to get busted by Google and Linkedin 



These are the very first steps for this project, if you have any idea of modules, scenarios, feel free to contact me at tahar.bennacef.farewell@gmail.com
