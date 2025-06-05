MOCK_TEST_DATA = {
    'toeic': {
        'business': {
            'reading': [
                {
                    'id': 'r1',
                    'text': """
                    The annual company retreat will be held at Mountain View Resort from July 15-17. All employees are expected to attend the main sessions, which will focus on team-building and strategic planning for the upcoming fiscal year. Department heads should prepare a 10-minute presentation highlighting their team's achievements and goals. 
                    
                    Accommodation will be provided, but employees must register by June 15 to secure a room. Those with dietary restrictions should notify Human Resources by July 1. Transportation will depart from the company headquarters at 8:00 AM on July 15.
                    """,
                    'questions': [
                        {
                            'question': 'What is the main purpose of the company retreat?',
                            'options': ['To provide a vacation for employees', 'To conduct performance reviews', 'To focus on team-building and strategic planning', 'To interview new candidates'],
                            'correct': 2
                        },
                        {
                            'question': 'When is the deadline for room registration?',
                            'options': ['July 1', 'June 15', 'July 15', 'July 17'],
                            'correct': 1
                        },
                    ]
                },
                {
                    'id': 'r2',
                    'text': """
                    On April 14, 1912, the Titanic, operated by the White Star Line, embarked on its maiden voyage. The company had promoted the ship as 'unsinkable,' creating a sense of overconfidence among its leadership. Captain Smith, under pressure to maintain the ship's speed of 22 knots to meet a tight schedule, ignored multiple ice warnings. At 11:39 p.m., lookouts Frederick Fleet and Reginald Lee reported an iceberg, but the ship collided with it 37 seconds later, leading to a catastrophic failure. The lack of binoculars, left behind in Southampton due to a last-minute officer change, was cited as a contributing factor by Fleet during an inquiry. Additionally, the Titanic carried lifeboats for only 1,178 of its 2,222 passengers, exceeding the Board of Trade's requirement of 1,060 but still insufficient. A scheduled lifeboat drill was cancelled to allow passengers to attend church, further compounding the disaster's impact.
                    """,
                    'questions': [
                        {
                            'question': 'Why did Captain Smith maintain the Titanic’s speed despite ice warnings?',
                            'options': ['To test the ship’s capabilities', 'To meet a tight schedule', 'Because he was unaware of the warnings', 'To avoid delays in Southampton'],
                            'correct': 1
                        },
                        {
                            'question': 'What was one reason the Titanic lacked sufficient lifeboats?',
                            'options': ['The company ignored all regulations', 'Regulations were based on ship size, not passenger numbers', 'The lifeboats were damaged before the voyage', 'The ship was designed for short trips'],
                            'correct': 1
                        },
                        {
                            'question': 'What contributed to the lookouts’ inability to spot the iceberg sooner?',
                            'options': ['The ship’s lights were too bright', 'They lacked binoculars due to an officer change', 'They were distracted by passengers', 'The weather was too foggy'],
                            'correct': 1
                        },
                    ]
                },
                {
                    'id': 'r3',
                    'text': """
                    The film industry has increasingly adopted 3-D technology to boost box office sales. Avatar, released in December 2009, became the highest-grossing film ever, earning over US$2 billion worldwide, largely due to its 3-D visual effects. An analyst at Exhibitor Relations noted that Avatar's success has solidified 3-D as a key promotional tool for blockbuster films, driving the construction of 3-D venues. However, critics like Roger Ebert argue that 3-D technology dims the viewing experience due to special glasses and shifts focus away from storytelling to special effects, potentially targeting a younger audience. Additionally, ophthalmologists warn that 3-D can cause eyestrain and nausea in 15% of viewers due to minor eye imbalances.
                    """,
                    'questions': [
                        {
                            'question': 'What has been a major business impact of Avatar’s success?',
                            'options': ['Increased focus on 2-D films', 'Construction of more 3-D venues', 'Reduction in ticket prices', 'Closure of traditional theaters'],
                            'correct': 1
                        },
                        {
                            'question': 'What is one criticism of 3-D technology in filmmaking?',
                            'options': ['It increases production costs too much', 'It shifts focus away from storytelling', 'It requires larger screens', 'It is only suitable for documentaries'],
                            'correct': 1
                        },
                        {
                            'question': 'What health concern is associated with 3-D films?',
                            'options': ['Hearing loss from loud sound effects', 'Eyestrain and nausea in some viewers', 'Increased risk of motion sickness', 'Allergic reactions to 3-D glasses'],
                            'correct': 1
                        },
                    ]
                },
                {
                    'id': 'r4',
                    'text': """
                    Horizon Enterprises announced a new sustainability initiative at their annual conference on June 1, 2025. The initiative aims to reduce the company’s carbon footprint by 30% over the next five years through energy-efficient practices and renewable energy investments. Employees will participate in mandatory training sessions starting July 2025 to ensure compliance with the new policies. The CEO emphasized that this initiative aligns with global trends and customer expectations for greener business practices.
                    """,
                    'questions': [
                        {
                            'question': 'What is the goal of Horizon Enterprises’ new initiative?',
                            'options': ['To increase profits by 30%', 'To reduce the carbon footprint by 30%', 'To hire more employees', 'To expand internationally'],
                            'correct': 1
                        },
                        {
                            'question': 'When will the training sessions for employees begin?',
                            'options': ['June 2025', 'July 2025', 'August 2025', 'September 2025'],
                            'correct': 1
                        },
                    ]
                },
                {
                    'id': 'r5',
                    'text': """
                    TechNova announced the release of its latest software update, Version 3.0, designed to enhance user security and performance. The update will be available for download starting June 20. Users are advised to back up their data before installing the new version.
                    
                    A webinar to demonstrate the new features is scheduled for June 25. Registration is open until June 22 via the company website.
                    """,
                    'questions': [
                        {
                            'question': 'What is the purpose of the software update?',
                            'options': ['To reduce company costs', 'To enhance user security and performance', 'To replace hardware', 'To train employees'],
                            'correct': 1
                        },
                        {
                            'question': 'When can users download the update?',
                            'options': ['June 20', 'June 22', 'June 25', 'June 30'],
                            'correct': 0
                        },
                    ]
                },
                # More reading sections...
            ],
            'grammar': [
                {
                    'id': 'g1',
                    'sentence': 'The meeting will not take more than an hour, ____ you prepare your presentation in advance.',
                    'options': ['while', 'in spite of', 'as long as', 'even if', 'until'],
                    'correct': 2  
                },
                {
                    'id': 'g2',
                    'sentence': 'I ____ buy a new laptop for the presentation. The old one worked perfectly after all.',
                    'options': ['should not', 'had to', 'needn’t', 'didn’t have to', 'would have to'],
                    'correct': 3  
                },
                {
                    'id': 'g3',
                    'sentence': 'The manager is ____ strict ____ the CEO when it comes to deadlines.',
                    'options': ['so / as', 'so / than', 'as / as', 'as / than', 'more / than'],
                    'correct': 2  # Answer: as / as
                },

                {
                    'id': 'g4',
                    'sentence': 'The new policy ____ compulsory for all departments last year.',
                    'options': ['used to be', 'would be', 'has', 'has been'],
                    'correct': 0  # Answer: used to be
                },
                {
                    'id': 'g5',
                    'sentence': 'The CEO ____ a speech when the projector suddenly failed.',
                    'options': ['was giving', 'gives', 'was give', 'has giving'],
                    'correct': 0  # Answer: was giving
                },
                {
                    'id': 'g6',
                    'sentence': 'There ____ enough budget for the marketing campaign this quarter.',
                    'options': ['isn’t some', 'isn’t any', 'any', 'none'],
                    'correct': 1  # Answer: isn’t any
                },
                {
                    'id': 'g7',
                    'sentence': 'More and more companies ____ sustainable practices every year.',
                    'options': ['are adopting', 'adopting', 'will adopting', 'adopt'],
                    'correct': 0  # Answer: are adopting
                },
                {
                    'id': 'g8',
                    'sentence': 'The project plan ____ by the team last week.',
                    'options': ['was finalized', 'finalized', 'is finalizing', 'has finalized'],
                    'correct': 0  # Answer: was finalized
                },
                {
                    'id': 'g9',
                    'sentence': 'If the company grows, we ____ hire more staff to support the expansion.',
                    'options': ['will', 'be able to', 'will be able to', 'will able to'],
                    'correct': 2  # Answer: will be able to
                },
                {
                    'id': 'g10',
                    'sentence': 'The report ____ received by the board early this morning.',
                    'options': ['were', 'was', 'will have', 'has been'],
                    'correct': 1  # Answer: was
                },
                # More grammar questions...
            ],
            'vocabulary': [
                {
                    'id': 'v1',
                    'word': 'unreasonable',
                    'question': 'It seems ____ to cancel the meeting without prior notice.',
                    'options': ['unbelievable', 'untrustworthy', 'probable', 'unreasonable', 'impossible'],
                    'correct': 3  # Answer: unreasonable
                },
                {
                    'id': 'v2',
                    'word': 'principal',
                    'question': 'My ____ objection to the proposal is its high cost.',
                    'options': ['primarily', 'principle', 'priority', 'privileged', 'principal'],
                    'correct': 4  # Answer: principal
                },
                {
                    'id': 'v3',
                    'word': 'afford',
                    'question': 'You could ____ to be a little more cooperative, couldn’t you?',
                    'options': ['effort', 'comfort', 'support', 'please', 'afford'],
                    'correct': 4  # Answer: afford
                },
                {
                    'id': 'v4',
                    'word': 'injustice',
                    'question': 'It was a gross ____ to reject her application without review.',
                    'options': ['impartiality', 'injustice', 'fairness', 'penalty', 'invasiveness'],
                    'correct': 1  # Answer: injustice
                },
                {
                    'id': 'v5',
                    'word': 'endorse',
                    'question': 'The board refused to ____ the new policy due to budget concerns.',
                    'options': ['praise', 'assess', 'avoid', 'endorse', 'advocate'],
                    'correct': 3  # Answer: endorse
                },
                {
                    'id': 'v6',
                    'word': 'foretell',
                    'question': 'It is impossible to ____ the exact outcome of the merger.',
                    'options': ['forearm', 'forbid', 'forsake', 'fortify', 'foretell'],
                    'correct': 4  # Answer: foretell
                },
                {
                    'id': 'v7',
                    'word': 'outnumber',
                    'question': 'In our company, full-time employees ____ part-time staff by three to one.',
                    'options': ['outlive', 'outdo', 'outshine', 'outnumber', 'outclass'],
                    'correct': 3  # Answer: outnumber
                },
                {
                    'id': 'v8',
                    'word': 'overcome',
                    'question': 'The team must ____ these challenges before launching the product.',
                    'options': ['conclude', 'overcome', 'aggravate', 'endanger', 'guarantee'],
                    'correct': 1  # Answer: overcome
                },
                {
                    'id': 'v9',
                    'word': 'nevertheless',
                    'question': 'The project faced delays; ____, it was completed on budget.',
                    'options': ['therefore', 'accordingly', 'nevertheless', 'consequently', 'otherwise'],
                    'correct': 2  # Answer: nevertheless
                },
                {
                    'id': 'v10',
                    'word': 'irrelevant',
                    'question': 'Your comments are ____ to the current discussion.',
                    'options': ['irrelevant', 'resentful', 'rebellious', 'scornful', 'enormous'],
                    'correct': 0  #Answer: irrelevant
                },
            ]
        },
        # More topics...
    },
    'cambridge': {
        # Similar structure to TOEIC but with different content...
    }
}

# Add more test data here for different topics and test types
# For example:
MOCK_TEST_DATA['toeic']['technology'] = {
    'reading': [
        # Technology-related reading sections
    ],
    'grammar': [
        # Technology-related grammar questions
    ],
    'vocabulary': [
        # Technology-related vocabulary questions
    ]
}

# Add Cambridge test data
MOCK_TEST_DATA['cambridge']['business'] = {
    'reading': [
        # Cambridge business reading sections
    ],
    'grammar': [
        # Cambridge business grammar questions
    ],
    'vocabulary': [
        # Cambridge business vocabulary questions
    ]
}

# ...and so on for other topics