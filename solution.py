
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist+[['A1','B2','C3','D4','E5','F6','G7','H8','I9']] 
unitlist = unitlist+[['A9','B8','C7','D6','E5','F4','G3','H2','I1']] 

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):

    digits='2345678'
    for unit in unitlist:
        for digit in digits:
            There_is_Twins=True
            naked_values_prev=''
            
            while There_is_Twins == True:
                
                if len(naked_values_prev)<2:
                    naked_box = [box for box in unit if len(values[box])==int(digit)]
                else:
                    naked_box = [box for box in unit  if (len(values[box])==int(digit))]
                    for m in range(len(naked_values_prev)):
                        kk=0
                        while kk < len(naked_box):
                            if (naked_values_prev[m] in values[naked_box[kk]]):
                                del naked_box[kk]
                            else:
                                kk+=1
                                
                if len(naked_box)>=int(digit):
                    for k in range(len(naked_box)):
                        if(len([dbox_element for dbox_element in naked_box[k:len(naked_box)] if values[naked_box[k]] == values[dbox_element]])==int(digit)):
                            naked_values=values[naked_box[k]]
                            dbox=[box for box in unit if values[box]!=naked_values]
                            for x in range(len(naked_values)):
                               for y in range(len(dbox)):
                                   values[dbox[y]]=values[dbox[y]].replace(naked_values[x],'')
                            naked_values_prev+=naked_values
                            break
                            
                        elif k==len(naked_box)-1:
                            There_is_Twins=False
                             
                else:
                    There_is_Twins=False


    return values


def eliminate(values):

    grid_updated = values
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for y in solved_values:
        x=values[y]
        if len(x)==1:
            for k in peers[y]:
                grid_updated[k]=grid_updated[k].replace(x,'')
            
    return grid_updated


def only_choice(values):

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Your code here: Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):

    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
