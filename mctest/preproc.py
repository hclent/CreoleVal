import argparse
from pudb import set_trace
import os, csv, json

"""
Example tsv row

mc160.dev.0	Author: 2670363255;Work Time(s): 1446	It was Jessie Bear's birthday. She was having a party.  She asked her two best friends to come to the party.  She made a big cake, and hung up some balloons. Soon her friend Lion came over. Then her friend Tiger came over. Lion and Tiger brought presents with them. Jessie hugged her friends. She asked them if they would like to have cake.  Yes! said Lion. Yes yes! said Tiger. Jessie cut the cake, and they all ate it together. Then Jessie opened her presents. She got a new jump rope and a fun game.  She asked Lion and Tiger to play the game with her. The friends played and played. They all had a good time. Soon it was time for the party to be over. Lion and Tiger hugged Jessie and said goodbye to her.  Thanks for a great birthday! Jessie Bear told her two best friends.	one: Who was having a birthday?	Jessie Bear	no one	Lion	Tiger	multiple: Who didn't come to the party?	Lion	Tiger	Snake	Jessie Bear	multiple: How did Jessie get ready for the party?	made cake and juice.	made cake and hung balloons.	made juice and cookies.	made juice and hung balloons.	one: How many friends came to Jessie's party?	one	two	six	four

"""


#TODO! 
def txt_to_tsv(file_path):
	pass


def write_to_json(path, split):
    """
    Input:
     path: str = the/path/to/your/data/dir
     split: str = mctest.train

    Output: 
     examples = list[dict] 
    """

    full_path = os.path.join(path, split)
    questions_path = f"{full_path}.tsv"
    answers_path = f"{full_path}.ans"

    q_dict = {}
     # q_dict: dict of dicts = 
     #    {id: 
     #        {'story': '...', 
     #         'questions': [[the question, a1, a2, a3, a4], [q2], [q3], [q4]],
     #         'answers': [A, B, C, A]
     #        } 

    examples = []

    with open(questions_path, newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for i, row in enumerate(reader):
            q_id = row[0]
            story = row[2]
            questions = row[3:]
            organized_questions = []
            q_set = []
            for q in questions:
                if q.startswith('one:') or q.startswith('multiple:'):
                    q_set = [] # start of new question
                    q_set.append(q)
                else:
                    q_set.append(q)
                if len(q_set) == 5:
                    organized_questions.append(q_set)

            assert len(organized_questions) == 4 #every story has 4 questions

            for qa in organized_questions:
                assert len(qa) == 5 #question + 4 multiple choice

            q_dict[q_id] = {'story': story, 'questions': organized_questions}

    with open(answers_path, newline='') as ansfile:
        reader = csv.reader(ansfile, delimiter='\t')
        for i, row in enumerate(reader):
            q_id = f"{split}.{i}"
            q_dict[q_id].update({'answers': row})

    story_counter = 0
    question_counter = 0 

    for indx, mc_dict in q_dict.items():
        story_counter += 1
        story = mc_dict['story']
        j = 1
        for q, a in zip(mc_dict['questions'], mc_dict['answers']):
            lut = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            choices = q[1:]
            a_to_index = lut[a]
            text_answer = choices[a_to_index]

            question_text = q[0]
            if question_text.startswith("one: "):
                cleaned = (question_text).strip("one: ")#("one: ").strip(question_text)
                q_type = "one"
            else:
                cleaned = (question_text).strip("multiple: ")#("multiple: ").strip(question_text)
                q_type = "multiple"

            e_dict = {
                'story': story,
                'story_id': str(indx),
                'question_id': str(j), 
                'question': cleaned,
                'q_type': q_type,
                'choices': choices,
                'answer': a, #ABCD
                'text_answer': text_answer, #the text itself
                'label': str(a_to_index), #FIXME: i'm having to cast this to an int later
            }
            examples.append(e_dict) 
            j+=1
            question_counter +=1

    print(f"* {story_counter} stories ...")
    print(f"* {question_counter} questions ...")


    with open(f"{path}/as_json/{split}.json", "w") as out:
        for ex in examples:
            json.dump(ex, out)
            out.write('\n')


#write_to_json(data_path, split)

