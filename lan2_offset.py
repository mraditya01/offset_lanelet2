#Edit path and name here
name = 'lanelet2_map.osm'
name2= 'lanelet2_map2.osm'
#The location of the original file
file_read = '/File/'+name
#The location of where you want the new file written
file_write = '/File/'+name2
#Note: the name that is used to read and write is the same, so if you select the same directory, it will overwrite the original file
#To  fix it, change the name in file_write to something else


#Your lat and long offset. You can keep it a 0 if you don't want to shift
long_offset = 0.3051
lat_offset = 0.00301483

#some variables
Node_Dict = {} #   Dict =  lat long (abbriviated) : [ lat long (full), Note IDs]
is_nd = False
prev_line = ''

#Opening the reading file
with open(file_read) as file_r:
    #Iterating through each line
    for line in file_r:
        new_line = ''
        current_line = line.split() #splitting line into words
        

        #Checking to see whether it is a new node on the line
        if current_line[0] == "<node":

            #Appending or making a new dictionary entry            
            dict_value = current_line[4] + " "+ current_line[5] #lat="xxxx" long="xxxx"
            dict_key= str(round(float(current_line[4][5:-1]), 5)) + " "+ str(round(float(current_line[5][5:-3]),6)) #getting just the numbers or the xxxx from above

            Node_Dict[dict_key] =  [dict_value, current_line[1][4:-1]] #If not, make a new entry

        for word in line.split():

            #substituing for the new id
            if is_nd:
                is_nd = False
                id_num = current_line[1][5:-3] #get current id's number
                which_id_to_use = id_num #which ID to overwrite it with. If the next if doesn't get triggered, the ID stays the same
                for other_value in Node_Dict:
                    if id_num in Node_Dict[other_value]:
                        which_id_to_use = Node_Dict[other_value][1] #Use the first value that has the same location
                        word = 'ref="'+str(which_id_to_use)+'"/>'
                        #print(word)
                        break

            if word[0] == '<':
                if word == "<node" or word == "<way"or word == "</way>" or word == "<relation" or word == "</relation>" or word == "</node>":
                    word = '  '+word
                elif word == "<nd" or word == "<member" or word == "<tag":
                    if word == "<nd":
                        is_nd = True
                    word = '  '+'  '+word
            #If none of the starting words, then it's just space before the next word  
            else:
                new_line =new_line+' '

            #Picking appart the lat and long incase it needs to be shifted
            if word[0] == 'l' and word[1] == 'a' and word[2] == 't':
                word = 'lat="'+ str(float(word[5:-1]) + lat_offset) +'"'
            elif word[0] == 'l' and word[1] == 'o' and word[2] == 'n':
                word = 'lon="'+ str(float(word[5:-3]) + long_offset)+'">'

            #Adding the edited word to the new line
            new_line = new_line + word

        # #if the line is the same as previous, we can skip it. Mostly used to not write reduntant points with same lat and long. 
        if prev_line==new_line:
            continue
        #Writing to the new file
        with open(file_write, 'a') as file_w:
            file_w.write(new_line +'\n')

        #updating the previous line
        prev_line = new_line
