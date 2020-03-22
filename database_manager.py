

import codecs

class DatabaseManager:

  rbheFile = "database\\rbhe_file.txt"

  def addToRbheFile(self, title, authors, summary, key_words):
    print("Starting to add to file")
    file_to_write = codecs.open(self.rbheFile,"a", "utf-8") 
    
    #title
    
    file_to_write.writelines(title)
    file_to_write.write("\n")

    # authors
    print(authors)
    file_to_write.writelines(", ".join(authors))
    file_to_write.write("\n")

    file_to_write.write("RESUMO")
    file_to_write.write("\n")

    # Summary
    file_to_write.writelines(summary)
    file_to_write.write("\n")

    # Keywords
    file_to_write.write("PALAVRAS-CHAVE: ")
    file_to_write.writelines("; ".join(key_words))
    file_to_write.write("\n")

    # Divider
    file_to_write.write(" ")
    file_to_write.write("\n")
    file_to_write.close()
    print("Add to file ok")