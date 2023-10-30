import os, csv, json

def txt_to_tsv(file_path, output_name):
    """
    columns: id, author_info, story, Q1, A1, A2, A3, A5, Q2 ...
    """

    output_rows = []

    with open(file_path, "r") as handle:
        text = handle.read()
        sections = text.split("***************************************************")
        for s in sections:
            lines = s.split("\n")
            lines = [l for l in lines if l.strip() != ""]

            if len(lines) > 1:
                #print("~~*~*~*~*~**~*~*~*~**~")

                id = lines[0].replace(" ", "")
                author_info = lines[1] + lines[2]
                author_info = author_info.replace(" ", "")

                #print(id)
                #print(author_info)

                story_start = 3
                story_end = 0
                #identify index of line that starts with "1:", as this is where questions begin
                for i, l in enumerate(lines):
                    if l.startswith("1"):
                        story_end = i

                if story_end == 3:
                    story = lines[3]
                    story = story.strip("\n")
                else:
                    story = lines[story_start:story_end]
                    story = [l.strip("\n") for l in story]
                    story = (' ').join(story)

                #print(story)

                remaining_rows = lines[story_end:]

                #print(remaining_rows)

                output = [id, author_info, story] + remaining_rows
                #print(len(output))

                output_rows.append(output)
                # if isinstance(story, list):
                #     if len(story) < 2:
                #         print(story)
                #
                #         print("--------")
                #         print(lines)
                #         print(f" >>>> {story_end}")
                # if len(story) == 0 :
                #     print(lines)
                #     print(f">>>>>>>> {lines[3]}")
                #     print(f" ##### {story_end}")
                #     print(lines[story_end+1])

    with open(f"MCTest/creole/{output_name}", "w") as tsvfile:
        reader = csv.writer(tsvfile, delimiter='\t')
        for row in output_rows:
            reader.writerow(row)



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
    answers_path = f"MCTest/mc160.dev.ans"

    q_dict = {}
     # q_dict: dict of dicts = 
     #    {id: 
     #        {'story': '...', 
     #         'questions': [[the question, a1, a2, a3, a4], [q2], [q3], [q4]],
     #         'answers': [A, B, C, A]
     #        } 

    examples = []

    with open(questions_path, newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for i, row in enumerate(reader):
            q_id = row[0]
            story = row[2]
            questions = row[3:]
            organized_questions = []
            q_set = []
            for q in questions:
                q = q.lstrip(" ") #get rid of any trailing whitespace
                #FIXME: only works for English | Hardcoded for Creoles now
                #if q.startswith('one:') or q.startswith('multiple:'): #English
                if q[0] in ['1', '2', '3', '4']: #Haitian or Mauritian
                    q_set = [] # start of new question
                    q_set.append(q)
                else:
                    #FIXME: asterisk `*` for correct answer needs to be removed for Haitian and Mauritian | Hardcoded
                    if q.startswith("*"):
                        q = q[1:] #cut off the asterisk
                    q_set.append(q)
                if len(q_set) == 5:
                    organized_questions.append(q_set)

            try:
                assert len(organized_questions) == 4
            except Exception as e:
                print(e)
                print(organized_questions)
                print(len(organized_questions))
                print("------")
                print(row)
                print("--------")

            assert len(organized_questions) == 4 #every story has 4 questions

            for qa in organized_questions:
                assert len(qa) == 5 #question + 4 multiple choice

            q_dict[q_id] = {'story': story, 'questions': organized_questions}

    with open(answers_path, newline='') as ansfile:
        reader = csv.reader(ansfile, delimiter='\t')
        for i, row in enumerate(reader):
            #q_id = f"{split}.{i}" #FIXME: this is English only | Hardcoded
            q_id = f"Story:mc160.dev.{i}" #Haitian and Marutian are like: Story:mc160.dev.0
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

            #Mauritian: "1: one:"
            #Haitian: "4: youn :"
            #print(question_text)

            #TODO: strip off the beginning number and colon, until it starts with "one"/"youn" or "multiple"/"multipil"
            #remove number
            question_text = question_text[1:]
            #remove leading whitespace
            question_text = question_text.lstrip(' ')
            #remove colon
            question_text = question_text.lstrip(':')
            #remove leading whitespace
            question_text = question_text.lstrip(' ')

            #print(question_text)

            if question_text.startswith("one"):
                cleaned = (question_text).strip("one")
                cleaned = cleaned.lstrip(' ')
                cleaned = cleaned.lstrip(':')
                cleaned = cleaned.lstrip(' ')
                q_type = "one"
            elif question_text.startswith("youn"):
                cleaned = (question_text).strip("youn")
                cleaned = cleaned.lstrip(' ')
                cleaned = cleaned.lstrip(':')
                cleaned = cleaned.lstrip(' ')
                q_type = "one"
            elif question_text.startswith("multipil"):
                cleaned = (question_text).strip("multipil")
                cleaned = cleaned.lstrip(' ')
                cleaned = cleaned.lstrip(':')
                cleaned = cleaned.lstrip(' ')
                q_type = "multiple"
            else:
                cleaned = (question_text).strip("multiple")
                cleaned = cleaned.lstrip(' ')
                cleaned = cleaned.lstrip(':')
                cleaned = cleaned.lstrip(' ')
                q_type = "multiple"

            """
            # ENGLISH ONLY 
            if question_text.startswith("one: "):
                cleaned = (question_text).strip("one: ")#("one: ").strip(question_text)
                q_type = "one"
            else:
                cleaned = (question_text).strip("multiple: ")#("multiple: ").strip(question_text)
                q_type = "multiple"
            """

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

            #print(e_dict)
            #exit(333)

            examples.append(e_dict) 
            j+=1
            question_counter +=1

    print(f"* {story_counter} stories ...")
    print(f"* {question_counter} questions ...")


    with open(f"{path}/{split}.json", "w", encoding='utf-8') as out:
        for ex in examples:
            json.dump(ex, out)
            out.write('\n')



def write_eng_to_json(path, split):
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


# txt_to_tsv("MCTest/creole/mc160.dev.kreyol1.txt", "keyol1.tsv")
# txt_to_tsv("MCTest/creole/mc160.dev.kreyol2_localized.txt", "kreyol2_localized.tsv")
# txt_to_tsv("MCTest/creole/mc160.dev.mauritian.txt", "mauritian.tsv")

#write_to_json("MCTest/creole", "mc160.dev.kreyol1")
#write_to_json("MCTest/creole", "mc160.dev.kreyol2_localized")
#write_to_json("MCTest/creole", "mc160.dev.mauritian")

#write_to_json("MCTest", "mc500.train")
#write_eng_to_json("MCTest", "mc160.test")
#write_eng_to_json("MCTest", "mc500.test")
#write_eng_to_json("MCTest", "mc160.train")
write_eng_to_json("MCTest", "mc500.dev")
