def lz77_compress(string, window_size):
   compressed = []
   position = 0
   while position < len(string):
        # at the near beginning of the string
      if position - window_size < 0:
         search_window_position = 0
      else:
         search_window_position = position - window_size
      
      best_match_length = 0
      best_match_offset = 0

   # we are going back to characters we have seen before
      for history_pointer in range(search_window_position, position):
         possible_match_length = 0
         while position + possible_match_length < len(string):
            if string[possible_match_length + history_pointer] == string[position + possible_match_length]:
               possible_match_length += 1
               if history_pointer + possible_match_length >= position: # we can't look forward from our current position
                  break
            else:
               break

         if possible_match_length > best_match_length:
            best_match_length = possible_match_length
            best_match_offset = position - history_pointer

      if best_match_length > 0:
         if position + best_match_length < len(string):
            character = string[position + best_match_length]
         else:
            character = ""
         position += best_match_length + 1
         compressed.append((best_match_offset,best_match_length,character))
      else:
         compressed.append((0,0,string[position]))
         position += 1
   return compressed

def lz77_decompress(compressed):
   decompressed = []
   for offset, match_length, character in compressed:
      if offset == 0 and match_length == 0:
         decompressed.append(character)
      else:
         goBackPosition = len(decompressed) - offset
         charactersAdded = 0
         while charactersAdded != match_length:
            decompressed.append(decompressed[goBackPosition])
            goBackPosition += 1
            charactersAdded += 1
         decompressed.append(character)
      
   return ''.join(decompressed)
