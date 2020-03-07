

import codecs

class DatabaseManager:

  rbheFile = "database\\rbhe_file.txt"

  def addToRbheFile(self, title, author, summary, key_words):
    print("Starting to add to file")
    file_to_write = codecs.open(self.rbheFile,"a", "utf-8") 
    file_to_write.writelines(title)
    file_to_write.write("\n")
    file_to_write.writelines(author)
    file_to_write.write("\n")
    file_to_write.writelines(summary)
    file_to_write.write("\n")
    file_to_write.writelines(key_words)
    file_to_write.write("\n")
    file_to_write.write(" ")
    file_to_write.write("\n")
    file_to_write.close()
    print("Add to file ok")