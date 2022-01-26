

class Parser:


    def __init__(self, file_name):

        self.file_name = file_name
        
        self.tokens = self.load_tokens()


    def load_tokens(self):

        with open(self.file_name) as f:
            
            lines = map(lambda line: self.remove_comments(line).split(), f.readlines())
            
            tokens = [line for line in lines if line != []]

            return tokens
    

    def remove_comments(self, line):

        j = 0
        for i in range(1, len(line)):
            if line[j] == line[i] == "/":
                return line[:j]
            j += 1

        return line


    def get_command(self):
        
        return self.tokens.pop(0)
    

    def has_more_commands(self):
        
        return self.tokens != []
    
if __name__ == "__main__":

    p = Parser("vm_example.vm")

    print(p.tokens)