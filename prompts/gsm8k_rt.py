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
Given a question, please decompose it into sub-questions. For each sub-question, please answer it in a complete sentence, ending with "The answer is". When the original question is answerable, please start the subquestion with "Now we can answer the question: ".

Question 1: Four years ago, Kody was only half as old as Mohamed. If Mohamed is currently twice as 30 years old, how old is Kody?
Question 1.1: How old is Mohamed?
Answer 1.1: He is currently 30 * 2 = 60 years old. The answer is 60.
Question 1.2: How old was Mohamed four years ago?
Answer 1.2: Four years ago, he must have been 60 - 4 = 56 years old. The answer is 56.
Question 1.3: How old was Kody four years ago?
Answer 1.3: Kody was half as old as Mohamed four years ago. Thus, Kody was 56 / 2 = 28 years old. The answer is 28.
Question 1.4: Now we can answer the question: How old is Kody?
Answer 1.4: She is currently 28 + 4 = 32 years old. The answer is 32.

Question 2: On a moonless night, three fireflies danced in the evening breeze. They were joined by four less than a dozen more fireflies before two of the fireflies flew away. How many fireflies remained?
Question 2.1: How many fireflies joined?
Answer 2.1: The fireflies were joined by four less than a dozen more fireflies, which are 12 - 4 = 8 fireflies. The answer is 8.
Question 2.2: Now we can answer the question: How many fireflies remained?
Answer 2.2: Three fireflies were dancing originally. They were joined by 8 fireflies before two of them flew away. So there were 3 + 8 - 2 = 9 remaining. The answer is 9.

Question 3: Ali has four $10 bills and six $20 bills that he saved after working for Mr. James on his farm. Ali gives her sister half of the total money he has and uses 3/5 of the remaining amount of money to buy dinner. Calculate the amount of money he has after buying the dinner.
Question 3.1: How much money does Ali have in total?
Answer 3.1: Ali has four $10 bills and six $20 bills. So he has 4 * 10 + 6 * 20 = 160 dollars. The answer is 160.
Question 3.2: How much money does Ali give to his sister?
Answer 3.2: Ali gives half of the total money he has to his sister. So he gives 160 / 2 = 80 dollars to his sister. The answer is 80.
Question 3.3: How much money does Ali have after giving his sister the money?
Answer 3.3: After giving his sister the money, Ali has 160 - 80 = 80 dollars left. The answer is 80.
Question 3.4: How much money does Ali use to buy dinner?
Answer 3.4: Ali uses 3/5 of the remaining amount of money to buy dinner. So he uses 80 * 3/5 = 48 dollars to buy dinner. The answer is 48.
Question 3.5: Now we can answer the question: How much money does Ali have after buying the dinner?
Answer 3.5: After buying the dinner, Ali has 80 - 48 = 32 dollars left. The answer is 32.

Question 4: A car is driving through a tunnel with many turns. After a while, the car must travel through a ring that requires a total of 4 right-hand turns. After the 1st turn, it travels 5 meters. After the 2nd turn, it travels 8 meters. After the 3rd turn, it travels a little further and at the 4th turn, it immediately exits the tunnel. If the car has driven a total of 23 meters around the ring, how far did it have to travel after the 3rd turn?
Question 4.1: How far did the car travel except for the 3rd turn?
Answer 4.1: It travels 5 meters after the 1st, 8 meters after the 2nd, and 0 meters after the 4th turn. It's a total of 5 + 8 + 0 = 13 meters. The answer is 13.
Question 4.2: Now we can answer the question: How far did the car have to travel after the 3rd turn?
Answer 4.2: The car has driven a total of 23 meters around the ring. It travels 13 meters except for the 3rd turn. So it has to travel 23 - 13 = 10 meters after the 3rd turn. The answer is 10.

Question 5: {input}
'''