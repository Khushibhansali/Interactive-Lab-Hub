# Counts the number of words received

class WordCounter:
    def __init__(self):
        self.current_word = None
        self.count = 0

    def process_word(self, word):
        if self.current_word == word:
            self.count += 1
            # print(f"The word '{word}' has been received '{self.count}' times.")
            # if self.count == 50:
            #     print(f"The word '{word}' has been received '{self.count}' times. Counting finished.")
            #     # self.reset_counter()  # Uncomment this line if you want to reset on reaching count 50.
        else:
            self.current_word = word
            self.count = 0

    



# Example usage:
# word_counter = WordCounter()

# words_to_process = ["apple", "apple", "apple", "orange", "orange", "banana", "banana", "banana", "banana", "grape"]

# for word in words_to_process:
#     word_counter.process_word(word)
