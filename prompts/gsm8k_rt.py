vote_prompt = ''' Given a question and a couple of decomposed manageable sub-questions, your task is to choose the next best sub-question and sub-answer pair among the given candidates. The goal for each sub-question is to summarize existing information, determine the new information required, and then articulate a logical and useful sub-question that brings you closer to the final answer. Analyze each sub-question sub-answer candidate pair in detail and compare them to decide which choice is the most promising to be the next step to solve the question. After analyzing each choice in detail and comparing them, conclude your final choice with \"Therefore, the best choice is\"

Question 1: Four years ago, Kody was only half as old as Mohamed. If Mohamed is currently twice as 30 years old, how old is Kody?

Choice 1:
Question 1.1: We start by understanding that four years ago, Kody's age was half that of Mohamed's, and currently, Mohamed is twice 30 years old. To proceed, we need Mohamed's current age. Therefore, the next useful subquestion we need to solve is: What is Mohamed's current age?
Answer 1.1: Since Mohamed is currently twice 30, we calculate 2 * 30 = 60. Thus, Mohamed is 60 years old now. The answer is 60.
Question 1.2: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?
Answer 1.2: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.
Question 1.3: Knowing that Mohamed was 56 years old four years ago enables us to figure out Kody's age at that time, given that Kody was half as old as Mohamed. Therefore, the next useful subquestion we need to solve is: How old was Kody four years ago?
Answer 1.3: If Kody was half as old as Mohamed four years ago, then 56 / 2 = 28. Kody was 28 years old four years ago. The answer is 28.

Choice 2:
Question 1.1: We start by understanding that four years ago, Kody's age was half that of Mohamed's, and currently, Mohamed is twice 30 years old. To proceed, we need Mohamed's current age. Therefore, the next useful subquestion we need to solve is: What is Mohamed's current age?
Answer 1.1: Since Mohamed is currently twice 30, we calculate 2 * 30 = 60. Thus, Mohamed is 60 years old now. The answer is 60.
Question 1.2: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?
Answer 1.2: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.
Question 1.3: Given that Mohamed is currently 60 years old and was 56 years old four years ago, we can calculate the number of years he has lived. Therefore, the next useful subquestion we need to solve is: How many years has Mohamed lived?
Answer 1.3: We can calculate the number of years Mohamed has lived by subtracting his age four years ago from his current age: 60 - 56 = 4. Mohamed has lived for 4 years. The answer is 4.

Choice 3:
Question 1.1: We start by understanding that four years ago, Kody's age was half that of Mohamed's, and currently, Mohamed is twice 30 years old. To proceed, we need Mohamed's current age. Therefore, the next useful subquestion we need to solve is: What is Mohamed's current age?
Answer 1.1: Since Mohamed is currently twice 30, we calculate 2 * 30 = 60. Thus, Mohamed is 60 years old now. The answer is 60.
Question 1.2: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?
Answer 1.2: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.
Question 1.3: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?
Answer 1.3: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.

Response: Let's think step by step. Choice 1 proves most valuable for advancing toward the main question about Kody's age. It effectively uses existing data, calculating Kody's age four years ago as half of Mohamed's age at that time (28 years). This step is crucial in determining Kody's current age, directly applying the relationship stated in the problem. Conversely, Choice 2 offers trivial information about the time elapsed, irrelevant to Kody's age, and Choice 3 redundantly revisits a previously solved sub-question. Therefore, the best choice is 1.

Question 2: On a moonless night, three fireflies danced in the evening breeze. They were joined by four less than a dozen more fireflies before two of the fireflies flew away. How many fireflies remained?

Choice 1:
Question 2.1: We start with the initial information that three fireflies were present, and then they were joined by four less than a dozen more fireflies. To proceed, we need to calculate the total number of fireflies that joined. Therefore, the next useful subquestion we need to solve is: How many fireflies joined the initial three?
Answer 2.1: A dozen fireflies minus four gives us 12 - 4 = 8 fireflies that joined the initial three. The answer is 8.
Question 2.2: With the knowledge that 8 fireflies joined the initial 3, we next need to find out the total number of fireflies before any of them flew away. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?
Answer 2.2: The total number of fireflies before any flew away can be found by adding the initial three to the eight that joined, which gives us 3 + 8 = 11 fireflies. The answer is 11.
Question 2.3: Understanding that 11 fireflies were gathered before any left the scene, we now need to find out the change in their number after two decided to leave. Therefore, the next useful subquestion we need to solve is: How many fireflies left the scene?
Answer 2.3: Since it's already established that two fireflies flew away, the answer is 2.

Choice 2:
Question 2.1: We start with the initial information that three fireflies were present, and then they were joined by four less than a dozen more fireflies. To proceed, we need to calculate the total number of fireflies that joined. Therefore, the next useful subquestion we need to solve is: How many fireflies joined the initial three?
Answer 2.1: A dozen fireflies minus four gives us 12 - 4 = 8 fireflies that joined the initial three. The answer is 8.
Question 2.2: With the knowledge that 8 fireflies joined the initial 3, we next need to find out the total number of fireflies before any of them flew away. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?
Answer 2.2: The total number of fireflies before any flew away can be found by adding the initial three to the eight that joined, which gives us 3 + 8 = 11 fireflies. The answer is 11.
Question 2.3: With the calculation that there were initially 11 fireflies, we need to determine the changes in their number to understand the dynamic of their gathering. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?
Answer 2.3: The total number of fireflies before any flew away was 11, as calculated by adding the initial three to the eight that joined. The answer is 11.

Choice 3:
Question 2.1: We start with the initial information that three fireflies were present, and then they were joined by four less than a dozen more fireflies. To proceed, we need to calculate the total number of fireflies that joined. Therefore, the next useful subquestion we need to solve is: How many fireflies joined the initial three?
Answer 2.1: A dozen fireflies minus four gives us 12 - 4 = 8 fireflies that joined the initial three. The answer is 8.
Question 2.2: With the knowledge that 8 fireflies joined the initial 3, we next need to find out the total number of fireflies before any of them flew away. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?
Answer 2.2: The total number of fireflies before any flew away can be found by adding the initial three to the eight that joined, which gives us 3 + 8 = 11 fireflies. The answer is 11.
Question 2.3: Knowing that there were 11 fireflies before two flew away gives us the information needed to determine how many remained. Now we can answer the question: How many fireflies remained after two flew away?
Answer 2.3: From the 11 fireflies, if two flew away, we subtract two from the total, which gives us 11 - 2 = 9 fireflies remaining. The answer is 9.

Response: Let's think step by step. Choice 3 proves most relevant as it calculates the remaining number of fireflies after two flew away, directly addressing the main question. It uses the previously determined total of 11 fireflies effectively to reach the answer of 9 remaining fireflies. Choice 1 merely repeats known information about two fireflies leaving, adding no new insight. Choice 2 redundantly calculates the total number of fireflies before two left, an answer previously established. Therefore, the best choice is 3.

Question 3: {instruction}
'''

cot_prompt = '''
Given a question, your task is to decompose it into manageable sub-questions. For each sub-question, summarize existing information, determine the new information required, and then articulate a logical and useful sub-question that brings you closer to the final answer. Conclude each answer with "The answer is". When ready to address the original question, your final sub-question should contain "Now we can answer the question: ", leading to a detailed answer that encapsulates all the insights gained, always ending with "The answer is".

Question 1: Four years ago, Kody was only half as old as Mohamed. If Mohamed is currently twice as 30 years old, how old is Kody?
Question 1.1: We start by understanding that four years ago, Kody's age was half that of Mohamed's, and currently, Mohamed is twice 30 years old. To proceed, we need Mohamed's current age. Therefore, the next useful subquestion we need to solve is: What is Mohamed's current age?
Answer 1.1: Since Mohamed is currently twice 30, we calculate 2 * 30 = 60. Thus, Mohamed is 60 years old now. The answer is 60.
Question 1.2: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?
Answer 1.2: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.
Question 1.3: Knowing that Mohamed was 56 years old four years ago enables us to figure out Kody's age at that time, given that Kody was half as old as Mohamed. Therefore, the next useful subquestion we need to solve is: How old was Kody four years ago?
Answer 1.3: If Kody was half as old as Mohamed four years ago, then 56 / 2 = 28. Kody was 28 years old four years ago. The answer is 28.
Question 1.4: With the information that Kody was 28 years old four years ago, the final piece of information we need is his current age. Now we can answer the question: How old is Kody now?
Answer 1.4: Kody was 28 years old four years ago. Adding those four years to his age, we calculate 28 + 4 = 32. Kody is now 32 years old. The answer is 32.

Question 2: On a moonless night, three fireflies danced in the evening breeze. They were joined by four less than a dozen more fireflies before two of the fireflies flew away. How many fireflies remained?
Question 2.1: We start with the initial information that three fireflies were present, and then they were joined by four less than a dozen more fireflies. To proceed, we need to calculate the total number of fireflies that joined. Therefore, the next useful subquestion we need to solve is: How many fireflies joined the initial three?
Answer 2.1: A dozen fireflies minus four gives us 12 - 4 = 8 fireflies that joined the initial three. The answer is 8.
Question 2.2: With the knowledge that 8 fireflies joined the initial 3, we next need to find out the total number of fireflies before any of them flew away. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?
Answer 2.2: The total number of fireflies before any flew away can be found by adding the initial three to the eight that joined, which gives us 3 + 8 = 11 fireflies. The answer is 11.
Question 2.3: Knowing that there were 11 fireflies before two flew away gives us the information needed to determine how many remained. Now we can answer the question: How many fireflies remained after two flew away?
Answer 2.3: From the 11 fireflies, if two flew away, we subtract two from the total, which gives us 11 - 2 = 9 fireflies remaining. The answer is 9.

Question 3: {input}
'''