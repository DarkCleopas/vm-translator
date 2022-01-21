

class Parser:


    def __init__(self, file_name):

        self.file_name = file_name
        
        self.tokens = self.load_tokens()


    def load_tokens(self):

        with open(self.file_name) as f:
            
            lines = map(lambda line: line.split(), f.readlines())
            
            tokens = list(filter(lambda x: x[0][0:2] != "//", lines))

            return tokens
    

    # def remove_comments(self, line):

    #     count = 0

    #     for term in line:

    #         if term[0:2] == "//":

    #             return line[0:count]
            
    #         count += 1


    def get_command(self):
        
        return self.tokens.pop(0)
    

    def has_more_commands(self):
        
        return self.tokens != []
    
if __name__ == "__main__":

    p = Parser("vm_example.vm")

    print(p.tokens)