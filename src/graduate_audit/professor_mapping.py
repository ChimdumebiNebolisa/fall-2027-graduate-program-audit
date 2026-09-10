from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FacultyCandidate:
    name: str
    themes: str


@dataclass(frozen=True)
class FacultyRoster:
    department: str
    roster_url: str
    alternatives: tuple[FacultyCandidate, ...]


def _c(name: str, themes: str) -> FacultyCandidate:
    return FacultyCandidate(name=name, themes=themes)


# These are bounded current-roster longlists, not retained matches.  The build
# adds the already verified strongest professor from the regional deep review,
# producing five evaluated candidates for every serious Stage 3 program.
FACULTY_ROSTERS: dict[str, FacultyRoster] = {
    "Carnegie Mellon University": FacultyRoster(
        "Software and Societal Systems Department",
        "https://s3d.cmu.edu/people/faculty-index.html",
        (
            _c("Vincent J. Hellendoorn", "AI for software engineering; code models; testing"),
            _c("Ruben Martins", "automated reasoning; program synthesis; software analysis"),
            _c("Christian Kästner", "software engineering; variability; AI-assisted development"),
            _c("İpek Özkaya", "software architecture; technical debt; AI for software engineering"),
        ),
    ),
    "Case Western Reserve University": FacultyRoster(
        "Department of Computer and Data Sciences",
        "https://bulletin.case.edu/engineering/computer-data-sciences/",
        (
            _c("H. Andy Podgurski", "software testing; fault localization; program analysis"),
            _c("Erman Ayday", "security; privacy; trustworthy computing"),
            _c("Vincenzo Liberatore", "software systems; networks; reliability"),
            _c("Gokarna Sharma", "distributed systems; algorithms; dependable computing"),
        ),
    ),
    "George Mason University": FacultyRoster(
        "Department of Computer Science",
        "https://cs.gmu.edu/research/software-engineering",
        (
            _c("Thomas LaToza", "human-centered software engineering; developer tools; debugging"),
            _c("Andrian Marcus", "program comprehension; software evolution; traceability"),
            _c("ThanhVu Nguyen", "program analysis; verification; automated reasoning"),
            _c("David Rosenblum", "software engineering; distributed systems; runtime assurance"),
        ),
    ),
    "Georgia Institute of Technology-Main Campus": FacultyRoster(
        "School of Computer Science",
        "https://www.scs.gatech.edu/people/faculty",
        (
            _c("Mayur Naik", "program analysis; machine learning for code; software reliability"),
            _c("Taesoo Kim", "systems security; vulnerability discovery; operating systems"),
            _c("Milos Prvulovic", "computer security; dependable systems; architecture"),
            _c("Santosh Pande", "compilers; program analysis; secure software systems"),
        ),
    ),
    "Iowa State University": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.iastate.edu/people/faculty",
        (
            _c("Hridesh Rajan", "programming languages; modularity; software engineering"),
            _c("Samik Basu", "formal methods; model checking; software verification"),
            _c("Wei Le", "program analysis; software testing; program repair"),
            _c("Lotfi ben Othmane", "software security; secure development; assurance"),
        ),
    ),
    "North Carolina State University at Raleigh": FacultyRoster(
        "Department of Computer Science",
        "https://www7.csc.ncsu.edu/directories/graduate_faculty.php",
        (
            _c("Laurie Williams", "secure software engineering; testing; software process"),
            _c("Chris Parnin", "developer tools; program comprehension; AI for software engineering"),
            _c("Tim Menzies", "software analytics; defect prediction; empirical software engineering"),
            _c("Munindar P. Singh", "responsible AI; software agents; trustworthy systems"),
        ),
    ),
    "Northeastern University": FacultyRoster(
        "Khoury College of Computer Sciences",
        "https://www.khoury.northeastern.edu/people/",
        (
            _c("Cristina Nita-Rotaru", "systems security; dependable distributed systems"),
            _c("Alina Oprea", "cybersecurity; adversarial machine learning; threat detection"),
            _c("David Choffnes", "network measurement; privacy; dependable systems"),
            _c("Christo Wilson", "security; privacy; algorithmic accountability"),
        ),
    ),
    "Oregon State University": FacultyRoster(
        "School of Electrical Engineering and Computer Science",
        "https://engineering.oregonstate.edu/EECS/research/software-engineering-and-human-computer-interaction",
        (
            _c("Anita Sarma", "collaborative software engineering; developer tools; inclusion"),
            _c("Margaret Burnett", "end-user software engineering; debugging; human factors"),
            _c("Martin Erwig", "programming languages; visual languages; program reasoning"),
            _c("Christopher Hundhausen", "human-centered software development; computing education"),
        ),
    ),
    "Pennsylvania State University-Main Campus": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.eecs.psu.edu/departments/cse-faculty-list.aspx",
        (
            _c("Ting Wang", "trustworthy machine learning; security; privacy"),
            _c("Daniel Kifer", "data privacy; algorithmic fairness; trustworthy data systems"),
            _c("Dongwon Lee", "data provenance; misinformation; trustworthy AI"),
            _c("Mahmut Kandemir", "compilers; software systems; reliability and efficiency"),
        ),
    ),
    "Purdue University-Main Campus": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.purdue.edu/research/software-engineering.html",
        (
            _c("Xiangyu Zhang", "program analysis; debugging; software security"),
            _c("Tianyi Zhang", "AI for software engineering; program repair; testing"),
            _c("Suresh Jagannathan", "programming languages; verification; dependable systems"),
            _c("Antonio Bianchi", "systems security; software analysis; vulnerability detection"),
        ),
    ),
    "Rochester Institute of Technology": FacultyRoster(
        "Golisano College of Computing and Information Sciences",
        "https://www.rit.edu/computing/phd-computing-and-information-sciences/research/software-engineering",
        (
            _c("Daniel Krutz", "software engineering; mobile security; software quality"),
            _c("Christian Newman", "source-code analysis; program transformation"),
            _c("Andy Meneely", "secure software engineering; empirical software engineering"),
            _c("Mohamed Wiem Mkaouer", "software refactoring; repair; search-based software engineering"),
        ),
    ),
    "The University of Texas at Austin": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.utexas.edu/department-info/faculty-roster",
        (
            _c("Calvin Lin", "program analysis; compilers; systems performance"),
            _c("Hovav Shacham", "computer security; software exploitation; systems assurance"),
            _c("Greg Durrett", "natural language processing; trustworthy language models"),
            _c("Keshav Pingali", "programming systems; compilers; parallel software"),
        ),
    ),
    "The University of Texas at Dallas": FacultyRoster(
        "Department of Computer Science",
        "https://cs.utdallas.edu/people/faculty/",
        (
            _c("Kevin Hamlen", "software security; program analysis; malware defense"),
            _c("Lawrence Chung", "software engineering; requirements; architecture"),
            _c("Gopal Gupta", "programming languages; automated reasoning; verification"),
            _c("Latifur Khan", "trustworthy machine learning; data mining; cybersecurity"),
        ),
    ),
    "University of California-Davis": FacultyRoster(
        "Department of Computer Science",
        "https://cs.ucdavis.edu/person-type/faculty",
        (
            _c("Zhendong Su", "program analysis; compiler testing; software reliability"),
            _c("Hao Chen", "software security; mobile systems; vulnerability analysis"),
            _c("Sean Peisert", "computer security; critical infrastructure; risk assessment"),
            _c("Jason Lowe-Power", "computer systems; simulation infrastructure; reproducibility"),
        ),
    ),
    "University of California-Irvine": FacultyRoster(
        "Department of Informatics",
        "https://ics.uci.edu/research-areas/software-engineering-and-systems/",
        (
            _c("Sam Malek", "software architecture; testing; mobile systems"),
            _c("James A. Jones", "software testing; debugging; fault localization"),
            _c("André van der Hoek", "software design; development environments; collaborative engineering"),
            _c("Iftekhar Ahmed", "AI for software engineering; software quality; empirical methods"),
        ),
    ),
    "University of Illinois Urbana-Champaign": FacultyRoster(
        "Siebel School of Computing and Data Science",
        "https://siebelschool.illinois.edu/about/people/all-faculty",
        (
            _c("Darko Marinov", "software testing; program analysis; software reliability"),
            _c("Sasa Misailovic", "programming languages; approximate computing; reliability"),
            _c("Gagandeep Singh", "formal verification; trustworthy AI; program analysis"),
            _c("Tianyin Xu", "systems reliability; configuration errors; cloud systems"),
        ),
    ),
    "University of Maryland-College Park": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.umd.edu/people/faculty",
        (
            _c("Michael Hicks", "programming languages; software security; verification"),
            _c("Michelle Mazurek", "usable security; privacy; empirical security"),
            _c("Marshini Chetty", "usable security; privacy; human-centered systems"),
            _c("Neil Spring", "network measurement; security; dependable systems"),
        ),
    ),
    "University of Massachusetts-Amherst": FacultyRoster(
        "Manning College of Information and Computer Sciences",
        "https://www.cics.umass.edu/about/people",
        (
            _c("Arjun Guha", "programming languages; web security; software systems"),
            _c("Emery Berger", "programming systems; software performance; reliability"),
            _c("Brian Levine", "security; privacy; networked systems"),
            _c("Prashant Shenoy", "distributed systems; cloud computing; dependability"),
        ),
    ),
    "University of Michigan-Ann Arbor": FacultyRoster(
        "Computer Science and Engineering",
        "https://cse.engin.umich.edu/people/faculty/",
        (
            _c("Baris Kasikci", "systems reliability; debugging; program analysis"),
            _c("Satish Narayanasamy", "computer systems; concurrency; debugging"),
            _c("Atul Prakash", "software systems; security; human-centered computing"),
            _c("Peter M. Chen", "dependable systems; virtualization; fault tolerance"),
        ),
    ),
    "University of Nebraska-Lincoln": FacultyRoster(
        "School of Computing",
        "https://computing.unl.edu/research-innovation/",
        (
            _c("Bonita Sharif", "empirical software engineering; program comprehension; traceability"),
            _c("Robert Dyer", "program analysis; mining software repositories; programming languages"),
            _c("Witawas Srisa-an", "programming languages; secure and dependable systems"),
            _c("Chris Bohn", "software engineering; methodology; software reliability"),
        ),
    ),
    "University of Notre Dame": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://cse.nd.edu/research/",
        (
            _c("Jane Cleland-Huang", "requirements engineering; software assurance; traceability"),
            _c("Collin McMillan", "program comprehension; software documentation; AI for software engineering"),
            _c("Toby Jia-Jun Li", "human-AI interaction; intelligent user interfaces; developer support"),
            _c("Adam Czajka", "trustworthy AI; biometrics; model assurance"),
        ),
    ),
    "Vanderbilt University": FacultyRoster(
        "Department of Computer Science",
        "https://computing.vanderbilt.edu/faculty/",
        (
            _c("Jules White", "AI for software engineering; generative AI; software systems"),
            _c("Abhishek Dubey", "cyber-physical systems; dependable software; resilience"),
            _c("Gabor Karsai", "model-integrated computing; cyber-physical systems; assurance"),
            _c("Taylor T. Johnson", "formal verification; autonomous systems; safety"),
        ),
    ),
    "Virginia Polytechnic Institute and State University": FacultyRoster(
        "Department of Computer Science",
        "https://cs.vt.edu/people/faculty.html",
        (
            _c("Eli Tilevich", "software engineering; program transformation; distributed systems"),
            _c("Muhammad Ali Gulzar", "software testing; distributed systems; debugging"),
            _c("Matthew Hicks", "systems security; trustworthy hardware and software"),
            _c("Stephen Edwards", "software systems; programming languages; embedded systems"),
        ),
    ),
    "Washington University in St Louis": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://engineering.washu.edu/faculty/",
        (
            _c("Ning Zhang", "systems security; software security; trusted computing"),
            _c("Patrick Crowley", "network systems; secure infrastructure; measurement"),
            _c("Yevgeniy Vorobeychik", "adversarial machine learning; security; trustworthy AI"),
            _c("Chien-Ju Ho", "responsible AI; human-AI systems; incentives"),
        ),
    ),
    "William & Mary": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.wm.edu/",
        (
            _c("Bin Ren", "programming systems; compilers; software performance"),
            _c("Qun Li", "security; networked systems; privacy"),
            _c("Adwait Nadkarni", "software security; program analysis; mobile systems"),
            _c("Gang Zhou", "distributed systems; mobile computing; reliability"),
        ),
    ),
    "Concordia University": FacultyRoster(
        "Department of Computer Science and Software Engineering",
        "https://www.concordia.ca/ginacody/computer-science-software-eng/about/faculty-members.html",
        (
            _c("Nikolaos Tsantalis", "software refactoring; program analysis; software evolution"),
            _c("Abdelwahab Hamou-Lhadj", "software diagnostics; log analysis; software reliability"),
            _c("Juergen Rilling", "program comprehension; software maintenance; mining repositories"),
            _c("Joey Paquet", "software engineering; programming languages; software design"),
        ),
    ),
    "McGill University": FacultyRoster(
        "School of Computer Science",
        "https://www.cs.mcgill.ca/people/faculty/",
        (
            _c("Martin Robillard", "software engineering; API design; program comprehension"),
            _c("Gunter Mussbacher", "model-driven engineering; requirements; software design"),
            _c("Borke Obada", "software engineering; program analysis; developer tools"),
            _c("Xujie Si", "program synthesis; programming languages; verification"),
        ),
    ),
    "Queen’s University": FacultyRoster(
        "School of Computing",
        "https://www.cs.queensu.ca/research/faculty/",
        (
            _c("Bram Adams", "software release engineering; mining repositories; software quality"),
            _c("Filipe Cogo", "software engineering; collaborative development; empirical methods"),
            _c("Juergen Dingel", "model-driven engineering; formal methods; software verification"),
            _c("Yuan Tian", "software engineering; program analysis; security"),
        ),
    ),
    "University of Alberta": FacultyRoster(
        "Department of Computing Science",
        "https://apps.ualberta.ca/directory/search/department/360300",
        (
            _c("Karim Ali", "program analysis; software security; programming languages"),
            _c("J. Nelson Amaral", "compilers; program optimization; software systems"),
            _c("Lei Ma", "software engineering; testing; trustworthy machine learning"),
            _c("Omid Ardakanian", "intelligent systems; dependable infrastructure; data-driven systems"),
        ),
    ),
    "University of British Columbia": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.ubc.ca/people/faculty",
        (
            _c("Gail C. Murphy", "software evolution; developer productivity; program understanding"),
            _c("Alex Summers", "program verification; separation logic; software correctness"),
            _c("Ivan Beschastnikh", "distributed systems; software reliability; program analysis"),
            _c("Margo Seltzer", "systems; data provenance; reproducible computing"),
        ),
    ),
    "University of Calgary": FacultyRoster(
        "Department of Computer Science",
        "https://science.ucalgary.ca/computer-science/contacts/faculty-members",
        (
            _c("Hadi Hemmati", "software testing; program repair; AI for software engineering"),
            _c("Gias Uddin", "software engineering; API documentation; developer support"),
            _c("Yani Ioannou", "trustworthy machine learning; computer vision; AI systems"),
            _c("Frank Maurer", "software engineering; agile development; human-centered systems"),
        ),
    ),
    "University of Saskatchewan": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.usask.ca/people/faculty.php",
        (
            _c("Banani Roy", "software evolution; software quality; mining repositories"),
            _c("Zadia Codabux", "software engineering; technical debt; software maintenance"),
            _c("Kevin Schneider", "software engineering; program comprehension; software architecture"),
            _c("Natalia Stakhanova", "cybersecurity; threat detection; secure software"),
        ),
    ),
    "University of Toronto": FacultyRoster(
        "Department of Computer Science",
        "https://uniweb.cs.utoronto.ca/members",
        (
            _c("Steve Engels", "software engineering; program comprehension; computing education"),
            _c("David Lie", "systems security; trusted execution; software isolation"),
            _c("Daniel Wigdor", "human-computer interaction; interactive systems; evaluation"),
            _c("Tovi Grossman", "human-computer interaction; developer tools; interactive systems"),
        ),
    ),
    "University of Victoria": FacultyRoster(
        "Department of Computer Science",
        "https://www.uvic.ca/ecs/computerscience/faculty-staff/index.php",
        (
            _c("Neil Ernst", "software architecture; requirements; software ecosystems"),
            _c("Daniela Damian", "requirements engineering; collaborative software engineering"),
            _c("Yvonne Coady", "programming languages; modularity; software systems"),
            _c("Jens Weber", "software engineering; model-driven development; safety"),
        ),
    ),
    "University of Waterloo": FacultyRoster(
        "Cheriton School of Computer Science",
        "https://uwaterloo.ca/computer-science/about/our-people",
        (
            _c("Mei Nagappan", "software analytics; mining repositories; software quality"),
            _c("Michael W. Godfrey", "software evolution; program comprehension; architecture"),
            _c("Patrick Lam", "program analysis; software engineering; verification"),
            _c("Krzysztof Czarnecki", "software engineering; variability; model-driven systems"),
        ),
    ),
    "ETH Zurich": FacultyRoster(
        "Department of Computer Science",
        "https://inf.ethz.ch/people/faculty/faculty.html",
        (
            _c("Peter Müller", "program verification; software correctness; programming languages"),
            _c("David Basin", "formal methods; information security; software verification"),
            _c("Adrian Perrig", "systems security; secure networks; dependable infrastructure"),
            _c("Markus Püschel", "program generation; compilers; high-performance software"),
        ),
    ),
    "Saarland University": FacultyRoster(
        "Department of Computer Science",
        "https://www.uni-saarland.de/en/university/organization/faculties/professors/mi/computer-science.html",
        (
            _c("Sven Apel", "software engineering; configurable systems; program analysis"),
            _c("Holger Hermanns", "dependable systems; formal verification; software reliability"),
            _c("Benjamin Kaminski", "quantitative verification; program semantics; formal methods"),
            _c("Sebastian Hack", "compilers; programming languages; program optimization"),
        ),
    ),
    "Trinity College Dublin": FacultyRoster(
        "School of Computer Science and Statistics",
        "https://www.tcd.ie/scss/people/academic-staff/",
        (
            _c("Ivana Dusparic", "autonomous systems; reinforcement learning; dependable software"),
            _c("David Lewis", "trustworthy data systems; privacy; adaptive software"),
            _c("Abeba Birhane", "responsible AI; data governance; algorithmic accountability"),
            _c("Stefan Weber", "software systems; cybersecurity; dependable infrastructure"),
        ),
    ),
    "University College London": FacultyRoster(
        "Department of Computer Science",
        "https://www.ucl.ac.uk/engineering/computer-science/people/academic-staff-ucl-profiles",
        (
            _c("Justyna Petke", "automated program repair; genetic improvement; software testing"),
            _c("Federica Sarro", "search-based software engineering; AI for software engineering"),
            _c("Sergey Mechtaev", "automated program repair; program analysis; software reliability"),
            _c("David Clark", "program analysis; information flow; software security"),
        ),
    ),
    "University of Cambridge": FacultyRoster(
        "Department of Computer Science and Technology",
        "https://www.cst.cam.ac.uk/people/directory/faculty?lang=en",
        (
            _c("Peter Sewell", "programming languages; semantics; systems verification"),
            _c("Robert N. M. Watson", "systems security; operating systems; capability systems"),
            _c("Richard Mortier", "distributed systems; dependable infrastructure; data systems"),
            _c("Neel Krishnaswami", "programming languages; verification; type systems"),
        ),
    ),
    "University of Edinburgh": FacultyRoster(
        "School of Informatics",
        "https://www.research.ed.ac.uk/en/organisations/school-of-informatics/persons/",
        (
            _c("Perdita Stevens", "software engineering; model-driven development; formal methods"),
            _c("Murray Cole", "parallel programming; software systems; performance"),
            _c("Stratis Viglas", "data systems; dependable infrastructure; software performance"),
            _c("Paul Jackson", "formal methods; automated reasoning; software verification"),
        ),
    ),
    "University of Oxford": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.ox.ac.uk/people/faculty.html",
        (
            _c("Marta Kwiatkowska", "probabilistic verification; trustworthy AI; formal methods"),
            _c("David Parker", "model checking; quantitative verification; software reliability"),
            _c("Nobuko Yoshida", "programming languages; distributed systems; protocol verification"),
            _c("Niki Trigoni", "cyber-physical systems; sensing; dependable AI systems"),
        ),
    ),
    "University of Wisconsin-Madison": FacultyRoster(
        "Department of Computer Sciences",
        "https://madpl.cs.wisc.edu/",
        (
            _c("Ethan Cecchetti", "programming languages; systems security; verification"),
            _c("Somesh Jha", "software security; program analysis; machine learning security"),
            _c("Adithya Murali", "program verification; automated reasoning; programming languages"),
            _c("Charles Yuan", "programming languages; verification; systems"),
        ),
    ),
    "University of Minnesota-Twin Cities": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://cse.umn.edu/cs/faculty",
        (
            _c("Stephen McCamant", "program analysis; software security; programming languages"),
            _c("Gopalan Nadathur", "logic programming; proof assistants; programming languages"),
            _c("Nick Hopper", "computer security; privacy; applied cryptography"),
            _c("Abhishek Chandra", "distributed systems; cloud computing; systems reliability"),
        ),
    ),
    "University of Colorado Boulder": FacultyRoster(
        "Department of Computer Science",
        "https://plv.colorado.edu/",
        (
            _c("Bor-Yuh Evan Chang", "program analysis; verification; reliable software systems"),
            _c("Danny Dig", "software engineering; program transformation; software evolution"),
            _c("Gowtham Kaki", "programming languages; verification; distributed systems"),
            _c("Dirk Grunwald", "computer systems; compilers; dependable computing"),
        ),
    ),
    "University of Arizona": FacultyRoster(
        "Department of Computer Science",
        "https://cs.arizona.edu/about/faculty",
        (
            _c("Christian Collberg", "software security; obfuscation; program transformation"),
            _c("Sazzadur Rahaman", "software security; program analysis; security auditing"),
            _c("Ravi Sethi", "compilers; programming languages; software technologies"),
            _c("Quinn Burke", "systems security; network security; computer systems"),
        ),
    ),
    "University of Utah": FacultyRoster(
        "Kahlert School of Computing",
        "https://www.cs.utah.edu/people/faculty/",
        (
            _c("Pavel Panchekha", "programming languages; formal verification; numerical software"),
            _c("Stefan Nagy", "software security testing; fuzzing; program analysis"),
            _c("Matthew Flatt", "programming languages; language implementation; software systems"),
            _c("Zvonimir Rakamarić", "formal methods; software verification; static analysis"),
        ),
    ),
    "University of California-San Diego": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://cse.ucsd.edu/people/faculty-profiles",
        (
            _c("Ranjit Jhala", "program verification; refinement types; program analysis"),
            _c("Loris D'Antoni", "program synthesis; automated reasoning; programming languages"),
            _c("Deian Stefan", "secure systems; programming languages; software security"),
            _c("Michael Coblenz", "programming languages; human-centered software engineering"),
        ),
    ),
    "Duke University": FacultyRoster(
        "Department of Computer Science",
        "https://cs.duke.edu/research/security-and-privacy",
        (
            _c("Matthew Lentz", "secure trustworthy systems; systems verification; cloud infrastructure"),
            _c("Pardis Emami-Naeini", "usable privacy and security; trustworthy systems"),
            _c("Kartik Nayak", "distributed systems security; blockchains; applied cryptography"),
            _c("Michael Reiter", "systems security; software security; distributed systems"),
        ),
    ),
    "Brown University": FacultyRoster(
        "Department of Computer Science",
        "https://cs.brown.edu/people/faculty/",
        (
            _c("Shriram Krishnamurthi", "programming languages; software engineering; formal methods"),
            _c("Nikos Vasilakis", "programming systems; software security; distributed systems"),
            _c("Deepti Raghavan", "systems; secure software; AI systems"),
            _c("Kathi Fisler", "formal methods; programming languages; software engineering"),
        ),
    ),
    "University of Virginia-Main Campus": FacultyRoster(
        "Department of Computer Science",
        "https://engineering.virginia.edu/department/computer-science/people",
        (
            _c("Kevin Sullivan", "software engineering; formal methods; systems assurance"),
            _c("Matthew Dwyer", "software engineering; program analysis; verification"),
            _c("Wajih Ul Hassan", "systems security; software analysis; threat detection"),
            _c("Samira Khan", "computer systems; reliability; architecture"),
        ),
    ),
    "Simon Fraser University": FacultyRoster(
        "School of Computing Science",
        "https://www.sfu.ca/fas/computing/people/faculty.html",
        (
            _c("Anders Miltner", "program synthesis; automated refactoring; verification"),
            _c("William Nick Sumner", "software testing; program analysis; automated repair"),
            _c("Steven Y. Ko", "distributed systems; vulnerability discovery and repair"),
            _c("Yuepeng Wang", "program synthesis; programming languages; software engineering"),
        ),
    ),
}
