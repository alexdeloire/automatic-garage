


def convert_seconds(seconds):
    #Cette fonction converti un nombre de secondes en un format plus lisible
    #Secondes en ..h..min..s
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return str(hours)+"h"+str(minutes)+"min"+str(remaining_seconds)+"s"

#Tests
"""
test=156254.97286
test = int(test)
print(test)
#seconds = int(input("Secondes: "))
print(convert_seconds(test))
"""
