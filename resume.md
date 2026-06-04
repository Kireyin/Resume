---
header-includes: |
  ```{=latex}
  % ---- colours --------------------------------------------------------------
  \usepackage{xcolor}
  \definecolor{accent}{HTML}{1F4E79}   % deep navy

  % ---- real font cuts (override CI's -V mainfont; header-includes wins) ------
  \setmainfont{SF-Compact-Text}[
    Path = fonts/,
    Extension = .otf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-RegularItalic ]

  % ---- section headers (## -> \subsection): uppercase, accent, rule below ----
  \usepackage{titlesec}
  \titleformat{\subsection}
    {\normalfont\large\bfseries\color{accent}}{}{0em}{\MakeUppercase}
    [{\color{accent!35}\titlerule[1pt]}]
  \titlespacing*{\subsection}{0pt}{2.2ex plus .3ex minus .2ex}{1.0ex}

  % ---- entry headers (### -> \subsubsection): bold left, date flush right -----
  \titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{}{0em}{}
  \titlespacing*{\subsubsection}{0pt}{1.6ex plus .2ex}{0.3ex}
  \newcommand{\datestamp}[1]{{\normalfont\itshape\small\color{black!55}#1}}

  % ---- name / contact banner ------------------------------------------------
  \newcommand{\resumeheader}[3]{%
    \begin{center}
      {\fontsize{24}{28}\selectfont\bfseries\color{accent}#1}\\[3pt]
      {\large #2}\\[5pt]
      {\small #3}
    \end{center}
    \vspace{2.5ex}}

  % ---- lists: accent bullets, tight, indented -------------------------------
  \usepackage{enumitem}
  \setlist[itemize]{leftmargin=1.4em, topsep=2pt, label=\textcolor{accent}{\textbullet}}
  \AtBeginDocument{\renewcommand{\tightlist}{%
    \setlength{\itemsep}{1.5pt}\setlength{\parskip}{0pt}}}

  % ---- page footer: name/title/linkedin reminder + "page X of Y" -------------
  \usepackage{lastpage}
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \fancyhf{}                          % clear default header & footer
  \renewcommand{\headrulewidth}{0pt}  % no header rule
  \renewcommand{\footrulewidth}{0.4pt}
  \makeatletter                       % colour the footer rule to match section rules
  \renewcommand{\footrule}{%
    \vskip-\footruleskip\vskip-\footrulewidth
    {\color{accent!35}\hrule\@width\headwidth\@height\footrulewidth}%
    \vskip\footruleskip}
  \makeatother
  \fancyfoot[L]{\footnotesize\color{black!55}Alexandre Brispot - Senior iOS Engineer · \href{https://www.linkedin.com/in/kireyin/}{linkedin.com/in/kireyin}}
  \fancyfoot[R]{\footnotesize\color{black!55}\thepage\ of \pageref{LastPage}}

  % ---- misc -----------------------------------------------------------------
  \usepackage{needspace}   % keep an entry from splitting across a page break
  \setcounter{secnumdepth}{0}
  \setlength{\parindent}{0pt}
  \AtBeginDocument{\hypersetup{colorlinks=true, allcolors=accent}}
  ```
---

```{=latex}
\resumeheader
  {Alexandre Brispot}
  {Senior iOS Engineer | Swift | 10+ years mobile experience | Epitech}
  {\href{https://www.linkedin.com/in/kireyin/}{linkedin.com/in/kireyin}}
```

```{=latex}
{\setlength{\parindent}{1.5em}%
Senior iOS Engineer leading cross-platform SDK development at DataDome, serving hundreds of millions of devices across iOS, Android, React Native, Flutter, and KMM. 10+ years of experience shipping production mobile apps, with deep expertise in Swift and iOS SDK architecture. Open to Senior/Lead iOS roles, remote preferred.\par}
```

## Experience

### DataDome - Senior iOS Software Engineer \hfill \datestamp{Sept 2022 - Present}
*Amiens, Hauts-de-France, France*

- Lead a team of 3 mobile developers, owning the full lifecycle of 14 SDKs across iOS, Android, React Native, Flutter, and KMM for DataDome's bot protection platform, used by clients such as TripAdvisor, SoundCloud, and The New York Times
- Architect and maintain the iOS SDK in Swift (+ others in their respective technologies), integrated by enterprise clients for real-time bot and fraud detection
- Reduced customer support tickets by 50% through improved SDK documentation, simpler APIs, and comprehensive unit and E2E test coverage
- Drive code reviews, technical decisions, and release planning for the mobile SDK team
- Implement CI/CD pipelines ensuring reliable delivery across all platforms

### SightCall - Senior iOS Engineer \hfill \datestamp{March 2021 - Sept 2022}
*Boulogne-Billancourt, Île-de-France, France*

- Developed the iOS SDK for SightCall's AR-powered remote visual assistance platform, used by enterprise clients such as Sony, Ford, and GE Healthcare
- Built real-time AR annotation features with ARKit, allowing users to place 3D markers, drawings, and measurements on live video streams
- Integrated Core ML for on-device object detection and annotation during live video sessions
- Migrated the legacy Objective-C codebase to Swift, modernizing the SDK architecture
- Built CI/CD pipelines with Bitrise, automating the release process

### Mention - iOS Engineer \hfill \datestamp{Sept 2015 - March 2021}
*Paris, Île-de-France, France*

- Sole iOS developer responsible for the full Mention iOS application
- Led complete migration from Objective-C to Swift, improving code maintainability and developer velocity
- Extracted business logic into a reusable SDK, separating front-end and business layers to prepare for future applications
- Built a custom GraphQL implementation to avoid Apollo's heavy code generation, alongside REST APIs and real-time WebSocket features
- Reduced app crash rate by 30% through systematic debugging, memory management improvements, and crash reporting analysis
- Recruited the Android developer, designed Kotlin technical challenges, and mentored them on mobile best practices and architecture

```{=latex}
\needspace{9\baselineskip}
```

### RotorMatch - Co-Founder & Software Engineer (part-time) \hfill \datestamp{Feb 2016 - Jan 2020}
*Paris, Île-de-France, France*

- Co-founded a drone racing event technology company
- Built a race timing system: an embedded system for signal capture, a Swift app for data reading and backend sync (custom UDP library), and a web app for the race control center
- Live-streamed to multiple platforms including our own RotorTV
- Event planning platform, ticket booking platform
- NFC/RFID integration and reverse engineering of custom protocols

## Education

### EPITECH - European Institute of Technology \hfill \datestamp{2010 - 2015}
Master's degree, Software Engineering

### 北京交通大学 (Beijing Jiaotong University) \hfill \datestamp{2013 - 2014}
M1, Software Engineering

### HEC Paris \hfill \datestamp{2013}
Digital Innovation for Business Certificate - E-commerce · Management · Lean Startup

## Skills

- Swift, Objective-C, iOS, SwiftUI, UIKit, ARKit, Core ML
- SDK Development, Technical Documentation
- Android, Flutter, React Native, KMM
- CI/CD, Team Leadership, Mentoring

## Languages

- French (Native)
- English (Professional Working)
