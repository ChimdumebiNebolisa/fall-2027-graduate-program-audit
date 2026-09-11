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
            _c("Zhijie Wang", "AI for software engineering; software quality; human factors"),
            _c("Yann-Gaël Guéhéneuc", "program comprehension; software quality; empirical software engineering"),
        ),
    ),
    "McMaster University": FacultyRoster(
        "Department of Computing and Software",
        "https://www.eng.mcmaster.ca/cas/research/software-and-its-engineering/",
        (
            _c("Spencer Smith", "software quality; requirements; research software engineering"),
            _c("Istvan David", "model-driven engineering; software testing; digital twins"),
            _c("Mark Lawford", "formal methods; software certification; safety-critical systems"),
            _c("Sébastien Mosser", "software architecture; DevOps; microservices; modelling"),
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
    "University of Alabama at Birmingham": FacultyRoster(
        "Department of Computer Science",
        "https://www.uab.edu/cas/computerscience/people/faculty-directory",
        (
            _c("Emily (Shuya) Feng", "AI security; data privacy; responsible AI; model security"),
            _c("Yuliang Zheng", "cybersecurity; digital privacy; modern cryptography"),
            _c("Chengcui Zhang", "data mining; multimedia forensics; machine learning"),
            _c("Baocheng Geng", "distributed systems; Internet of Things; explainable AI"),
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
        "Departments of Electrical and Computer Engineering / Computer Science",
        "https://www.uvic.ca/ecs/software/research/our-researchers/index.php",
        (
            _c("Neil Ernst", "software architecture; requirements; software ecosystems"),
            _c("Daniela Damian", "requirements engineering; collaborative software engineering"),
            _c("Yvonne Coady", "programming languages; modularity; software systems"),
            _c("Jens Weber", "software engineering; model-driven development; safety"),
        ),
    ),
    "University of Waterloo": FacultyRoster(
        "Cheriton School of Computer Science / Department of Electrical and Computer Engineering",
        "https://uwaterloo.ca/electrical-computer-engineering/contacts?group%5B61%5D=61&title=",
        (
            _c("Mei Nagappan", "software analytics; mining repositories; software quality"),
            _c("Michael W. Godfrey", "software evolution; program comprehension; architecture"),
            _c("Werner Dietl", "programming languages; type systems; program verification"),
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
    "Rutgers University-New Brunswick": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.rutgers.edu/people/directory.php?type=faculty",
        (
            _c("Shiqing Ma", "software security; program analysis; systems security"),
            _c("Zheng Zhang", "programming languages; compilers; software systems"),
            _c("He Zhu", "programming languages; formal methods; software systems"),
            _c("Ulrich Kremer", "compilers; runtime systems; programming systems"),
        ),
    ),
    "Ohio State University-Main Campus": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://cse.osu.edu/directory/faculty",
        (
            _c("Michael Bond", "program analysis; software systems; reliability; security"),
            _c("Atanas Rountev", "static and dynamic analysis; testing; software evolution"),
            _c("Carter Yagemann", "systems security; software security; vulnerability analysis"),
            _c("Neelam Soundarajan", "formal correctness; software engineering; programming languages"),
        ),
    ),
    "Stony Brook University": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.stonybrook.edu/people/faculty",
        (
            _c("R. Sekar", "software security; program analysis; systems security"),
            _c("Y. Annie Liu", "programming languages; verification; distributed systems"),
            _c("Michalis Polychronakis", "systems security; vulnerability analysis; malware defense"),
            _c("Erez Zadok", "operating systems; file systems; software reliability"),
        ),
    ),
    "University of California-Santa Barbara": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.ucsb.edu/people/faculty",
        (
            _c("Ben Hardekopf", "programming languages; static analysis; software verification"),
            _c("Giovanni Vigna", "software security; vulnerability analysis; systems security"),
            _c("Christopher Kruegel", "systems security; program analysis; malware detection"),
            _c("Chandra Krintz", "programming systems; cloud systems; software performance"),
        ),
    ),
    "University of Delaware": FacultyRoster(
        "Department of Computer and Information Sciences",
        "https://www.cis.udel.edu/research/computing-foundations/",
        (
            _c("James Clause", "software testing; program analysis; software engineering"),
            _c("Sunita Chandrasekaran", "parallel programming; compilers; verification"),
            _c("Xi Peng", "trustworthy AI; explainable AI; software systems"),
            _c("Austin Cory Bart", "software tools; programming systems; software engineering"),
        ),
    ),
    "Boston University": FacultyRoster(
        "Department of Computer Science",
        "https://www.bu.edu/cs/about/people/faculty/",
        (
            _c("Marco Gaboardi", "programming languages; program verification; privacy"),
            _c("Hongwei Xi", "type systems; safe software; programming languages"),
            _c("Manuel Egele", "software security; program analysis; vulnerability detection"),
            _c("Gianluca Stringhini", "systems security; abuse detection; trustworthy systems"),
        ),
    ),
    "University of North Carolina at Charlotte": FacultyRoster(
        "College of Computing and Informatics, Software and Information Systems",
        "https://cci.charlotte.edu/sis-faculty/",
        (
            _c("Meera Sridhar", "language and systems security; formal methods; software assurance"),
            _c("Rrezarta Krasniqi", "AI for software engineering; software quality; maintenance"),
            _c("L. Jean Camp", "computer security; privacy; trustworthy systems"),
            _c("Heather Lipford", "usable security; privacy; secure software design"),
        ),
    ),
    "York University": FacultyRoster(
        "Department of Electrical Engineering and Computer Science",
        "https://lassonde.yorku.ca/eecs/academics/graduate/graduate-faculty/",
        (
            _c("Song Wang", "AI for software engineering; testing; static analysis"),
            _c("Maleknaz Nayebi", "empirical software engineering; release engineering; platforms"),
            _c("Franck van Breugel", "concurrency; formal verification; software semantics"),
            _c("Marios Fokaefs", "software engineering; cloud systems; service computing"),
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
    "Colorado State University-Fort Collins": FacultyRoster(
        "Department of Computer Science",
        "https://compsci.colostate.edu/people/",
        (
            _c("Ravi Mangal", "programming languages; program analysis; verification"),
            _c("Indrakshi Ray", "formal methods; database security; secure software"),
            _c("Vinayak Prabhu", "formal methods; hybrid systems; verification"),
            _c("Yashwant Malaiya", "software reliability; testing; vulnerability discovery"),
        ),
    ),
    "University of Central Florida": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.ucf.edu/faculty-directory/",
        (
            _c("David Mohaisen", "software and systems security; threat detection; trustworthy systems"),
            _c("Yan Solihin", "computer architecture; systems security; dependable computing"),
            _c("Cliff Zou", "network and software security; vulnerability analysis"),
            _c("Liqiang Wang", "distributed systems; software systems; machine learning"),
        ),
    ),
    "University of Illinois Chicago": FacultyRoster(
        "Department of Computer Science",
        "https://cs.uic.edu/cs-research/research-areas-2/",
        (
            _c("William Mansky", "formal verification; program logic; software analysis"),
            _c("Luis Pina", "program analysis; programming languages; software systems"),
            _c("Ugo Buy", "software analysis; software engineering; formal methods"),
            _c("Venkat Venkatakrishnan", "software security; program analysis; secure systems"),
        ),
    ),
    "University of Kansas": FacultyRoster(
        "Department of Electrical Engineering and Computer Science",
        "https://eecs.ku.edu/faculty",
        (
            _c("Drew J. Davidson", "program analysis; secure design; software security"),
            _c("Hossein Saiedian", "formal methods; secure software engineering; software architecture"),
            _c("Alexandru Bardas", "cybersecurity; systems security; dependable systems"),
            _c("Hongyang Sun", "distributed systems; fault tolerance; resilient computing"),
        ),
    ),
    "University of Kentucky": FacultyRoster(
        "Department of Computer Science",
        "https://cs.engr.uky.edu/people-4",
        (
            _c("A.B. Siddique", "AI for software engineering; code language models; trustworthy NLP"),
            _c("Zongming Fei", "distributed systems; cybersecurity; cloud computing"),
            _c("Kenneth L. Calvert", "network security; programmable infrastructure; dependable networks"),
            _c("Dakshnamoorthy Manivannan", "distributed systems; fault tolerance; software systems"),
        ),
    ),
    "Stevens Institute of Technology": FacultyRoster(
        "Department of Computer Science",
        "https://www.stevens.edu/page-minisite-landing/computer-science-department",
        (
            _c("David Naumann", "program verification; programming languages; secure software"),
            _c("William Eiers", "formal methods; quantitative program analysis; verification"),
            _c("Michael Greenberg", "programming languages; software reliability; program analysis"),
            _c("Eric Koskinen", "program verification; concurrency; formal methods"),
        ),
    ),
    "University of New Mexico-Main Campus": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.unm.edu/directory/index.html",
        (
            _c("Patrick G. Bridges", "fault tolerance; operating systems; large-scale systems"),
            _c("Afsah Anwar", "distributed systems; cloud computing; dependable systems"),
            _c("Matthew Lakin", "formal methods; programming languages; verified systems"),
            _c("Abdullah A. Mueen", "data mining; time-series analysis; reliable analytics"),
        ),
    ),
    "The University of Tennessee-Knoxville": FacultyRoster(
        "Min H. Kao Department of Electrical Engineering and Computer Science",
        "https://eecs.utk.edu/faculty/",
        (
            _c("Scott Ruoti", "systems security; usable security; web security"),
            _c("Doowon Kim", "cybersecurity; mobile systems; human-centered security"),
            _c("Michael Jantz", "compilers; software systems; program optimization"),
            _c("Qing Charles Cao", "networked systems; cybersecurity; dependable computing"),
        ),
    ),
    "University of Rochester": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.rochester.edu/people/faculty/index.html",
        (
            _c("Chen Ding", "compilers; program analysis; software performance; memory systems"),
            _c("Michael L. Scott", "concurrent programming; distributed systems; programming languages"),
            _c("Daniel Gildea", "natural language processing; trustworthy language systems; evaluation"),
            _c("Henry Kautz", "knowledge representation; trustworthy AI; automated reasoning"),
        ),
    ),
    "University of Maryland-Baltimore County": FacultyRoster(
        "Department of Computer Science and Electrical Engineering",
        "https://www.csee.umbc.edu/people/tenure-track-faculty/",
        (
            _c("Tim Finin", "knowledge representation; semantic web; trustworthy data systems"),
            _c("Karuna Joshi", "cloud security; data governance; policy-based systems"),
            _c("Naghmeh Karimi", "hardware and software security; trustworthy computing; verification"),
            _c("Roberto Yus", "privacy; data management; mobile and pervasive systems"),
        ),
    ),
    "University of California-Riverside": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www1.cs.ucr.edu/people/faculty",
        (
            _c("Manu Sridharan", "program analysis; software engineering; programming languages"),
            _c("Rajiv Gupta", "dynamic program analysis; compilers; debugging; software reliability"),
            _c("Zhijia Zhao", "programming systems; compilers; performance; reliable software"),
            _c("Heng Yin", "systems security; program analysis; malware and vulnerability analysis"),
        ),
    ),
    "University of Houston": FacultyRoster(
        "Department of Computer Science",
        "https://www.uh.edu/nsm/computer-science/people/faculty/",
        (
            _c("Amin Alipour", "software testing; program analysis; empirical software engineering"),
            _c("Weidong Shi", "software and systems security; trustworthy computing"),
            _c("Rakesh Verma", "cybersecurity; trustworthy AI; language and security analytics"),
            _c("Omprakash Gnawali", "networked systems; dependable software systems; IoT"),
        ),
    ),
    "The University of Texas at Arlington": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.uta.edu/academics/schools-colleges/engineering/academics/departments/cse/faculty-directory",
        (
            _c("Allison Sullivan", "formal methods; software correctness; program verification"),
            _c("Jiang Ming", "software security; program analysis; vulnerability detection"),
            _c("Matthew Wright", "computer security; privacy; trustworthy systems"),
            _c("Hong Jiang", "distributed systems; storage systems; reliable computing"),
        ),
    ),
    "The University of Texas at San Antonio": FacultyRoster(
        "Department of Computer Science",
        "https://sciences.utsa.edu/computer-science/faculty/",
        (
            _c("Jianwei Niu", "software engineering; privacy; requirements; program analysis"),
            _c("Rocky Slavin", "software security; program analysis; mobile privacy"),
            _c("Mitra Bokaei Hosseini", "requirements engineering; privacy; trustworthy software"),
            _c("Murtuza Jadliwala", "systems security; privacy; dependable mobile systems"),
        ),
    ),
    "University of Iowa": FacultyRoster(
        "Department of Computer Science",
        "https://cs.uiowa.edu/people/faculty",
        (
            _c("Katherine Kosaian", "formal verification; proof assistants; automated reasoning"),
            _c("J. Garrett Morris", "programming languages; type systems; formal logic"),
            _c("Taylor Olson", "programming languages; formal methods; software correctness"),
            _c("Rishab Nithyanand", "security; privacy; measurement; trustworthy online systems"),
        ),
    ),
    "Clemson University": FacultyRoster(
        "School of Computing",
        "https://www.clemson.edu/cecas/departments/computing/people/",
        (
            _c("Mert Pese", "software and automotive security; reverse engineering; trustworthy systems"),
            _c("Long Cheng", "cybersecurity; cloud and edge systems; privacy"),
            _c("Jacob Sorber", "embedded systems; dependable computing; sensing systems"),
            _c("Carlos Toxtli-Hernández", "human-centered software; collaborative systems; developer experience"),
        ),
    ),
    "North Dakota State University-Main Campus": FacultyRoster(
        "Department of Computer Science",
        "https://www.ndsu.edu/cs/people/faculty/",
        (
            _c("Gursimran Walia", "empirical software engineering; software testing; requirements engineering; software quality"),
            _c("Jeremy Straub", "cybersecurity; artificial intelligence; robotics; trustworthy systems"),
            _c("Jun Kong", "model-driven software engineering; human-computer interaction; software visualization"),
            _c("Simone Ludwig", "machine learning; computational intelligence; privacy and security"),
        ),
    ),
    "Boise State University": FacultyRoster(
        "Department of Computer Science; School of Computing",
        "https://www.boisestate.edu/coen-cs/people/faculty/",
        (
            _c("Hoda Mehrpouyan", "formal verification; cybersecurity; cyber-physical systems; trustworthy computing"),
            _c("Max Taylor", "formal methods; systems security; dependability; software assurance"),
            _c("Gaby Dagher", "security and privacy; data security; trustworthy systems"),
            _c("Jyh-haw Yeh", "cybersecurity; cyber-physical systems; dependable computing"),
        ),
    ),
    "Florida International University": FacultyRoster(
        "Knight Foundation School of Computing and Information Sciences",
        "https://www.cis.fiu.edu/faculty-staff/",
        (
            _c("Bogdan Carbunar", "systems security; privacy; distributed systems; mobile security"),
            _c("Ruimin Sun", "cyber-physical systems security; mobile security; trustworthy systems"),
            _c("Selcuk Uluagac", "Internet of Things security; cyber-physical security; privacy"),
            _c("Farhad Shirani", "privacy; security; information theory; trustworthy machine learning"),
        ),
    ),
    "Ontario Tech University": FacultyRoster(
        "Department of Electrical, Computer and Software Engineering",
        "https://engineering.ontariotechu.ca/people/ecse/index.php",
        (
            _c("Akramul Azim", "embedded software; model-based testing; software verification; real-time systems"),
            _c("Khalid Elgazzar", "intelligent software systems; distributed systems; Internet of Things"),
            _c("Masoud Makrehchi", "artificial intelligence; data analytics; trustworthy learning systems"),
            _c("Mohamed El-Darieby", "software systems; Internet of Things; intelligent infrastructure"),
        ),
    ),
    "Carleton University": FacultyRoster(
        "Department of Systems and Computer Engineering",
        "https://carleton.ca/sce/faculty/",
        (
            _c("Nafiseh Kahani", "AI-based software testing; automated test repair; software engineering"),
            _c("Jason Jaskolka", "model-driven security; formal methods; software assurance"),
            _c("Babak Esfandiari", "software agents; distributed software systems; software engineering"),
            _c("Hala Assal", "usable security; privacy; human-centered software systems"),
        ),
    ),
    "University of Trento": FacultyRoster(
        "Department of Information Engineering and Computer Science",
        "https://www.disi.unitn.it/research/programs/sweng",
        (
            _c("Chiara Di Francescomarino", "process mining; business-process management; software engineering"),
            _c("Paolo Giorgini", "agent-oriented software; requirements engineering; security engineering"),
            _c("Alessandro Marchetto", "software testing; empirical software engineering; software quality"),
            _c("Roberto Sebastiani", "automated reasoning; formal methods; software verification"),
        ),
    ),
    "University of Manitoba": FacultyRoster(
        "Department of Computer Science",
        "https://umanitoba.ca/science/directory/computer-science",
        (
            _c("Tristan Miller", "natural language processing; automated reasoning; trustworthy AI"),
            _c("Mengjun Hu", "cybersecurity; data systems; trustworthy machine learning"),
            _c("Jimmy Zhu", "machine learning; software systems; reliable data analysis"),
            _c("Shaiful Chowdhury", "software systems; artificial intelligence; data-driven computing"),
        ),
    ),
    "Baylor University": FacultyRoster(
        "Department of Computer Science",
        "https://www.ecs.baylor.edu/departments/computer-science/computer-science-faculty",
        (
            _c("Eunjee Song", "software engineering; model-driven engineering; software testing"),
            _c("Xiao Shou", "cybersecurity; secure systems; threat analysis"),
            _c("Chen Zhao", "trustworthy artificial intelligence; security; data systems"),
            _c("Greg Hamerly", "machine learning; data mining; reliable intelligent systems"),
        ),
    ),
    "Rice University": FacultyRoster(
        "Department of Computer Science",
        "https://compsci.rice.edu/people/faculty",
        (
            _c("Dan S. Wallach", "systems security; software security; electronic voting"),
            _c("Ang Chen", "network security; distributed systems; secure infrastructure"),
            _c("Yuke Wang", "systems security; trustworthy AI infrastructure; computer architecture"),
            _c("Scott Rixner", "computer systems; virtualization; reliable infrastructure"),
        ),
    ),
    "Washington State University": FacultyRoster(
        "School of Electrical Engineering and Computer Science",
        "https://school.eecs.wsu.edu/directory/",
        (
            _c("Xu Lin", "web security; software security; vulnerability analysis"),
            _c("Janardhan Rao Doppa", "artificial intelligence; trustworthy machine learning; optimization"),
            _c("Leon Li", "cybersecurity; systems security; privacy"),
            _c("Shih-Lien Lu", "computer systems; architecture; dependable computing"),
        ),
    ),
    "University of South Florida": FacultyRoster(
        "Bellini College of Artificial Intelligence, Cybersecurity and Computing",
        "https://www.usf.edu/ai-cybersecurity-computing/people/faculty/",
        (
            _c("Jay Ligatti", "software security; programming languages; program enforcement"),
            _c("Xinming Ou", "cybersecurity; attack analysis; security automation"),
            _c("Hao Zheng", "formal methods; software verification; cyber-physical systems"),
            _c("Tempestt Neal", "identity; trustworthy artificial intelligence; usable security"),
        ),
    ),
    "University of Gothenburg": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.gu.se/en/about/find-organisation/department-of-computer-science-and-engineering-3",
        (
            _c("Robert Feldt", "software engineering; software testing; artificial intelligence"),
            _c("Richard Torkar", "empirical software engineering; software analytics; quality"),
            _c("Jennifer Horkoff", "requirements engineering; modeling; explainable systems"),
            _c("Daniel Strüber", "model-driven engineering; software evolution; program transformation"),
        ),
    ),
    "University of Cincinnati-Main Campus": FacultyRoster(
        "Department of Computer Science",
        "https://www.ceas.uc.edu/academics/departments/computer-science/computer-science-people.html",
        (
            _c("Chong Yu", "secure software; federated learning; networked systems; AI-enabled software"),
            _c("Tianyu Jiang", "natural language processing; trustworthy language models; software intelligence"),
            _c("Swastik Brahma", "networked systems; human-in-the-loop systems; dependable computing"),
            _c("Boyang Wang", "binary analysis; embedded-system security; privacy; applied cryptography"),
        ),
    ),
    "Virginia Commonwealth University": FacultyRoster(
        "Department of Computer Science",
        "https://egr.vcu.edu/departments/computer-science/research/research-clusters/",
        (
            _c("Rodrigo Spinola", "software engineering; software evolution; human-centered software"),
            _c("Thomas Gyeera", "software engineering; computer systems; AI and data science"),
            _c("Luke Gusukuma", "software engineering; human-centered computing; developer tools"),
            _c("Irfan Ahmed", "digital forensics; malware analysis; cyber-physical systems security"),
        ),
    ),
    "University of Guelph": FacultyRoster(
        "School of Computer Science",
        "https://www.uoguelph.ca/computing/future/graduate-studies",
        (
            _c("Ali Dehghantanha", "cybersecurity; threat intelligence; AI-assisted security analysis"),
            _c("Rozita Dara", "privacy; trustworthy artificial intelligence; data governance"),
            _c("Xiaodong Lin", "cybersecurity; privacy; secure systems and communications"),
            _c("John Akinyemi", "software engineering; information retrieval; knowledge graphs; graph databases"),
        ),
    ),
    "École Polytechnique de Montréal": FacultyRoster(
        "Department of Computer Engineering and Software Engineering",
        "https://www.polymtl.ca/gigl/en/research/areas-research",
        (
            _c("Mohammad Hamdaqa", "software engineering; cloud software; software architecture; developer tools"),
            _c("Foutse Khomh", "software quality; machine-learning systems; software analytics; trustworthy AI"),
            _c("Heng Li", "software engineering; software performance; trace analysis; software analytics"),
            _c("Zohreh Sharafi", "software engineering; program comprehension; human factors; developer studies"),
        ),
    ),
    "Emory University": FacultyRoster(
        "Department of Computer Science",
        "https://computerscience.emory.edu/graduate-phd/csi-faculty.html",
        (
            _c("Ymir Vigfusson", "distributed systems; systems security; privacy; networked systems"),
            _c("Wei Jin", "trustworthy artificial intelligence; graph learning; privacy; robustness"),
            _c("Subhasish Das", "computer systems; distributed systems; systems education"),
            _c("Joon-Seok Kim", "distributed computing; data-intensive systems; simulation"),
        ),
    ),
    "Northwestern University": FacultyRoster(
        "Department of Computer Science",
        "https://www.mccormick.northwestern.edu/computer-science/people/faculty/tenure-track.html",
        (
            _c("Christos Dimoulas", "programming languages; software contracts; program verification"),
            _c("Simone Campanoni", "compilers; program optimization; software performance"),
            _c("Yan Chen", "network security; distributed systems; systems measurement"),
            _c("Jennie Rogers", "database systems; data analytics; reliable data infrastructure"),
        ),
    ),
    "University of Pittsburgh-Pittsburgh Campus": FacultyRoster(
        "Department of Computer Science",
        "https://www.sci.pitt.edu/people/faculty",
        (
            _c("Panos K. Chrysanthis", "database systems; distributed systems; data privacy"),
            _c("Daniel Mossé", "real-time systems; dependable systems; distributed computing"),
            _c("Longfei Shangguan", "networked systems; sensing; mobile computing; security"),
            _c("Balaji Palanisamy", "distributed systems; cloud computing; privacy; data management"),
        ),
    ),
    "Brandeis University": FacultyRoster(
        "Michtom School of Computer Science",
        "https://www.brandeis.edu/computer-science/people/index.html",
        (
            _c("Liuba Shrira", "distributed systems; reliable storage; fault tolerance"),
            _c("Olga Papaemmanouil", "database systems; data analytics; scalable data management"),
            _c("Kostas Solomos", "web security; privacy; network measurement"),
            _c("Elijah Rivera", "program synthesis; formal verification; programming languages"),
        ),
    ),
    "Johns Hopkins University": FacultyRoster(
        "Department of Computer Science",
        "https://www.cs.jhu.edu/faculty/",
        (
            _c("Avi Rubin", "systems security; software security; privacy"),
            _c("Abhishek Jain", "cryptography; privacy; secure computation"),
            _c("Ashutosh Dhekne", "networked systems; wireless systems; systems measurement"),
            _c("Anton Dahbura", "cybersecurity; dependable systems; critical infrastructure"),
        ),
    ),
    "St. Francis Xavier University": FacultyRoster(
        "Department of Computer Science",
        "https://www.stfx.ca/directory-department/761?groupid=581",
        (
            _c("Hao Cai", "artificial intelligence; data-driven computing; software systems"),
            _c("Jean-Alexis Delamer", "algorithms; theoretical computer science; optimization"),
            _c("Milton King", "machine learning; data science; computational applications"),
            _c("Man Lin", "software systems; data management; computer science education"),
        ),
    ),
    "University of Oregon": FacultyRoster(
        "Department of Computer Science",
        "https://cas.uoregon.edu/directory/computer-science-faculty",
        (
            _c("Reza Rejaie", "distributed systems; network measurement; dependable networked systems"),
            _c("Ram Durairajan", "networked systems; Internet measurement; resilient infrastructure"),
            _c("Yingjiu Li", "cybersecurity; privacy; applied cryptography; trustworthy systems"),
            _c("Jun Li", "network security; Internet measurement; dependable systems"),
        ),
    ),
    "University of Georgia": FacultyRoster(
        "School of Computing",
        "https://www.cs.uga.edu/faculty-directory",
        (
            _c("Kyu Hyung Lee", "systems security; malware analysis; software security"),
            _c("Roberto Perdisci", "network security; malware analysis; threat detection"),
            _c("In Kee Kim", "cloud computing; distributed systems; systems reliability"),
            _c("Shelby H. Funk", "real-time systems; distributed systems; dependable computing"),
        ),
    ),
    "Georgia State University": FacultyRoster(
        "Department of Computer Science",
        "https://csds.gsu.edu/directory/",
        (
            _c("Zhipeng Cai", "privacy and security; networking; trustworthy machine learning"),
            _c("Ashwin Ashok", "networked sensing; mobile systems; dependable computing"),
            _c("Esra Akbas", "data mining; graph learning; trustworthy data analysis"),
            _c("Yingshu Li", "distributed computing; wireless networks; privacy and security"),
        ),
    ),
    "University of South Carolina-Columbia": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.cse.sc.edu/isl/people",
        (
            _c("Csilla Farkas", "data security; privacy; provenance; information assurance"),
            _c("Biplav Srivastava", "trustworthy artificial intelligence; planning; responsible systems"),
            _c("Stephen A. Fenner", "algorithms; cryptography; theoretical computer science"),
            _c("Peng Fu", "programming languages; formal methods; software verification"),
        ),
    ),
    "University of Nevada-Reno": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.unr.edu/cse/people",
        (
            _c("Fred Harris, Jr.", "software systems; data infrastructure; scientific computing"),
            _c("Lei Yang", "data and software systems; networked systems; computing infrastructure"),
            _c("Shamik Sengupta", "cybersecurity; wireless networks; dependable systems"),
            _c("Niusen Chen", "cybersecurity; network systems; trustworthy computing"),
        ),
    ),
    "University of Louisiana at Lafayette": FacultyRoster(
        "School of Computing and Informatics",
        "https://computing.louisiana.edu/about-us/faculty-staff-0",
        (
            _c("Sheng Chen", "programming languages; software engineering; language security"),
            _c("Shuvalaxmi Dass", "software security; misconfiguration security; machine learning"),
            _c("Xiali Sharon Hei", "mobile and wireless security; privacy; digital forensics"),
            _c("Arun Lakhotia", "software engineering; cybersecurity; trusted computing"),
        ),
    ),
    "Montana State University": FacultyRoster(
        "Gianforte School of Computing",
        "https://web1vm.cs.montana.edu/research.html",
        (
            _c("Clem Izurieta", "software engineering; software evolution; cybersecurity; quality assurance"),
            _c("Matt Revelle", "computer security; program analysis; binary analysis; exploit detection"),
            _c("Ann Marie Reinhold", "environmental data science; cybersecurity threat detection"),
            _c("Neda Nazemi", "data mining; machine learning; time-series analysis"),
        ),
    ),
    "Tennessee Technological University": FacultyRoster(
        "Department of Computer Science",
        "https://www.tntech.edu/engineering/programs/csc/faculty-and-staff.php",
        (
            _c("Amani Altarawneh", "cybersecurity; formal methods; IoT; blockchain consensus"),
            _c("Anthony Skjellum", "high-performance computing; scalable systems; IoT and blockchain security"),
            _c("Michael Rogers", "distributed computing; operating systems; network protocols"),
            _c("Gerald Gannod", "software engineering; agile methods; enterprise software; data"),
        ),
    ),
    "University of Wyoming": FacultyRoster(
        "Department of Electrical Engineering and Computer Science",
        "https://www.uwyo.edu/eecs/faculty-staff/index.html",
        (
            _c("Duong Nguyen", "distributed systems; fault tolerance; cloud and IoT computing"),
            _c("Yibo Wang", "systems security; software engineering; blockchain and network measurement"),
            _c("Diksha Shukla", "secure and trustworthy machine learning; authentication; side channels"),
            _c("Ruben Gamboa", "formal methods; theorem proving; software verification"),
        ),
    ),
    "Trent University": FacultyRoster(
        "Department of Computer Science",
        "https://www.trentu.ca/cois/faculty-research",
        (
            _c("Richard Hurley", "distributed systems; systems performance; networking"),
            _c("Bin Guo", "parallel and distributed computing; concurrency; graph algorithms"),
            _c("Wenying Feng", "web caching; network intrusion detection; data systems"),
            _c("Makhdumabanu Saiyed", "network security; IoT; artificial intelligence; machine learning"),
        ),
    ),
    "University of Pisa": FacultyRoster(
        "Department of Computer Science",
        "https://di.unipi.it/en/people/",
        (
            _c("Stefano Forti", "cloud-edge systems; secure software; distributed applications"),
            _c("Gabriele Mencagli", "parallel systems; data streams; distributed computing"),
            _c("Massimo Torquati", "parallel and distributed systems; high-performance data processing"),
            _c("Chiara Bodei", "formal methods; IoT security; software analysis"),
        ),
    ),
    "University of Florence": FacultyRoster(
        "Department of Mathematics and Computer Science",
        "https://www.dimai.unifi.it/vp-484-staff-members.html",
        (
            _c("Andrea Bondavalli", "dependability; critical systems; cyber-physical systems"),
            _c("Alessandro Fantechi", "formal methods; safety-critical systems; verification"),
            _c("Paolo Lollini", "resilient computing; security; dependability assessment"),
            _c("Tommaso Zoppi", "intrusion detection; anomaly detection; trustworthy software"),
        ),
    ),
    "Università di Camerino": FacultyRoster(
        "School of Science and Technology, Computer Science Division",
        "https://sst.unicam.it/corsi/computer-science",
        (
            _c("Andrea Polini", "software testing; model-driven engineering; IoT systems"),
            _c("Flavio Corradini", "formal specification; verification; distributed and real-time systems"),
            _c("Andrea Morichetta", "software engineering; cloud-native systems; microservices"),
            _c("Diletta Cacciagrano", "concurrency; formal semantics; process calculi"),
        ),
    ),
    "University of Idaho": FacultyRoster(
        "College of Engineering, Department of Computer Science and Cybersecurity",
        "https://www.uidaho.edu/engineering/academics/computer-science",
        (
            _c("Frederick T. Sheldon", "cybersecurity; critical infrastructure; cyber-physical systems; software assurance"),
            _c("Xiaogang Ma", "data systems; semantics; scientific cyberinfrastructure; reproducibility"),
            _c("Terence Soule", "evolutionary computation; machine learning; resilient systems"),
            _c("Min Xian", "computer vision; machine learning; data-driven systems"),
        ),
    ),
    "Kansas State University": FacultyRoster(
        "Carl R. Ice College of Engineering, Department of Computer Science",
        "https://www.cs.ksu.edu/about/people/faculty/",
        (
            _c("John Hatcliff", "formal methods; high-assurance systems; model-based engineering; verification"),
            _c("Eugene Vasserman", "cybersecurity; cyber-physical systems; usable security; dependable systems"),
            _c("Arslan Munir", "embedded systems; trustworthy computing; cyber-physical systems; AI assurance"),
            _c("Pascal Hitzler", "knowledge representation; neuro-symbolic AI; explainable reasoning"),
        ),
    ),
    "Oklahoma State University-Main Campus": FacultyRoster(
        "College of Arts and Sciences, Department of Computer Science",
        "https://cas.okstate.edu/computer_science/about_us/faculty_staff",
        (
            _c("Sharmin Jahan", "cybersecurity; trustworthy AI; security education"),
            _c("Anirudh Paranjothi", "vehicular networks; intrusion detection; fog computing; cyber-physical security"),
            _c("Atriya Sen", "explainable AI; reasoning; knowledge-guided machine learning"),
            _c("H B Acharya", "systems security; networked systems; software and data security"),
        ),
    ),
    "West Virginia University": FacultyRoster(
        "Lane Department of Computer Science and Electrical Engineering",
        "https://directory.statler.wvu.edu/tenure-track-faculty",
        (
            _c("Donald Adjeroh", "data analytics; machine learning; dependable data systems"),
            _c("K. Subramani", "algorithms; formal reasoning; theoretical computer science"),
            _c("Piotr Wojciechowski", "distributed systems; algorithms; concurrent computing"),
            _c("Gianfranco Doretto", "computer vision; machine learning; trustworthy perception systems"),
        ),
    ),
    "Louisiana State University and Agricultural & Mechanical College": FacultyRoster(
        "College of Engineering, Division of Computer Science and Engineering",
        "https://www.lsu.edu/eng/cse/people/faculty/index.php",
        (
            _c("Aisha Ali-Gombe", "systems security; network forensics; malware analysis; cyber operations"),
            _c("Umar Farooq", "program analysis; compilers; mobile systems; software reliability"),
            _c("Nash Mahmoud", "software engineering; software evolution; program comprehension"),
            _c("Felipe Fronchetti", "software engineering; human-robot interaction; empirical methods"),
        ),
    ),
    "Brock University": FacultyRoster(
        "Faculty of Mathematics and Science, Department of Computer Science",
        "https://brocku.ca/mathematics-science/computer-science/faculty-staff/",
        (
            _c("Naser Ezzati-Jivan", "software analytics; trace analysis; observability; machine learning"),
            _c("Michael Winter", "formal methods; relational methods; program specification and verification"),
            _c("Rahnuma Nishat", "algorithms; graph theory; computational methods"),
            _c("Sajal Saha", "artificial intelligence; data analytics; intelligent systems"),
        ),
    ),
    "University of Alabama in Huntsville": FacultyRoster(
        "College of Science, Department of Computer Science",
        "https://www.uah.edu/science/departments/computer-science/faculty-staff",
        (
            _c("Chaity Banerjee", "artificial intelligence; data science; cybersecurity; trustworthy computing"),
            _c("Jingshu Chen", "digital forensics; cybersecurity; security analysis"),
            _c("Tathagata Mukherjee", "cybersecurity; machine learning; systems security"),
            _c("Vineetha Menon", "machine learning; artificial intelligence; cybersecurity; data analytics"),
        ),
    ),
    "The University of Texas at El Paso": FacultyRoster(
        "College of Engineering, Department of Computer Science",
        "https://www.utep.edu/cs/people/",
        (
            _c("Eric Freudenthal", "software assurance; systems security; vulnerability analysis"),
            _c("Marcelo Frias", "formal methods; software verification; program analysis"),
            _c("Ann Q. Gates", "software engineering; software processes; trustworthy systems"),
            _c("Christopher Kiekintveld", "artificial intelligence; security; game theory; decision making"),
        ),
    ),
    "Old Dominion University": FacultyRoster(
        "College of Sciences, Department of Computer Science",
        "https://faculty.pages.cs.odu.edu/",
        (
            _c("Mohammad GhasemiGol", "generative AI; AI red teaming; agentic systems; cybersecurity"),
            _c("Mahmoud Nazzal", "large language models; adversarial machine learning; software engineering"),
            _c("Rui Ning", "trustworthy AI; privacy; cyber-physical systems; security"),
            _c("Andrey Chernikov", "formal methods; parallel systems; verification; algorithms"),
        ),
    ),
    "Temple University": FacultyRoster(
        "College of Science and Technology, Department of Computer and Information Sciences",
        "https://cis.temple.edu/people/faculty/?s=cs",
        (
            _c("Yan Wang", "systems security; mobile security; trustworthy machine learning"),
            _c("Eduard Dragut", "natural language processing; information retrieval; web data"),
            _c("Anduo Wang", "networked systems; cybersecurity; formal reasoning"),
            _c("Slobodan Vucetic", "artificial intelligence; machine learning; trustworthy data science"),
        ),
    ),
    "University of Rhode Island": FacultyRoster(
        "College of Arts and Sciences, Department of Computer Science and Statistics",
        "https://web.uri.edu/cs/people/",
        (
            _c("Sarah Brown", "sociotechnical AI; algorithmic fairness; machine learning evaluation"),
            _c("Alina Jade Barnett", "interpretable machine learning; data science; trustworthy AI"),
            _c("Noah Daniels", "FAIR data; scientific metadata; reproducible computing"),
            _c("Shaun Wallace", "human-AI interaction; information retrieval; interactive systems"),
        ),
    ),
    "University of Nebraska at Omaha": FacultyRoster(
        "College of Information Science & Technology, Department of Computer Science",
        "https://www.unomaha.edu/college-of-information-science-and-technology/computer-science/about/faculty-staff.php",
        (
            _c("Harvey Siy", "software engineering; software evolution; mining software repositories"),
            _c("Victor Winter", "programming languages; program transformation; dependable software"),
            _c("Yuliya Lierler", "automated reasoning; logic programming; artificial intelligence"),
            _c("Mahadevan Subramaniam", "software engineering; distributed systems; dependable computing"),
        ),
    ),
    "University of Colorado Colorado Springs": FacultyRoster(
        "College of Engineering and Applied Science, Department of Computer Science",
        "https://eas.uccs.edu/departments/computer-science/directory/faculty",
        (
            _c("Shouhuai Xu", "cybersecurity dynamics; systems security; threat modeling"),
            _c("Yanyan Zhuang", "mobile and systems security; privacy; software security"),
            _c("Gedare Bloom", "embedded systems security; real-time systems; secure computing"),
            _c("Philip Brown", "cybersecurity; networked systems; resilient infrastructure"),
        ),
    ),
    "University of Massachusetts-Lowell": FacultyRoster(
        "Kennedy College of Sciences, Miner School of Computer & Information Sciences",
        "https://www.uml.edu/sciences/computer-science/people/faculty.aspx",
        (
            _c("Paul Downen", "programming languages; logic; compilation; formal methods"),
            _c("Xinwen Fu", "computer security; privacy; system and software security"),
            _c("Yimin (Ian) Chen", "security; privacy; trustworthy systems"),
            _c("Sashank Narain", "systems security; privacy; network measurement"),
        ),
    ),
    "University of Louisville": FacultyRoster(
        "J.B. Speed School of Engineering, Department of Computer Science and Engineering",
        "https://engineering.louisville.edu/cybercenter/homepage/faculty/",
        (
            _c("Wei Zhang", "hardware and systems security; compilers; real-time systems"),
            _c("Adrian P. Lauf", "cybersecurity; autonomous systems; Internet of Things"),
            _c("Adel S. Elmaghraby", "cybersecurity; multimedia; intelligent systems"),
            _c("Olfa Nasraoui", "data mining; trustworthy artificial intelligence; machine learning"),
        ),
    ),
    "University of New Hampshire-Main Campus": FacultyRoster(
        "College of Engineering and Physical Sciences, Department of Computer Science",
        "https://ceps.unh.edu/computer-science/faculty-staff-directory",
        (
            _c("Michel Charpentier", "formal specification and verification; distributed and parallel programming"),
            _c("Aleksey Charapko", "distributed systems; databases; fault-tolerant computing"),
            _c("Wheeler Ruml", "heuristic search; automated planning; artificial intelligence systems"),
            _c("Laura Dietz", "information retrieval; natural language processing; knowledge graphs"),
        ),
    ),
    "University of Missouri-Columbia": FacultyRoster(
        "David L. Payne Department of Electrical Engineering and Computer Science",
        "https://engineering.missouri.edu/departments/eecs/eecs-faculty/",
        (
            _c("Sean Patrick Goggins", "open-source software health; social computing; cybersecurity"),
            _c("Khaza Anuarul Hoque", "cybersecurity; cyber-physical systems security; formal verification"),
            _c("Prasad Calyam", "network and cloud security; cyberinfrastructure; distributed systems"),
            _c("Tanu Malik", "reproducibility; provenance; data systems; scientific workflows"),
        ),
    ),
    "University of Wisconsin-Milwaukee": FacultyRoster(
        "College of Engineering and Applied Science, Department of Computer Science",
        "https://uwm.edu/engineering/departments/computer-science/people-faculty-and-staff/",
        (
            _c("John Boyland", "programming languages; compilers; concurrency; formal logic"),
            _c("Jerald Thomas", "cybersecurity; secure intelligent systems; trustworthy computing"),
            _c("Zhen Zeng", "secure artificial intelligence; machine learning; trustworthy systems"),
            _c("Rohit Kate", "natural language processing; machine learning; information extraction"),
        ),
    ),
    "Illinois Institute of Technology": FacultyRoster(
        "College of Computing, Department of Computer Science",
        "https://www.iit.edu/directory/people?organization=116826&profile_type=21",
        (
            _c("Farzaneh Derakhshan", "programming languages; formal methods; software security"),
            _c("Binghui Wang", "trustworthy machine learning; security; privacy"),
            _c("Ioan Raicu", "distributed systems; high-performance computing; cloud computing"),
            _c("Stefan Muller", "parallel computing; programming languages; verification"),
        ),
    ),
    "New Jersey Institute of Technology": FacultyRoster(
        "Ying Wu College of Computing, Department of Computer Science",
        "https://cs.njit.edu/faculty",
        (
            _c("Iulian Neamtiu", "programming languages; software engineering; dependable systems; security"),
            _c("Reza Curtmola", "software security; privacy; cloud security; applied cryptography"),
            _c("Cristian Borcea", "distributed systems; mobile computing; cloud systems"),
            _c("Zephyr Yao", "systems security; mobile computing; trustworthy systems"),
        ),
    ),
    "University of Connecticut": FacultyRoster(
        "College of Engineering, School of Computing",
        "https://computing.engineering.uconn.edu/people/faculty/",
        (
            _c("Ghada Almashaqbeh", "cryptography; computer security; privacy; blockchain systems"),
            _c("Yuan Hong", "security; privacy; trustworthy artificial intelligence"),
            _c("Mohammad Khan", "distributed systems; cybersecurity; systems performance"),
            _c("Walter Krawec", "quantum security; cryptography; secure communications"),
        ),
    ),
    "Saint Mary’s University": FacultyRoster(
        "Department of Mathematics and Computing Science",
        "https://www.smu.ca/math-cs/faculty-and-staff.html",
        (
            _c("Pawan Lingras", "machine learning; data mining; soft computing"),
            _c("Stavros Konstantinidis", "formal languages; automata; error detection"),
            _c("Jiju Poovvancheri", "computer graphics; spatial computing; machine learning"),
            _c("Yasushi Akiyama", "human-computer interaction; multimedia; machine learning"),
        ),
    ),
    "Clarkson University": FacultyRoster(
        "Coulter School of Engineering & Applied Sciences, Department of Computer Science",
        "https://www.clarkson.edu/academics/schools-colleges/arts-sciences/departments/computer-science/faculty-staff",
        (
            _c("Daqing Hou", "software engineering; program analysis; cybersecurity; compilers"),
            _c("Jeanna Matthews", "systems accountability; security; cloud and distributed systems"),
            _c("Christopher Lynch", "automated reasoning; formal methods; protocol analysis"),
            _c("Alexis Maciel", "software systems; computer science education; applied computing"),
        ),
    ),
    "Florida Atlantic University": FacultyRoster(
        "College of Engineering and Computer Science, Department of Electrical Engineering and Computer Science",
        "https://www.fau.edu/engineering/eecs/research/research-interests/",
        (
            _c("Shihong Huang", "software architecture; empirical software engineering; software quality"),
            _c("George Sklivanitis", "software-defined networking; smart infrastructure; wireless systems"),
            _c("Mehrdad Nojoumian", "security; privacy; cryptography; trustworthy systems"),
            _c("Xingquan Zhu", "machine learning; data mining; security analytics; trustworthy AI"),
        ),
    ),
    "New Mexico Institute of Mining and Technology": FacultyRoster(
        "Department of Computer Science and Engineering",
        "https://www.cs.nmt.edu/faculty/",
        (
            _c("Subhasish Mazumdar", "distributed systems; databases; data management"),
            _c("Jun Zheng", "computer networks; wireless systems; network security"),
            _c("Hamdy Soliman", "cybersecurity; machine learning; dependable systems"),
            _c("Huixin Zhan", "software systems; data science; machine learning"),
        ),
    ),
    "Southern Illinois University-Carbondale": FacultyRoster(
        "College of Engineering, Computing, Technology, and Mathematics, School of Computing",
        "https://soc.siu.edu/our-people/",
        (
            _c("Ahmed Imteaj", "distributed machine learning; edge computing; trustworthy AI"),
            _c("Abdur Rahman Bin Shahid", "cybersecurity; machine learning; dependable computing"),
            _c("Ansuman Bhattacharya", "distributed systems; algorithms; networked computing"),
            _c("Zhong Chen", "software systems; data management; artificial intelligence"),
        ),
    ),
    "Wichita State University": FacultyRoster(
        "College of Engineering, School of Computing",
        "https://www.wichita.edu/profiles/academics/engineering/SoC/index.php",
        (
            _c("Souvika Sarkar", "software engineering; trustworthy AI; program analysis"),
            _c("Zhiyong Shan", "software engineering; software architecture; dependable systems"),
            _c("Rajiv Bagai", "computer security; algorithms; formal reasoning"),
            _c("Lokesh Das", "cybersecurity; machine learning; secure systems"),
        ),
    ),
    "Michigan Technological University": FacultyRoster(
        "College of Computing, Department of Computer Science",
        "https://www.mtu.edu/cs/department/people/",
        (
            _c("Yunlong Xing", "automated program repair; software testing; program analysis"),
            _c("Ali Ebnenasir", "formal methods; dependable systems; software verification"),
            _c("Charles Wallace", "software engineering; applied formal methods; trustworthy systems"),
            _c("Leo Ureel", "software engineering; AI-assisted programming; program comprehension"),
        ),
    ),
    "University of Tulsa": FacultyRoster(
        "College of Engineering and Computer Science, Tandy School of Computer Science",
        "https://utulsa.edu/departments/computer-science/",
        (
            _c("Yi Qian", "network security; wireless systems; cyber-physical infrastructure"),
            _c("Mauricio Papa", "critical-infrastructure security; industrial control systems; cyber-physical systems"),
            _c("Sujeet Shenoi", "digital forensics; critical-infrastructure security; cyber operations"),
            _c("Tyler Moore", "cybersecurity economics; measurement; dependable systems"),
        ),
    ),
    "Western University": FacultyRoster(
        "Faculty of Engineering, Department of Electrical and Computer Engineering",
        "https://www.eng.uwo.ca/electrical/people/faculty/index.html",
        (
            _c("Atrisha Sarkar", "multiagent systems; autonomous systems; software and societal systems"),
            _c("Katarina Grolinger", "cloud computing; data analytics; software engineering"),
            _c("Xianbin Wang", "wireless systems; network security; intelligent communications"),
            _c("Arash Reyhani-Masoleh", "hardware security; cryptography; dependable computing"),
        ),
    ),
}


# Institutions can expose serious routes through more than one department. Use
# an exact-program override where an institution-level roster would be wrong.
PROGRAM_FACULTY_ROSTERS: dict[str, FacultyRoster] = {
    "ca:dli:O19359011007:program:thesis-or-research-master-s:cybersecurity-engineering-masc": FacultyRoster(
        "Department of Cybersecurity and Intelligent Systems Engineering",
        "https://www.concordia.ca/ginacody/cybersecurity-intelligent-systems-eng/about/faculty-members.html",
        (
            _c("Amr Youssef", "cryptography; information security; privacy; secure systems"),
            _c("Lingyu Wang", "network security; attack graphs; SDN and NFV security"),
            _c("Suryadipta Majumdar", "cloud security; threat detection; security automation"),
            _c("Jeremy Clark", "applied cryptography; blockchain; secure voting systems"),
        ),
    ),
    "ca:dli:O19361109242:program:thesis-or-research-master-s:masc-in-electrical-and-computer-engineering": FacultyRoster(
        "Department of Electrical Engineering and Computer Science",
        "https://lassonde.yorku.ca/eecs/academics/graduate/graduate-faculty/",
        (
            _c("Zhen Ming (Jack) Jiang", "software performance; mining repositories; distributed-system debugging"),
            _c("Song Wang", "AI for software engineering; testing; static analysis"),
            _c("Marin Litoiu", "cloud systems; adaptive systems; performance engineering"),
            _c("Alvine Boaye Belle", "software assurance; assurance arguments; requirements debt"),
        ),
    ),
}
